from datetime import datetime
from django.contrib.auth.models import User

from app.models import UserProfile, Owner, Renter, Car, Transaction

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.validation import FormValidation
from tastypie import fields


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'User'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        fields = ['id', 'last_login']
        # allowed_methods = ['get']
        filtering = {
            # 'User': ALL_WITH_RELATIONS,
            'id': ALL,
            'username': ALL,
            'updated': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        always_return_data = True
        authorization = Authorization()


class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'UserProfile'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        # fields = ['id', 'last_login']
        # allowed_methods = ['get']
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }
        always_return_data = True
        authorization = Authorization()


class OwnerResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Owner.objects.all()
        resource_name = 'Owner'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        # fields = ['id', 'last_login']
        # allowed_methods = ['get']
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }
        always_return_data = True
        authorization = Authorization()

class RenterResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Renter.objects.all()
        resource_name = 'Renter'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        # fields = ['id', 'last_login']
        # allowed_methods = ['get']
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }
        always_return_data = True
        authorization = Authorization()

class CarResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Car.objects.all()
        resource_name = 'Car'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        # fields = ['id', 'last_login']
        # allowed_methods = ['get']
        # filtering = {
        #     'user': ALL_WITH_RELATIONS,
        # }
        always_return_data = True
        authorization = Authorization()

class TransactionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Transaction.objects.all()
        resource_name = 'Transaction'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        # fields = ['id', 'last_login']
        # allowed_methods = ['get']
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }
        always_return_data = True
        authorization = Authorization()