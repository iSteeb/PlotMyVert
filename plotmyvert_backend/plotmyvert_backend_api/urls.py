from django.urls import path, include

from . import views

urlpatterns = [
    path('getNewSessionsFromEmail/', views.getNewSessionsFromEmail, name='getNewSessionsFromEmail'),
    path('signup/', views.signup, name='signup'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('setCsrfCookie/', views.setCsrfCookie, name='setCsrfCookie'),
    path('userLogin/', views.userLogin, name='userLogout'),
    path('checkLoginStatus/', views.checkLoginStatus, name='checkLoginStatus'),
    path('configure/', views.configure, name='configure'),
    path('getAllSessions/', views.getAllSessions, name='getAllSessions'),
    path('getJumpsFromSession/', views.getJumpsFromSession, name='getJumpsFromSession'),
]