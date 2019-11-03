from django.urls import path
from . import views

urlpatterns = [
    #path('', views.classify, name='index')
    #path('<enter_text>/', views.classify, name='classify')
    path('', views.home, name='index'),
    path('predict/', views.predict, name='predict'),
    path('submit/', views.submit, name='submit'),
    path('success/', views.success, name='success'),
    
]


