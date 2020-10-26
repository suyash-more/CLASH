from django.urls import path
from . import views


urlpatterns = [
    path('',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('success/',views.success,name='success'),
    path('logout/',views.userlogout,name='logout'),
    path('result/', views.success, name='result'),
    path('getrequest/',views.check,name='check'),
    path('emglogin/',views.emglogin,name='emglogin'),
    path('spincheck/',views.checkspin, name='spincheck'),
    path('getassured/',views.getassured,name='getassured'),
    path('visionise/',views.visionise,name='visionise'),
    path('get_p_score/',views.get_p_score,name='get_p_score')
]