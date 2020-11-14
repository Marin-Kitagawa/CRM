from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('patient', PatientViewSet)
router.register('game', GameViewSet)
router.register('activity', ActivityViewSet)

urlpatterns = router.urls
