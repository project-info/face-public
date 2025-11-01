import cv2
from simple_facerec import SimpleFacerec
import numpy as np

# Load face encodings
sfr = SimpleFacerec()
sfr.load_encoding_images("newImages/")

# Open camera (try 0, then 1)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap = cv2.VideoCapture(1)

window_name = "Top Five Matches"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

print("Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect known faces using the project's SimpleFacerec
    face_locations, face_names = sfr.detect_known_faces(frame)

    # face_names is expected as a list of lists per face, where each item is (name, distance)
    # We'll show top 5 (lowest distances)
    for (face_loc, possible_names) in zip(face_locations, face_names if face_names else []):
        # face_loc expected as [y1, x2, y2, x1]
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Sort possible names by distance and take top 5
        sorted_names = sorted(possible_names, key=lambda p: p[1])[:5]

        # Draw each name on the left of the face box
        for i, (name, distance) in enumerate(sorted_names):
            text = f"{i+1}. {name} ({distance:.4f})"
            text_pos = (x1, y1 - 10 - (20 * i))
            cv2.putText(frame, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
