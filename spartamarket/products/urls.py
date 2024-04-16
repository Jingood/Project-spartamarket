from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
	path('', views.products, name="products"),
	path('create/', views.create, name="create"),
	path('<int:pk>/', views.product_detail, name='product_detail'),
	path('<int:pk>/update/', views.product_update, name='product_update'),
	path('<int:pk>/delete/', views.product_delete, name='product_delete'),
	path('<int:pk>/like/', views.like, name='like'),
]