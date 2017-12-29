"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import thepopularevents.views
import django.views.static
import os
print os.path.join(settings.BASE_DIR, "static")
os.system('ls %s' % (os.path.join(settings.BASE_DIR, "static")))
urlpatterns = [
    url(r'^static/(?P<path>.*)$', django.views.static.serve,{'document_root':os.path.join(settings.BASE_DIR, "static/")}),
    url(r'^admin/', admin.site.urls),
    url(r'^$', thepopularevents.views.home_page, name='home'),
    url(r'^get_events/$',
        thepopularevents.views.get_events, name='get_events'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
