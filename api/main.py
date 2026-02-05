from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64, cv2, numpy as np

from feature_extractor import FeatureExtractor
from database import insert_features, fetch_all

app = FastAPI()
extractor = FeatureExtractor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TABLES = ["image1_features", "image2_features", "image3_features"]
capture_index = 0
max_captures = 3  # Peut être changé dynamiquement depuis l'UI

class ImagePayload(BaseModel):
    image: str

@app.post("/capture")
def capture_image(payload: ImagePayload):
    global capture_index

    if capture_index >= max_captures:
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
    return {"count": capture_index, "message": f"Image {capture_index} capturée !"}

@app.get("/results")
def results():
    data = {f"image{i+1}": fetch_all(f"image{i+1}_features") for i in range(3)}
    return data
