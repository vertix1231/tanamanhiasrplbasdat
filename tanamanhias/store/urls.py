from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.store,name='store'),
    url(r'^carts/$',views.cart,name='cart'),
    url(r'^cekot/$',views.checkout,name='checkout'),
    # url(r'^process_order/$',views.processOrder,name='process_order'),
    
]
