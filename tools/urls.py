from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('tools/', views.ToolsListView.as_view(), name='tools_list'),
    path('tool/<slug:slug>/', views.ToolDetailView.as_view(), name='tool_detail'),
    path('process/', views.process_text, name='process_text'),
] 