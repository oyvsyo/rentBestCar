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
    url(r'^$', 'app.views.index', name='index'),
    url(r'^car/(?P<car_id>\d+)/$', 'app.views.car', name='car'),
    url(r'^car-edit$', 'app.views.car_edit', name='car_edit'),
    url(r'^car-list$', 'app.views.car_list', name='car_list'),
    url(r'^owner-profile$', 'app.views.owner_profile', name='owner_profile'),
    url(r'^owner-profile-edit$', 'app.views.owner_profile_edit', name='owner_profile_edit'),
    url(r'^renter-profile$', 'app.views.renter_profile', name='renter_profile'),
    url(r'^renter-profile-edit$', 'app.views.renter_profile_edit', name='renter_profile_edit'),
    url(r'^transaction$', 'app.views.transaction', name='transaction'),

    # auth
    url(r'^login', 'app.views.login', name='login'),
    url(r'^registration', 'app.views.registration', name='registration'),
    url(r'^forgot_password', 'app.views.forgot_password', name='forgot_password'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
]

urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}), )

