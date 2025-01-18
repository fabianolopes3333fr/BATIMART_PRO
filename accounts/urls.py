from django.urls import path
from .views import login_view, SignUpView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
# ... outras URLs ...
]