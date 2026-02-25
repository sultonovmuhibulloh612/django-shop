from django.urls import path
from . import views


app_name  = 'like_and_rating'

urlpatterns = [
    path('product/<int:id>/like/', views.add_like, name='add_like'),
    path('product/<int:product_id>/review/', views.add_or_edit_review, name='add_or_edit_review'),
    path('product/<int:product_id>/review/delete_review', views.delete_review, name='delete_review'),
    path("product/<int:product_id>/reviews/", views.product_reviews, name="product_reviews"),
    
]