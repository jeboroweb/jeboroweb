from django.urls import path
from .views import PageListView, PageDetailView


pages_patterns = ([
    path('', PageListView.as_view(), name='pages'),
    path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),

], 'pages')