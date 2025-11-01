import cv2
from simple_facerec import SimpleFacerec
import numpy as np

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("newImages/")

# Load Camera
cap = cv2.VideoCapture(1)
frames = []


while True:
    ret, frame = cap.read()

    # Detect Faces
    frames.append(sfr.detect_known_faces(frame))
    frames = frames[-60:]

    all_distances = []
    all_names = []

    averaged_face_names = frames[-1][1]

    face_locations = frames[-1][0]
    for face_loc, possible_names in zip(face_locations, averaged_face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        print(averaged_face_names)

        # for i, (name, distance) in enumerate(possible_names):
        #     cv2.putText(frame, f"{i + 1}. {name}; confidence {round(distance, 4)}", (x1, y1 - 150 + 30*i), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        for i, (name, distance) in enumerate(possible_names):
            cv2.putText(frame, f"{i + 1}. {name}; confidence {round(distance, 4)}", (x1, y1 - 150 + 30*i), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()