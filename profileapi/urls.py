from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewset)
router.register('login', views.LoginViewSet, base_name='login ' )
router.register('feed', views.ProfileFeedItemViewSet)

urlpatterns =[
    path('helloapiview/', views.HelloApiView.as_view(), name='helloapiview'),
    path('', include(router.urls)),
]