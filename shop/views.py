from rest_framework_simplejwt.tokens import RefreshToken
from .tests import BadRequest
from .models import User
from .tests import http_response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from haversine import haversine, Unit
from .models import *
from .serializers import *

# Create your views here.

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        register_serializer = UserRegisterSerializer(data=request.data)
        if not register_serializer.is_valid():
            raise ValidationError(
                {
                    'error_message': 'Please correct the following errors.',
                    'errors': register_serializer.errors,
                }
            )
        # saving the details of the registered user
        user = register_serializer.save()
        return http_response(data=self.get_tokens_for_user(user, register_serializer),
                                 message='Register Successfully', status_code=status.HTTP_201_CREATED)

    # generating access token for the user     
    def get_tokens_for_user(self, user, register_serializer):
        refresh = RefreshToken.for_user(user)
        return {
            'user': {'id': user.id,
                     'username': register_serializer.data['username'],
                     'phone': register_serializer.data['phone'], },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class LoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        login_serializer = UserLoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            raise ValidationError(
                {
                    'error_message': 'Please correct the following errors.',
                    'errors': login_serializer.errors,
                }
            )
        founded_user = User.objects.get(phone=request.data['phone'])
        if not founded_user.check_password(login_serializer.data['password']):
            raise BadRequest({'error_message': 'Incorrect authentication credentials.'})
        return http_response(data=self.get_tokens_for_user(founded_user, login_serializer),
                            message='Login Successfully', status_code=status.HTTP_200_OK)

    # generating access token for the user     
    def get_tokens_for_user(self, user, login_serializer):
        refresh = RefreshToken.for_user(user)
        return {
            'user': {'phone': login_serializer.data['phone']},
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
# Login from facebook or google using email ID by JWT Authentication
class SocialLoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SocialLoginSerializer

    def post(self, request, *args, **kwargs):
        login_serializer = SocialLoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            raise ValidationError(
                {
                    'error_message': 'Please correct the following errors.',
                    'errors': login_serializer.errors,
                }
            )
        founded_user = User.objects.get(email=request.data['email'])
        return http_response(data=self.get_tokens_for_user(founded_user, login_serializer),
                            message='Login Successfully', status_code=status.HTTP_200_OK)
    # generating access token for the user 
    def get_tokens_for_user(self, user, login_serializer):
        refresh = RefreshToken.for_user(user)
        return {
            'user': {'email': login_serializer.data['email']},
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ShopView(generics.CreateAPIView,generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShopSerializer

    # getting the list of all the shops 
    def get(self, request, *args, **kwargs):
        users = Shop.objects.filter(is_deleted=False)
        serializer = ShopSerializer(users, many=True)
        return http_response(data=serializer.data, message='List Retreived Successfully', 
                             status_code=status.HTTP_200_OK)
    
    # posting a new shop's details
    def post(self, request, *args, **kwargs):
        serializer = ShopSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(
                {
                    'error_message': 'Please correct the following errors.',
                    'errors': serializer.errors,
                }
            )
        serializer.save()
        return http_response(data=serializer.data, message='Data Created Sucessfully', 
                            status_code=status.HTTP_200_OK)

class ShopReviewView(generics.CreateAPIView,generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    # getting the list of reviews posted by a particular user using JWT Authentication
    def get(self, request, *args, **kwargs):
        users = Shop.objects.filter(user_id=request.user.id, is_deleted=False)
        serializer = ShopSerializer(users, many=True)
        return http_response(data=serializer.data, message='List Retreived Successfully', 
                             status_code=status.HTTP_200_OK)
    # posting reviews for a particular shop by a particular user using JWT Authentication
    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user
        serializer = ShopSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(
                {
                    'error_message': 'Please correct the following errors.',
                    'errors': serializer.errors,
                }
            )
        serializer.save()
        return http_response(data=serializer.data, message='Data Created Sucessfully', 
                            status_code=status.HTTP_200_OK)

# calculating distance between user and shops
def get_distance_between_user_and_shop(latitude, longitude, shops: Shop):
    user_loc = (float(latitude), float(longitude))
    shop_loc = (float(shops['latitude']), float(shops['longitude']))
    return haversine(user_loc, shop_loc, unit=Unit.KILOMETERS)

# Checking for shops contained by the radius provided by user
def filter_distance(user: User, shop_distance):
    if float(user['distance']) <= float(shop_distance):
        return True
    else:
        return False

# Nearby Shops List
class ShopsNearMeView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).values()
        radius = request.data['radius']
        shop_list = Shop.objects.all()
        serializer = ShopSerializer(shop_list, many=True)
        response_data = serializer.data
        # user's latitude and longitude
        user_lat, user_long = user[0]['latitude'], user[0]['longitude']
        if radius is not None:
            for shops in response_data:
                shops['distance'] = get_distance_between_user_and_shop(user_lat,user_long,shops)
                # storing all the jobs under the radius provided by the user
                shops_list_iterator = filter(lambda seq: filter_distance(user=seq, shop_distance=radius),
                                            response_data)
            resp_data = list(shops_list_iterator)
            # sorting the list on the basis of distance
            near_by_shops = sorted(resp_data, key=lambda d: d['distance'])
            return http_response(data=near_by_shops, message='List of nearby Shops', 
                                status_code=status.HTTP_200_OK)

class LocationView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        try:
            user = User.objects.get(user=request.user.id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User does not exists"})
        serializer = LocationSerializer(user, data=request.data)
        if not serializer.is_valid():
            raise ValidationError(
                {
                    'error_message': 'Please correct the following errors.',
                    'errors': serializer.errors,
                }
            )
        serializer.save()
        return http_response(data=serializer.data, message='Data Updated Sucessfully', 
                            status_code=status.HTTP_200_OK)
