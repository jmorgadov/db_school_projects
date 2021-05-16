from django.urls import path
from users import views as users_views

urlpatterns = [
    path('login/', users_views.login_view, name='login'),
    path('register/', users_views.register_view, name='register'),
    path('start/', users_views.start_view, name='start'),
]
