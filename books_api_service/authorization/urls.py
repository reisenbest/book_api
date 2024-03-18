from django.urls import path, include
from .views import RegisterView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('registeruser/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    #стандантрная рест-фрейворковская авторизация через сессии, логин стандартный, логаут переопределн
    path('auth/', include('rest_framework.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
