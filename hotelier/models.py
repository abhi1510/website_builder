import json

from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth import get_user_model


class Product(TimeStampedModel):
    content = models.TextField()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='product')

    def get_images(self):
        return self.images.all()

    def get_content(self):
        return json.loads(self.content)


def get_upload_path(instance, filename):
    return 'rooms/{}/{}'.format(instance.product.id, filename)


class Room(TimeStampedModel):
    content = models.TextField()
    image = models.ImageField(upload_to=get_upload_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rooms')

    def update_image_url(self):
        earlier = json.loads(self.content)
        earlier.update({'image_url': self.image.url})
        self.content = json.dumps(earlier)
        self.save()

    def get_content(self):
        return json.loads(self.content)


class ProductImages(TimeStampedModel):
    name = models.CharField(max_length=512)
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.name
