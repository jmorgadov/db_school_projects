from django.urls import path
from pages import views as pages_views

urlpatterns = [
    path('', pages_views.HomeView.as_view(), name='home'),
    path('players/', pages_views.PlayerSearchView.as_view(), name='players'),
    path('beasts/', pages_views.beast_search_view, name='beasts')
]
