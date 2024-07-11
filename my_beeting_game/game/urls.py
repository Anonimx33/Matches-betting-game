from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('game/accounts/', include('django.contrib.auth.urls')),
    path('game/register/', views.register, name='register'),
    path('game/', views.game, name='game'),
    path('game/details/<int:id>', views.details, name='details')
]
