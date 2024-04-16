from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
	path('<int:user_id>/profile/', views.profile, name='profile'),
	path('<int:user_id>/follow/', views.follow, name='follow'),
]