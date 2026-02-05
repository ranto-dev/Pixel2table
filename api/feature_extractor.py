import cv2
import numpy as np

class FeatureExtractor:

    def detect_blue(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([90, 50, 50])
        upper = np.array([130, 255, 255])
        return cv2.inRange(hsv, lower, upper)

    def extract_contour(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return max(contours, key=cv2.contourArea) if contours else None

    def extract_features(self, contour):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)

        hull = cv2.convexHull(contour)
        solidity = area / cv2.contourArea(hull)

        circularity = 4 * np.pi * area / (perimeter ** 2)

        hu = cv2.HuMoments(cv2.moments(contour))
        hu = -np.sign(hu) * np.log10(np.abs(hu) + 1e-10)

        return {
            "area": area,
            "perimeter": perimeter,
            "aspect_ratio": w / h,
            "solidity": solidity,
            "circularity": circularity,
            "hu_moments": hu.flatten()
        }
