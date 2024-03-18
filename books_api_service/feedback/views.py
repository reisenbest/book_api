from rest_framework.permissions import IsAuthenticated

from .paginations import FeedbackPagination
from rest_framework import viewsets
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by('id')
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FeedbackPagination
