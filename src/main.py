from webcam_capture import capture_three_images
from feature_extractor import FeatureExtractor
from database import insert_features

TABLES = [
    "image1_features",
    "image2_features",
    "image3_features"
]

def main():
    images = capture_three_images()

    extractor = FeatureExtractor()

    for i, image in enumerate(images):
        mask = extractor.detect_blue(image)
        contour = extractor.extract_shape(mask)

        if contour is None:
            print(f"Aucune forme détectée pour l’image {i+1}")
            continue

        features = extractor.extract_features(contour, mask)
        insert_features(TABLES[i], features)

        print(f"Image {i+1} stockée dans {TABLES[i]}")

    print("\n✅ Programme terminé avec succès.")

if __name__ == "__main__":
    main()
