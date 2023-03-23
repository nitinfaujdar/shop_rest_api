from rest_framework import serializers
from django.db.models import Q
from django.core.validators import MinLengthValidator
from shop.models import *

# User register serializer using JWT Authentication
class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(validators=[MinLengthValidator(5)], allow_null=False, required=True,
                                     write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email',  'password']

    def validate_phone(self, attrs):
        user = User.objects.filter(phone=attrs)
        if user.exists():
            raise serializers.ValidationError("This phone number already exist")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone=validated_data['phone'],
            email=validated_data['email'],
        )
        user = User.objects.get(phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        return user

# User Login serializer using JWT Authentication
class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['phone','password']

class SocialLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['latitude', 'longitude']

    def update(self, instance, validated_data):
        instance.latitude = validated_data['latitude']
        instance.longitude = validated_data['longitude']
        instance.save()
        return instance

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop 
        fields = '__all__'

    # checking whether the shop already exist or not 
    def validate_shop(self, attrs):
        shop = Shop.objects.filter(shop_name=attrs)
        if shop.exists():
            raise serializers.ValidationError("A shop with this name already exists")
        return attrs

    # creating a new shop's data
    def create(self, validated_data):
        obj = Shop.objects.create(
            shop_name=validated_data['shop_name'],
            shop_address=validated_data['shop_address'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
        )
        return obj

class ShopReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopReview
        fields = '__all__'

    # posting a review for a particular shop
    def create(self, validated_data):
        obj = ShopReview.objects.create(
            user=validated_data['user'],
            shop=validated_data['shop'],
            shop_review=validated_data['shop_review'],
        )
        return obj
        