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

def convert_to_date(time):
    import datetime
    return datetime.datetime.fromtimestamp(time/1000).strftime('%Y-%m-%d')

def get_events(request):
    import requests
    if not settings.MEETUPAPIKEY:
        return JsonResponse({'success': False, 'error': 'MEETUPAPIKEY environment variable not set'})
    events = []
    import datetime
    events_url = 'https://api.meetup.com/2/open_events?and_text=False&offset=1&sign=True&format=json&page=1000&radius=%s&order=time&lat=%s&lon=%s&key=%s&time=0,2m' % (
        request.GET.get('radius'), request.GET.get('lat'), request.GET.get('lng'), settings.MEETUPAPIKEY)
    result = requests.get(events_url)
    try:
        events.extend(result.json()['results'])
    except:
        print result.text
    i = 0
    while True:
        i += 1
        events_url = result.json()['meta'].get('next')
        if not events_url:
            break
        print events_url
        try:
            result = requests.get(events_url)

        except:
            break
        events.extend(result.json()['results'])
    top_ten_events = sorted(
        [y for y in events], key=lambda t: t.get('yes_rsvp_count'), reverse=True)[:10]
    print len(events)
    top_ten_events_with_food = [z for z in sorted([y for y in events], key=lambda t: t.get(
        'yes_rsvp_count'), reverse=True) if has_food(z.get('description'))][:10]
    days_to_events = dict([(x, sorted([y for y in events if convert_to_date(y.get('time')) == x], key=lambda t: t.get('yes_rsvp_count'), reverse=True))
                          for x in [convert_to_date(row.get("time")) for row in events]])

    data = {
        'most_popular_events_per_day': days_to_events,
            'top_ten_events': top_ten_events,
           'top_ten_events_with_food': top_ten_events_with_food}
    return JsonResponse(data, safe=False)
