import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Product, Room, ProductImages


def index(request):
    return render(request, 'hotelier/index.html')


def choose_template(request):
    return render(request, 'hotelier/choose_template.html')


def create_product_content(data):
    return json.dumps({
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'address': {
            'street': data.get('street'),
            'city': data.get('city'),
            'state': data.get('state'),
            'country': data.get('country'),
            'zipcode': data.get('zipcode'),
        },
        'contact_desc': data.get('contact_desc'),
        'about': data.get('about')
    })


@login_required(login_url='/admin/login')
def create_product(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    try:
        product = json.loads(user.product.content)
    except:
        product = {}
    context.update({'data': product})
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        try:
            data = request.POST
            if product:
                prod = Product.objects.get(id=user.product.id)
                prod.content = create_product_content(data)
                prod.save()
            else:
                Product(content=create_product_content(data), user=user).save()
            context.update({'res': 'Successfully saved!!!'})
        except Exception as e:
            context.update({'error': e})
    return render(request, 'hotelier/create_product.html', context)


@login_required(login_url='/admin/login')
def create_product_image(request):
    pass


def create_room_content(data):
    return json.dumps({
        'name': data.get('name'),
        'description': data.get('description'),
        'size': data.get('size'),
        'bed': {
            'type': data.get('bed_type'),
            'count': data.get('bed_count'),
        },
        'price': {
            'type': data.get('rate_type'),
            'weekend': data.get('weekend_price'),
            'weekday': data.get('weekday_price')
        },
        'amenities': data.getlist('amenities[]')
    })


@login_required(login_url='/admin/login/')
def rooms(request):
    all_rooms = request.user.product.rooms.all()
    amenities = [
        {'name': 'Air Conditioning', 'value': 'ac', 'icon': ''},
        {'name': 'Internet (Wi-Fi)', 'value': 'wifi', 'icon': ''},
        {'name': 'TV', 'value': 'tv', 'icon': ''},
        {'name': 'Safe', 'value': 'safe', 'icon': ''},
        {'name': 'Minibar', 'value': 'minibar', 'icon': ''},
        {'name': 'Shower', 'value': 'shower', 'icon': ''},
        {'name': 'Telephone', 'value': 'telephone', 'icon': ''},
        {'name': 'Bath', 'value': 'bath', 'icon': ''},
        {'name': 'Kitchen', 'value': 'kitchen', 'icon': ''},
        {'name': 'Work Space', 'value': 'work', 'icon': ''},
        {'name': 'Towels', 'value': 'towels', 'icon': ''},
        {'name': 'Smoking Allowed', 'value': 'smoking', 'icon': ''}
    ]
    context = {'rooms': all_rooms, 'amenities': amenities}
    if request.method == 'POST':
        room = Room()
        room.product = request.user.product
        room.image = request.FILES.get('photo')
        room.content = create_room_content(request.POST)
        room.save()
        room.update_image_url()
    return render(request, 'hotelier/rooms.html', context)


@login_required(login_url='/admin/login/')
def room_detail(request, id):
    room = Room.objects.get(id=id)
    amenities = [
        {'name': 'Air Conditioning', 'value': 'ac', 'icon': ''},
        {'name': 'Internet (Wi-Fi)', 'value': 'wifi', 'icon': ''},
        {'name': 'TV', 'value': 'tv', 'icon': ''},
        {'name': 'Safe', 'value': 'safe', 'icon': ''},
        {'name': 'Minibar', 'value': 'minibar', 'icon': ''},
        {'name': 'Shower', 'value': 'shower', 'icon': ''},
        {'name': 'Telephone', 'value': 'telephone', 'icon': ''},
        {'name': 'Bath', 'value': 'bath', 'icon': ''},
        {'name': 'Kitchen', 'value': 'kitchen', 'icon': ''},
        {'name': 'Work Space', 'value': 'work', 'icon': ''},
        {'name': 'Towels', 'value': 'towels', 'icon': ''},
        {'name': 'Smoking Allowed', 'value': 'smoking', 'icon': ''}
    ]
    context = {'room': room, 'amenities': amenities}
    if request.method == 'POST':
        room.content = create_room_content(request.POST)
        room.save()
        room.update_image_url()
        return redirect('/hotelier/rooms')
    return render(request, 'hotelier/room_detail.html', context)


@login_required(login_url='/admin/login/')
def create_room(request):
    context = {}
    rooms = request.user.product.rooms.all()
    room = rooms.first()
    amenities = [
        {'name': 'Air Conditioning', 'value': 'ac', 'icon': ''},
        {'name': 'Internet (Wi-Fi)', 'value': 'wifi', 'icon': ''},
        {'name': 'TV', 'value': 'tv', 'icon': ''},
        {'name': 'Safe', 'value': 'safe', 'icon': ''},
        {'name': 'Minibar', 'value': 'minibar', 'icon': ''},
        {'name': 'Shower', 'value': 'shower', 'icon': ''},
        {'name': 'Telephone', 'value': 'telephone', 'icon': ''},
        {'name': 'Bath', 'value': 'bath', 'icon': ''},
        {'name': 'Kitchen', 'value': 'kitchen', 'icon': ''},
        {'name': 'Work Space', 'value': 'work', 'icon': ''},
        {'name': 'Towels', 'value': 'towels', 'icon': ''},
        {'name': 'Smoking Allowed', 'value': 'smoking', 'icon': ''}
    ]
    if room:
        context.update({'data': json.loads(room.content)})
        room.update_image_url()
    if request.method == 'POST':
        room = Room()
        room.product = request.user.product
        room.image = request.FILES.get('photo')
        room.content = create_room_content(request.POST)
        room.save()
    context.update({'amenities': amenities, 'rooms': rooms})
    return render(request, 'hotelier/create_room.html', context)


@login_required(login_url='/admin/login')
def set_payments(request):
    return render(request, 'hotelier/set_payments.html')
