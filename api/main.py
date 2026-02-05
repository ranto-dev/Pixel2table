from fastapi import FastAPI
from pydantic import BaseModel
import base64, cv2, numpy as np
from fastapi.middleware.cors import CORSMiddleware

from feature_extractor import FeatureExtractor
from database import insert_features, fetch_all

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

extractor = FeatureExtractor()

TABLES = ["image1_features", "image2_features", "image3_features"]
capture_index = 0

class ImagePayload(BaseModel):
    image: str

@app.post("/capture")
def capture_image(payload: ImagePayload):
    global capture_index

    if capture_index >= 3:
        return {"done": True}

    img_data = base64.b64decode(payload.image.split(",")[1])
    img_array = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    mask = extractor.detect_blue(image)
    contour = extractor.extract_contour(mask)

    if contour is None:
        return {"error": "No shape detected"}

    features = extractor.extract_features(contour)
    insert_features(TABLES[capture_index], features)

    capture_index += 1
    return {"count": capture_index}

@app.get("/results")
def results():
    return {
        "image1": fetch_all("image1_features"),
        "image2": fetch_all("image2_features"),
        "image3": fetch_all("image3_features")
    }
