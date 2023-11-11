#from import about as about
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from . import views
from django.contrib import admin
from .views import validate_username
from django.contrib.auth.views import LoginView

from .views import *

urlpatterns = [
    path('', ApplicationListView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', views.registration, name='registration'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('validate_username', validate_username, name='validate_username'),
    path('logout/', BBLogoutView.as_view(), name='logout'),
    path('profil/', ApplicationsByUserListView.as_view(), name='profil'),

    path('request/', views.ApplicationCreate.as_view(), name='request'),
    path('create/', views.MyPostListViews.as_view(), name='create'),
    path('delete/', views.ApplicationDelete.as_view(), name='delete'),


    path('superadmin/', views.ApplicationListViewAdmin.as_view(), name='superadmin'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),
    path('create_category/', views.CategoryCreate.as_view(), name='create_category'),
    path('change/<int:pk>/status/', views.ChangeStatusRequest.as_view(), name='change_status'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


