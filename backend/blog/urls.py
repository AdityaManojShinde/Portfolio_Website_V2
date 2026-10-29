from rest_framework.routers import DefaultRouter
from blog.views import BlogViewSet

router = DefaultRouter()
router.register("blogs", BlogViewSet, basename="blog")

urlpatterns = router.urls