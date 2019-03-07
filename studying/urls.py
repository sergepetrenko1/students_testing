from  django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('testing', views.TestingView)
router.register('match_task', views.MatchView)

urlpatterns = [
    path('', include(router.urls))
]