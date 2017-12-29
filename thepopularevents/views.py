from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from . import settings
import requests


def home_page(request):
    return render(request, 'index.html', {'googleapikey': settings.GOOGLEAPIKEY})


def has_food(description):
    items = ['food', 'happy hour', 'snacks', 'appetizer', 'pizza']
    if not description:
        return False
    for item in items:
        if item in description.lower():
            return True
    return False


def get_events(request):
    import requests
    if not settings.MEETUPAPIKEY:
        return JsonResponse({'success': False, 'error': 'MEETUPAPIKEY environment variable not set'})
    events = []
    import datetime
    two_months_from_now = (datetime.date.today() + datetime.timedelta(2*365/12)).isoformat()
    events_url = 'https://api.meetup.com/find/upcoming_events?radius=%s&order=time&lat=%s&lon=%s&page=20000&key=%s&end_date_range=%sT00:00:00' % (
        request.GET.get('radius'), request.GET.get('lat'), request.GET.get('lng'), settings.MEETUPAPIKEY, two_months_from_now)
    result = requests.get(events_url)
    events.extend(result.json()['events'])
    while True:
        events_url = result.headers.get('Link')
        if not events_url:
            break
        events_url = events_url[1:events_url.index('>')]
        result = requests.get(events_url)
        events.extend(result.json()['events'])
    print '# of events ', len(events)
    top_ten_events = sorted(
        [y for y in events], key=lambda t: t.get('yes_rsvp_count'), reverse=True)[:10]
    top_ten_events_with_food = [z for z in sorted([y for y in events], key=lambda t: t.get(
        'yes_rsvp_count'), reverse=True) if has_food(z.get('description'))][:10]
    days_to_events = dict([(x, sorted([y for y in events if y.get('local_date') == x], key=lambda t: t.get('yes_rsvp_count'), reverse=True))
                          for x in [row.get("local_date") for row in events]])
    eventbrite_per_day = requests.get('https://www.eventbriteapi.com/v3/events/search/?location.longitude=%s&location.latitude=%s&location.within=%smi&token=%s' %
                                      (request.GET.get('lng'), request.GET.get('lat'), request.GET.get('radius'), settings.EVENTBRITEAPIKEY)).json()
    print 'https://www.eventbriteapi.com/v3/events/search/?location.longitude=%s&location.latitude=%s&location.within=%smi&token=%s' % (request.GET.get('lng'), request.GET.get('lat'), request.GET.get('radius'), settings.EVENTBRITEAPIKEY)
    data = {
        'most_popular_events_per_day': days_to_events,
            'top_ten_events': top_ten_events,
           'top_ten_events_with_food': top_ten_events_with_food, 'eventbrite_per_day': eventbrite_per_day}
    return JsonResponse(data, safe=False)
