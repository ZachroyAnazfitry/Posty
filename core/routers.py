from rest_framework import routers
from core.user.viewsets import UserViewSet

router = routers.SimpleRouter()
# prefix and view arguments in register() method
router.register(r'user', UserViewSet, basename='user')
urlpatterns = routers.urls
# urlpatterns = [
#     path('', router.urls),
# ]