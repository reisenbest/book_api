from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)