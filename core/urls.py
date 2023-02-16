from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  
from django.conf import settings
from django.conf.urls.static import static
from .forms import LoginForm


urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name= 'login.html',  authentication_form=LoginForm), name='login'),
    path('newitem/',views.newitem, name='newitem'),
    path('<int:pk>/',views.detail, name='detail'),
    path('<int:pk>/delete/',views.delete, name='delete'),
    path('<int:pk>/edititem/',views.edititem, name='edititem'),
    path('browse/', views.browse, name='browse'),
    path('inbox/', views.inbox, name='inbox'),
    path('cart/', views.cart, name='cart'),
    path('message/<int:pk>/', views.message, name='message'),
    path('addtocart/<int:pk>/', views.addtocart, name='addtocart'),
    path('new/<int:item_pk>/', views.new_message, name='new_message'),
    path('<str:pk>/remove/',views.remove, name='remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)