import os
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import convert_to_sketch


def home(request):
	return HttpResponse('<h1>Sketcher app is running</h1>')


@csrf_exempt
def sketch_image(request):
	"""Accept a multipart/form-data POST with key 'image', save it, run sketch conversion,
	and return JSON with the sketch URL.
	"""
	if request.method != 'POST':
		return JsonResponse({'error': 'POST required'}, status=405)

	image_file = request.FILES.get('image')
	if not image_file:
		return JsonResponse({'error': 'No image uploaded'}, status=400)

	# Save original to MEDIA_ROOT/uploads/
	saved_rel_path = default_storage.save(f'uploads/{image_file.name}', image_file)
	image_full_path = os.path.join(str(settings.MEDIA_ROOT), saved_rel_path)

	# Ensure output directory exists
	sketches_dir = os.path.join(str(settings.MEDIA_ROOT), 'sketches')
	os.makedirs(sketches_dir, exist_ok=True)

	# Convert to sketch (returns absolute path)
	try:
		sketch_abs = convert_to_sketch(image_full_path, output_dir=sketches_dir)
	except Exception as e:
		return JsonResponse({'error': f'Processing failed: {e}'}, status=500)

	# Build URL relative to MEDIA_URL
	rel_path = os.path.relpath(sketch_abs, start=str(settings.MEDIA_ROOT)).replace('\\', '/')
	sketch_url = request.build_absolute_uri(settings.MEDIA_URL + rel_path)

	return JsonResponse({'sketch_url': sketch_url})


def list_images(request):
	"""Return JSON lists of available uploaded and sketched images."""
	if request.method != 'GET':
		return JsonResponse({'error': 'GET required'}, status=405)

	media_root = Path(settings.MEDIA_ROOT)
	uploads_dir = media_root / 'uploads'
	sketches_dir = media_root / 'sketches'
	allowed_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

	def _gather(directory: Path):
		files = []
		if directory.exists():
			for file_path in sorted(directory.iterdir(), reverse=True):
				if file_path.is_file() and file_path.suffix.lower() in allowed_exts:
					rel = file_path.relative_to(media_root).as_posix()
					files.append({
						'filename': file_path.name,
						'url': request.build_absolute_uri(settings.MEDIA_URL + rel),
					})
		return files

	return JsonResponse({
		'uploads': _gather(uploads_dir),
		'sketches': _gather(sketches_dir),
	})
