from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Mechanic, ServiceRequest


class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = ['id', 'name', 'phone', 'location', 'rating', 'is_open', 'services']

    def create(self, validated_data):
        try:
            return Mechanic.objects.create(**validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict if hasattr(exc, 'message_dict') else exc.messages)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            instance.save()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict if hasattr(exc, 'message_dict') else exc.messages)
        return instance


class ServiceRequestSerializer(serializers.ModelSerializer):
    mechanic_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'customer_name',
            'customer_phone',
            'vehicle_number',
            'mechanic_id',
            'service',
            'problem_description',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_mechanic_id(self, value):
        try:
            Mechanic.objects.get(id=value)
        except Mechanic.DoesNotExist:
            raise serializers.ValidationError('Mechanic does not exist.')
        return value

    def validate(self, data):
        mechanic_id = data.get('mechanic_id')
        service = data.get('service')

        if mechanic_id is not None:
            mechanic = Mechanic.objects.get(id=mechanic_id)
            available_services = [item.strip().lower() for item in mechanic.services if isinstance(item, str)]
            if service is not None and service.strip().lower() not in available_services:
                raise serializers.ValidationError({'service': 'Invalid service for the selected mechanic.'})

        return data

    def create(self, validated_data):
        mechanic_id = validated_data.pop('mechanic_id')
        mechanic = Mechanic.objects.get(id=mechanic_id)
        try:
            return ServiceRequest.objects.create(mechanic=mechanic, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict if hasattr(exc, 'message_dict') else exc.messages)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['mechanic_id'] = instance.mechanic_id
        return representation
