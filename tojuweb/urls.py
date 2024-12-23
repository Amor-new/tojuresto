from django.urls import path
from .views import order,index,product
from django.conf import settings
from django.conf.urls.static import static



# from .views import 

urlpatterns = [
    path('', index, name='index'),
    path('order/', order, name='order'),
    path('product/<int:pk>', product, name='product'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)