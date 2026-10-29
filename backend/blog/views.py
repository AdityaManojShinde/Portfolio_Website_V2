from blog.models import Blog
from rest_framework.viewsets import ModelViewSet
from blog.serializers import BlogSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(status="published")

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        
        return [IsAuthenticated()]