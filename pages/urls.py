from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.Main, name='main'),
    path('chat/', views.Chat, name='chat'),
    path('chat/saveChatlog', views.makeContract, name='makeContract'),
    path('chat/resetMessages', views.resetMessages, name='resetMessages'),
    path('history/', views.History, name='history'),
    path('history/<int:pk>/', views.Detail, name='detail'),
    path('about/', views.About, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)