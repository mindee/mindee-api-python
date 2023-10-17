"""
An example using OpenCV to display the cropping data returned by Mindee's API.

Note that this example only works for images.

You'll need to ``pip install opencv-python`` in addition to the mindee library.

Run as follows from project root::

  python examples/display_cropping.py
"""

from typing import List, Tuple

import cv2
import numpy as np

from mindee import Client, product
from mindee.parsing.common.predict_response import PredictResponse


def relative_to_pixel_pos(polygon, image_h: int, image_w: int) -> List[Tuple[int, int]]:
    """Convert from Mindee's relative format to an absolute pixel format as used by OpenCV."""
    return [(int(point[0] * image_w), int(point[1] * image_h)) for point in polygon]


def show_image_crops(file_path: str, cropping: list):
    """Display cropping results on an image."""
    image = cv2.imread(file_path)
    height = image.shape[0]
    width = image.shape[1]

    img = None
    for crop in cropping:
        to_display = [
            {"shape": crop.polygon, "color": (0, 0, 128), "thickness": 1},
            {"shape": crop.quadrangle, "color": (0, 128, 0), "thickness": 1},
            {"shape": crop.rectangle, "color": (128, 0, 0), "thickness": 1},
            {"shape": crop.bounding_box, "color": (255, 0, 0), "thickness": 2},
        ]
        for item in to_display:
            abs_polygon = relative_to_pixel_pos(item["shape"], height, width)
            # convert the pixel positions to a 3D numpy array
            polygon_points = np.array([abs_polygon], np.int32)
            img = cv2.polylines(
                image, polygon_points, True, item["color"], item["thickness"]
            )
    if img is None:
        raise RuntimeError("Not able to set the polygons")

    # resize the image as needed by changing the fx, fy values
    img_half = cv2.resize(img, (0, 0), fx=0.9, fy=0.9)

    cv2.imshow(file_path, img_half)
    cv2.moveWindow(file_path, 10, 10)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = "./tests/data/fr/id_card/cni-rectoverso.jpg"

    # We'll get the API key from the environment
    mindee_client = Client()

    # Load a file from disk
    input_doc = mindee_client.source_from_path(image_path)

    # Parse the document by passing the appropriate type
    api_response: PredictResponse = mindee_client.parse(product.CropperV1, input_doc)

    # Display
    show_image_crops(image_path, api_response.document.inference.pages[0].cropping)
