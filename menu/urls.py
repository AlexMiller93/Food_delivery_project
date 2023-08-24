from django.urls import path
from menu import views


urlpatterns = [
    path('menu', views.menu_list),
    path('menu/<int:pk>', views.menu_detail),
]
