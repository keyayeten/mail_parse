from . import views
from django.urls import path

urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'api/register/',
        views.RegisterUserView.as_view(),
        name='register-user'
    ),
]
