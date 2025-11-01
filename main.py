import cv2
from simple_facerec import SimpleFacerec
import numpy as np
import json
import tkinter as tk
from PIL import Image, ImageTk

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("newImages/")
root = tk.Tk()

# Load Camera

cap = cv2.VideoCapture(1)

root.title('Face Recognition')
root.bind('<Escape>', lambda e: root.quit()) 
root.geometry("500x150+475+300")

register = tk.StringVar()
name = ""
with open('./signups.json', 'r') as f:
    data = json.load(f)

def find_name():
    global data
    with open('./signups.json', 'r') as f:
        data = json.load(f)
    frames = []
    while len(frames) <= 10:
        ret, frame = cap.read()

        # Detect Faces
        all_distances = []
        all_names = []
        frames.append(sfr.detect_known_faces(frame))

        averaged_face_names = []

        for past_frame in frames:
            face_locations, face_names = past_frame
            if(face_names):
                for possible_face in face_names[0]:
                    all_distances.append(possible_face[1])
                    all_names.append(possible_face[0])
        
        single_face_names = []
        print(len(all_distances))
        for index in np.argsort(all_distances)[:5]:
            single_face_names.append((all_names[index], all_distances[index]))
        averaged_face_names.append(single_face_names)

        # averaged_face_names = frames[-1][1]

        face_locations = frames[-1][0]
        for face_loc, possible_names in zip(face_locations, averaged_face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            # for i, (name, distance) in enumerate(possible_names):
            #     cv2.putText(frame, f"{i + 1}. {name}; confidence {round(distance, 4)}", (x1, y1 - 150 + 30*i), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.putText(frame, f"Face Detected", (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Frame", cv2.WND_PROP_TOPMOST, 1)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()
    if not all_names:
        print("No face detected")
        register.set(f"No face detected")
        secondary.pack()
        secondary.configure(state='disabled')
        root.update()
    global name
    name = all_names[np.argmin(all_distances)]
    if name in data:
        print("Welcome back!")
        register.set(f"Already registered: {name}")
        secondary.pack()
        secondary.configure(state='disabled')
        root.update()
    else:
        register.set(f"Register: {name}")
        print(name)
        secondary.pack()
        secondary.configure(state='active')
        root.update()

button = tk.Button(root, text='Capture Face', command=find_name, width=25, pady=10)
button.pack()

def signup():
    data.append(name)
    print(name)
    with open('./signups.json', 'w') as f:
        json.dump(data, f)
    register.set(f"Registered: {name}")
    secondary.pack()
    secondary.configure(state='disabled')
    root.update()

secondary = tk.Button(root, textvariable=register, width=50, pady=25, command=signup)

root.attributes('-topmost', True)
root.mainloop()

cap.release()