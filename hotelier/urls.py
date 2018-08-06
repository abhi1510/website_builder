from django.urls import path

from .views import (
    index,
    choose_template,
    create_product,
    rooms,
    room_detail,
    create_room,
    create_product_image,
    set_payments,
)

urlpatterns = [
    path('', index, name='home'),
    path('choose_template', choose_template, name='choose_template'),
    path('create_product', create_product, name='create_product'),
    path('rooms', rooms, name='rooms'),
    path('room_detail/<int:id>', room_detail, name='room_detail'),

    path('create_room', create_room, name='create_room'),
    path('set_payments', set_payments, name='set_payments'),
    path('create_product_image', create_product_image, name='create_product_image'),
]
