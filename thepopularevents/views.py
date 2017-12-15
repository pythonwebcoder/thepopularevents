from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
import settings
import requests

def home_page(request):
    return render(request, 'index.html', {'googleapikey': settings.GOOGLEAPIKEY})

def get_events(request):
    import requests
    if not settings.MEETUPAPIKEY:
        return JsonResponse({'success': False, 'error': 'MEETUPAPIKEY environment variable not set'})

    events_url = 'https://api.meetup.com/find/upcoming_events?radius=%s&lat=%s&lon=%s&page=2000&key=%s&end_date_range=2020-12-30T00:00:00' % (request.GET.get('radius'), request.GET.get('lat'), request.GET.get('lng'),settings.MEETUPAPIKEY)
    print events_url
    print requests.get(events_url)
    events = requests.get(events_url).json()['events']
    top_ten_events = sorted([y for y in events], key=lambda t: t.get('yes_rsvp_count'), reverse=True)[:10]
    days_to_events = dict([(x, sorted([y for y in events if y.get('local_date') == x], key=lambda t: t.get('yes_rsvp_count'), reverse=True)) for x in [row.get("local_date") for row in events]])
    data = {'most_popular_events_per_day': days_to_events, 'top_ten_events': top_ten_events}
    return JsonResponse(data, safe=False)
