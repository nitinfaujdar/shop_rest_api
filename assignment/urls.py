from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("shop/", include("shop.urls")),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('social_login/', SocialLoginView.as_view(), name="social_login"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
