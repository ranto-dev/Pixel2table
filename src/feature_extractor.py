import cv2
import numpy as np

class FeatureExtractor:

    def detect_blue(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        return cv2.inRange(hsv, lower_blue, upper_blue)

    def extract_shape(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        return max(contours, key=cv2.contourArea)

    def extract_features(self, contour, mask):
        moments = cv2.moments(contour)
        hu = cv2.HuMoments(moments)
        hu = -np.sign(hu) * np.log10(np.abs(hu) + 1e-10)

        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)

        hull = cv2.convexHull(contour)
        solidity = area / cv2.contourArea(hull)

        circularity = 4 * np.pi * area / (perimeter ** 2)

        hist = cv2.calcHist([mask], [0], None, [8], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        return {
            "area": area,
            "perimeter": perimeter,
            "aspect_ratio": w / h,
            "solidity": solidity,
            "circularity": circularity,
            "orientation": 0.0,
            "hu_moments": hu.flatten(),
            "histogram": hist
        }
