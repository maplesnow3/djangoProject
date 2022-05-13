from django.urls import path
from Backend.views import user_views
from Backend.views import injury_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# API list
urlpatterns = [
    # Login api
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # User related functions
    path('user/register', user_views.registerUser, name='register'),
    path('user/profile', user_views.getUserProfile, name='users'),
    path('user/<str:pk>', user_views.getUserById, name='routes'),
    path('user/delete/<str:pk>', user_views.deleteUser, name='delete'),
    # injury form functions
    path('newinjuryform', injury_views.newInjury, name='new_form'),
    path('injuryforms/<str:pk>', injury_views.injurys, name='form_by_id'),
    path('injuryform/<str:pk>/<str:start>/<str:finish>', injury_views.injuryByTimeID, name='form_by_id_time'),
    path('concussionform', injury_views.newConcussion, name='new_form'),
    # Team functions, under development
]
