from django.urls import path, include

from users import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('register/', views.Register.as_view(), name='register'),
    path('user_profile/<int:user_id>/', views.user_profile, name="user")
]
