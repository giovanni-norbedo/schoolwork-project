from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('ask/', views.ask, name='ask'),
    path('reply/<int:ask_id>/', views.reply, name='reply'),
    path('bad/<int:reply_id>/', views.bad, name='bad'),
    path('adminwrite/<int:chat_id>/', views.adminwrite, name='adminwrite'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('solved/<int:bad_id>/', views.solved, name='solved'),
    path('earn/', views.earn, name='earn'),
    path('inbox/', views.inbox, name='inbox'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', views.home, name='home'),
    path('bads/', views.bads, name='bads'),
    path('contactus/', views.contactus, name='contactus'),
    path('write/', views.write, name='write'),
    path('chat/', views.chat, name='chat'),
    path('users/', views.users, name='users'),
    path('thanks/<int:reply_id>/', views.thanks, name='thanks'),
    path('refunds/', views.refunds, name='refunds'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)