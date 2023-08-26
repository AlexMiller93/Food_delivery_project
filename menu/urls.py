from django.urls import path
from menu import views

urlpatterns = [
    # path('menu', views.menu_list),
    # path('menu/<int:pk>', views.menu_detail),

    # CBV
    path('menu', views.MenuItemStaffList.as_view()),
    # path('menu', views.MenuItemList.as_view()),

    path('menu/<int:pk>', views.MenuItemDetail.as_view()),

]
