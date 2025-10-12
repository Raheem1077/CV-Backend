from django.contrib import admin
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'original_image', 'sketch_image', 'created_at')
	readonly_fields = ('created_at',)
