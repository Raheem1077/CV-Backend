from django.db import models


class UploadedImage(models.Model):
	"""Model to store uploaded images and their sketches."""
	original_image = models.ImageField(upload_to='uploads/')
	sketch_image = models.ImageField(upload_to='sketches/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"UploadedImage {self.pk} - {self.created_at.isoformat()}"
