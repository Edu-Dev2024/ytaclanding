from django.urls import path
from django.conf import settings
from . import views
from . import views_landing
from django.conf.urls.static import static

urlpatterns = [
    path('', views.default_landing_view, name='default_landing'),
    path('home', views_landing.landing_home, name='landing_home'),
    path('YTAC', views_landing.landing_ytac, name='landing_ytac'),
    path('IITC', views_landing.landing_iitc, name='landing_iitc'),
    path('ICIA', views_landing.landing_icia, name='landing_icia'),
]