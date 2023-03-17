from django.urls import path
from shop.views import *

urlpatterns = (
    [
        path('shops/', ShopView.as_view(), name='shops'),
        path('shop_review/', ShopReviewView.as_view(), name='shop_review'),       
        path('shops_near_me/', ShopsNearMeView.as_view(), name='shops_near_me'),       
        path('location/', LocationView.as_view(), name='location'),       
    ]
)
