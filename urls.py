from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from . import views
import django.conf.urls

urlpatterns = [
    django.conf.urls.url(r'^home/$', views.home_view.as_view(), name='home_view'),
    django.conf.urls.url(r'^profile/$', views.user_profile_view.as_view(), name='user_profile_view'),
    django.conf.urls.url(r'^question_creation/$', views.question_creator_view.as_view(), name='question_creator_view'),
    django.conf.urls.url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    django.conf.urls.url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]


