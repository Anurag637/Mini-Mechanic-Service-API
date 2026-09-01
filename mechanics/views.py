import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Mechanic, ServiceRequest
from .serializers import MechanicSerializer, ServiceRequestSerializer

logger = logging.getLogger('mechanics')


class MechanicListCreateView(ListCreateAPIView):
    queryset = Mechanic.objects.all().order_by('id')
    serializer_class = MechanicSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        location = self.request.query_params.get('location')
        is_open = self.request.query_params.get('is_open')

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(location__icontains=search))
        if location:
            queryset = queryset.filter(location__icontains=location)
        if is_open is not None:
            queryset = queryset.filter(is_open=is_open.lower() in {'true', '1', 'yes'})
        logger.info('Mechanic list requested with filters: search=%s location=%s is_open=%s', search, location, is_open)
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        logger.info('Mechanic created: %s', request.data.get('name'))
        return response


class MechanicDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Mechanic.objects.all().order_by('id')
    serializer_class = MechanicSerializer

    def delete(self, request, *args, **kwargs):
        mechanic = self.get_object()
        logger.info('Mechanic deleted: %s', mechanic.name)
        return super().delete(request, *args, **kwargs)


class ServiceRequestListCreateView(ListCreateAPIView):
    queryset = ServiceRequest.objects.select_related('mechanic').order_by('-created_at')
    serializer_class = ServiceRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_request = serializer.save()
        logger.info('Service request created for mechanic %s by %s', service_request.mechanic_id, service_request.customer_name)
        response = self.get_serializer(service_request)
        return Response(response.data, status=status.HTTP_201_CREATED)
