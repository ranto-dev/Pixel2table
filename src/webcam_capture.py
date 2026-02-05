import cv2

def capture_three_images():
    cap = cv2.VideoCapture(0)
    images = []
    count = 0

    print("Appuyez sur ESPACE pour capturer une image")
    print("Appuyez sur Q pour quitter")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        cv2.putText(
            display,
            f"Captures: {count}/3",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Pixel2Table - Webcam", display)
        key = cv2.waitKey(1) & 0xFF

        if key == 32:  # ESPACE
            images.append(frame.copy())
            count += 1
            print(f"Image {count} capturée")

        elif key == ord('q'):
            break

        if count == 3:
            break

    cap.release()
    cv2.destroyAllWindows()
    return images
