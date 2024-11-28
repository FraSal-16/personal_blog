from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index, name='index'), 
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'), 
    path('after_log_out/', views.after_log_out, name='after_log_out'),
    path('not_logged_in/', views.not_logged_in, name='not_logged_in'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('success/', views.success, name='success'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_confirm_delete'),
]