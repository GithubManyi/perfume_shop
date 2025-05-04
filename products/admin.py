from django.contrib import admin
from django.utils.html import format_html
from .models import Perfume, ProductImage

# Inline for additional product images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']
    verbose_name = "Additional Image"
    verbose_name_plural = "Additional Images"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

# Perfume Admin Configuration
@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'weekly_offer', 'new_arrival', 'discounted', 'main_image_preview']
    list_filter = ['is_available', 'weekly_offer', 'new_arrival', 'discounted']
    search_fields = ['name', 'description']
    ordering = ['-id']
    inlines = [ProductImageInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'photo', 'main_image_preview')
        }),
        ('Availability & Offers', {
            'fields': ('is_available', 'weekly_offer', 'new_arrival', 'discounted')
        }),
        ('Delivery & Payment', {
            'fields': ('delivery_method', 'delivery_location', 'payment_on_delivery')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'instagram_link', 'tiktok_link')
        }),
    )

    readonly_fields = ['main_image_preview']

    def main_image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 100px;" />', obj.photo.url)
        return "-"
    main_image_preview.short_description = 'Main Image Preview'

# Register additional product images
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['perfume', 'image_preview']
    readonly_fields = ['image_preview']
    search_fields = ['perfume__name']
    ordering = ['perfume__name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;" />', obj.image.url)
        return "-"
