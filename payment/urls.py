from django.urls import path
from .views import  payment_success, checkout, billing_info

urlpatterns = [
    path('payment_success/', payment_success, name='payment_success'),
    path('checkout/', checkout, name='checkout'),
    path('billing_info/', billing_info, name="billing_info"),
    # path('process_order/', process_order, name="process_order"),
    # path('shipped_dash/', shipped_dash, name="shipped_dash"),
    # path('not_shipped_dash/', not_shipped_dash, name="not_shipped_dash"),
   
]     