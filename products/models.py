from django.db import models
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator


class Perfume(models.Model):
    # Basic Info
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    # Flags for Filtering
    weekly_offer = models.BooleanField(default=False)
    discounted = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    # Delivery
    delivery_location = models.CharField(max_length=200, default="Countrywide")

    DELIVERY_METHODS = [
        ('free', 'Free Delivery'),
        ('pickup', 'Pick Up Mtaani'),
        ('paid', 'Paid Delivery'),
    ]
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHODS, default='paid')
    payment_on_delivery = models.BooleanField(default=True)

    # Contact Info
    contact = models.CharField(max_length=100, help_text="WhatsApp contact or business name")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(default="your_email@example.com")

    # Social Links
    whatsapp_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    tiktok_link = models.URLField(blank=True, null=True)

    # Main Image
    photo = models.ImageField(upload_to='perfume_photos/', blank=True, null=True)
    @property
    def image(self):
        return self.photo

    def __str__(self):
        return self.name

    def main_image_preview(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" style="height:100px;" />')
        return "(No main photo)"
    main_image_preview.short_description = 'Main Image Preview'


class ProductImage(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='perfume_photos/')

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" style="object-fit: cover;" />')
        return "(No image)"
    image_preview.short_description = 'Preview'

    def __str__(self):
        return f"Image of {self.perfume.name}"


class Review(models.Model):
    perfume = models.ForeignKey(Perfume, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"


def image_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return None
