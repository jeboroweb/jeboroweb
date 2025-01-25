from django.urls import path
from .views import CalendarioPageView, HomePageView, SamplePageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('calendario/', CalendarioPageView.as_view(), name="calendario"),
    path('sample/', SamplePageView.as_view(), name="sample"),
]
