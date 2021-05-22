from django.urls import path
from pages import views as pages_views

urlpatterns = [
    path('', pages_views.HomeView.as_view(), name='home'),
    path('players/', pages_views.PlayerSearchView.as_view(), name='players'),
    path('beasts/', pages_views.BeastSearchView.as_view(), name='beasts'),
    path('spells/', pages_views.SpellSearchView.as_view(), name='spells')
]
