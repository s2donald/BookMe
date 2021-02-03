from rest_framework import serializers
from .models import Account
from business.models import Company

from consumer.models import Bookings

class CompanySerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=True, queryset=Account.objects.all())
    user = serializers.ReadOnlyField(source='company.user')
    class Meta:
        model = Company
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("first_name", "last_name","email","phone","tz","id","address", "postal","province","on_board", "is_business", "avatar","city")

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
