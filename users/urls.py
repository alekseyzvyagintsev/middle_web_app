######################################################################################
from django.contrib.auth.views import LogoutView
from django.urls import path

from .apps import UsersConfig
from .views import CustomLoginView, ProfileDeleteView, ProfileDetailView, ProfileUpdateView, RegisterView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    # path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path("logout/", LogoutView.as_view(next_page="catalog:home"), name="logout"),
    path("accounts/profile/<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("accounts/profile/update/<int:pk>/", ProfileUpdateView.as_view(), name="profile_update"),
    path("accounts/profile/delete/<int:pk>/", ProfileDeleteView.as_view(), name="profile_delete"),
]

######################################################################################
