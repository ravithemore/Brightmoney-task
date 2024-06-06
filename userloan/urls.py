from django.urls import path
from . import views

'''from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("", views.UserViewSet)'''

urlpatterns = [
    path('apply-loan', views.LoanApplicationView.as_view()),
    path('make-payment', views.PaymentView.as_view()),
    path('get-statement', views.TransactionView.as_view()),
]