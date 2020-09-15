from django.urls import path
from .views import HomeView, EncryptView, VerifyView, DecryptView, SuccessView

app_name = "secretapp"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path("encrypt/", EncryptView.as_view(), name="encrypt"),
    path("verify/", VerifyView.as_view(), name="verify"),
    path('decrypt/', DecryptView.as_view(), name="decrypt"),
    path('decryption-successfull/', SuccessView.as_view(), name="success")
]