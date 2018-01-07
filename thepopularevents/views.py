from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from . import settings
import requests
import datetime


def home_page(request):
    return render(request, 'index.html', {'googleapikey': settings.GOOGLEAPIKEY, 'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY})


def has_food(description):
    items = [
        'food',
        'happy hour',
     'snacks',
     'appetizer',
     'pizza',
     'lunch',
     'breakfast',
     'dinner']
    if not description:
        return False
    for item in items:
        if item in description.lower():
            return True
    return False


def convert_to_date(time):
    import datetime
    return datetime.datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d')


def make_days_to_events(events):
    return dict([(date, sorted([event for event in events if convert_to_date(event.get('time')) == date], key=lambda t: t.get('yes_rsvp_count'), reverse=True))
                 for date in set([convert_to_date(row.get("time")) for row in events])])


def get_meetup_event_data(request, next_url=None, events=[]):
    if next_url:
        events_url = next_url
    else:
        events_url = 'https://api.meetup.com/2/open_events?fields=timezone&and_text=False&sign=True&format=json&page=1000&radius=%s&order=time&lat=%s&lon=%s&key=%s&text_format=plain&time=,2m&text=%s' % (
            request.GET.get('radius'), request.GET.get('lat'), request.GET.get('lng'), settings.MEETUPAPIKEY, request.GET.get('search_terms', ''))
    result = requests.get(events_url)
    try:
        events.extend(result.json()['results'])
    except:
        return events
    next_url = result.json()['meta'].get('next')
    if not next_url:
        return events
    else:
        return get_meetup_event_data(request, next_url=next_url, events=events)


def get_events(request):

    if not settings.MEETUPAPIKEY:
        return JsonResponse({'success': False, 'error': 'MEETUPAPIKEY environment variable not set'})
    events = get_meetup_event_data(request)

    top_ten_events = sorted(
        [event for event in events], key=lambda event: event.get('yes_rsvp_count'), reverse=True)[:10]
    top_ten_events_with_food = [event for event in sorted([event for event in events], key=lambda event: event.get(
        'yes_rsvp_count'), reverse=True) if has_food(event.get('description'))][:10]
    days_to_events = make_days_to_events(events)

    data = {
        'most_popular_events_per_day': days_to_events,
            'top_ten_events': top_ten_events,
           'top_ten_events_with_food': top_ten_events_with_food}
    return JsonResponse(data, safe=False)
