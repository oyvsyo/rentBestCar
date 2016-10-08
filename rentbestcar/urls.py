from django.conf.urls import include, url, patterns
from django.contrib import admin
from settings import STATIC_ROOT
from tastypie.api import Api
from app.api import *

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(UserProfileResource())
v1_api.register(OwnerResource())
v1_api.register(RenterResource())
v1_api.register(CarResource())
v1_api.register(TransactionResource())

urlpatterns = [
    url(r'^$', 'app.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
]

urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}), )

