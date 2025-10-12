from pathlib import Path
import cv2


def convert_to_sketch(input_path: str, output_dir: str | None = None, suffix: str = '_sketch', method: str = 'laplacian') -> str:
    """Convert an image to a pencil-sketch-like image using OpenCV.

    Steps implemented:
    1. Read the image using cv2.imread.
    2. Convert it to grayscale.
    3. Invert the grayscale image.
    4. Apply Gaussian blur.
    5. Invert the blurred image.
    6. Create a pencil sketch using cv2.divide(gray, inverted_blur, scale=256.0).
    7. Save the output image and return its path.

    Args:
        input_path: Path to the input image file.
        output_dir: Optional directory to write the output. If None, writes next to input file in a
            `sketches` subdirectory.
        suffix: Suffix to append before the file extension for the output filename.

    Returns:
        Absolute path to the saved sketch image.
    """

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Determine output directory
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = input_path.parent / 'sketches'
    out_dir.mkdir(parents=True, exist_ok=True)

    # Read image
    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Failed to read image or unsupported format: {input_path}")

    # Use the Laplacian-based sketch function below
    from . import utils as _utils  # local import to reference sketch_image
    sketch = _utils.sketch_image(img, show=False)

    # Create output filename
    out_name = input_path.stem + suffix + input_path.suffix
    out_path = out_dir / out_name

    # Save result
    success = cv2.imwrite(str(out_path), sketch)
    if not success:
        raise IOError(f"Failed to write sketch image to: {out_path}")

    return str(out_path.resolve())


def sketch_image(img, show: bool = False):
    """Apply the Laplacian filter + threshold to create a sketch.

    This implements the exact filter you requested. `show=True` will try to
    display the intermediate and final images with `cv2.imshow` but is
    guarded so it won't crash on headless servers.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.medianBlur(img_gray, 5)
    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=5)

    if show:
        try:
            cv2.imshow('Thats it', edges)
        except Exception:
            pass

    ret, threshold = cv2.threshold(edges, 80, 255, cv2.THRESH_BINARY)

    if show:
        try:
            print(ret)
            cv2.imshow('Again', threshold)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception:
            pass

    return threshold
