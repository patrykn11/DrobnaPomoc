from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import RegexValidator
from django.db import transaction
from rest_framework import serializers

from .models import ContractorProfile, User

phone_number_validator = RegexValidator(
    regex=r"^\+?[0-9]{9,15}$",
    message="Podaj prawidłowy numer telefonu zawierający od 9 do 15 cyfr.",
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = fields


class SelectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]

    def validate_role(self, value):
        if value == User.Role.UNDEFINED:
            raise serializers.ValidationError("Wybierz właściwą rolę.")
        if value == User.Role.CONSULTANT:
            raise serializers.ValidationError(
                "Rolę konsultanta może nadać tylko administrator."
            )
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.role != User.Role.UNDEFINED:
            raise serializers.ValidationError({"role": "Rola została już wybrana."})

        role = validated_data["role"]
        instance.role = role
        instance.save(update_fields=["role", "updated_at"])

        if role == User.Role.CONTRACTOR:
            ContractorProfile.objects.get_or_create(user=instance)
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[phone_number_validator],
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        user = User(
            username=attrs.get("username", ""),
            email=attrs.get("email", ""),
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
            phone_number=attrs.get("phone_number", ""),
        )

        try:
            validate_password(attrs["password"], user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"password": list(error.messages)}
            ) from error

        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        auth_user = authenticate(username=username, password=password)

        if auth_user is None:
            raise serializers.ValidationError(
                "Nieprawidłowa nazwa użytkownika lub hasło."
            )

        attrs["user"] = auth_user

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["user"]

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Stare hasło jest nieprawidłowe."}
            )

        if user.check_password(attrs["new_password"]):
            raise serializers.ValidationError(
                {"new_password": "Nowe hasło musi być inne niż stare hasło."}
            )

        try:
            validate_password(attrs["new_password"], user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"new_password": list(error.messages)}
            ) from error

        return attrs
