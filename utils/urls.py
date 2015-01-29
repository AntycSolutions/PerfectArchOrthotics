from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from utils import views


urlpatterns = patterns(
    '',
    url(r'^thumbnail/(?P<width>\d+)/(?P<height>\d+)/(?P<url>.+)/$',
        login_required(views.get_thumbnail),
        name='get_thumbnail'),
)
