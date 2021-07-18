from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice"""

    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "client_name",
            "client_email",
            "project_name",
            "amount",
            "paid",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        email = attrs.get("client_email", "")
        try:
            validate_email(email)
            return attrs

        except Exception as e:
            raise serializers.ValidationError("Invalid email id!")

    def create(self, validated_data):
        return Invoice.objects.create(**validated_data)
