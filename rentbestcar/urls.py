from django.conf.urls import include, url, patterns
from django.contrib import admin
from settings import STATIC_ROOT

urlpatterns = [
    url(r'^$', 'app.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}), )

