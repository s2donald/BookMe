from .models import Account
from consumer.models import Bookings
from .serializers import CompanySerializer, AccountSerializer, BookingSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from business.models import Company

##Company API
class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]


## Account API

class UsersListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UsersCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UserDeleteView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Account.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


##Booking API
class BookingListView(generics.ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
