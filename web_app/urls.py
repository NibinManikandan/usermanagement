from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),

    path('signup/', views.signup, name='signup'),

    path('admin_log/', views.admin_log, name = 'admin_log'),
    path('admin_page/',views.admin_page, name ='base'),
    path('search/', views.search, name = 'search'),
    path('logout/', views.logoutt, name = 'logout'),
    path('Add/', views.Add, name='Add'),
    path('Edit/', views.Edit, name = 'Edit'),
    path('Update/<str:id>', views.Update, name = 'Update'),
    path('delete/<str:id>', views.delete, name = 'delete'),

    path('main/', views.main, name = 'main'),
    path('user_page/', views.user_page, name='user_page'),
]