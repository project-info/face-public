import cv2import cv2

from simple_facerec import SimpleFacerecfrom simple_facerec import SimpleFacerec

import numpy as npimport numpy as np

import jsonimport json

import platformimport platform

import osimport os



# Determine whether to use GUI# Determine whether to use GUI

USE_GUI = TrueUSE_GUI = True

if os.environ.get("FORCE_GUI", "") == "0":if os.environ.get("FORCE_GUI", "") == "0":
import cv2

from simple_facerec import SimpleFacerec

import numpy as np

import json

import platform

import os


# Determine whether to use GUI
USE_GUI = True
if os.environ.get("FORCE_GUI", "") == "0":
    USE_GUI = False
elif platform.system() == 'Darwin':
    mac_ver = platform.mac_ver()[0] or ""
    try:
        parts = mac_ver.split('.')
        if len(parts) >= 3:
            patch = int(parts[2])
            if int(parts[0]) == 14 and patch < 8:
                USE_GUI = False
    except Exception:
        USE_GUI = True


sfr = SimpleFacerec()
sfr.load_encoding_images("images/")


cap = cv2.VideoCapture(1)


with open('./signups.json', 'r') as f:
    data = json.load(f)



def capture_and_detect():
    frames = []
    all_distances = []
    all_names = []
    while len(frames) <= 10:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(sfr.detect_known_faces(frame))

    if not frames:
        return None, None, None

    for past_frame in frames:
        face_locations, face_names = past_frame
        if face_names:
            for possible_face in face_names[0]:
                all_distances.append(possible_face[1])
                all_names.append(possible_face[0])

    if not all_names:
        return None, None, None

    best_index = int(np.argmin(all_distances))
    # return name, distance, last frame for possible display
    return all_names[best_index], all_distances[best_index], frames[-1][0]

if USE_GUI:
    try:
        from PySide6 import QtWidgets, QtGui, QtCore
    except Exception as e:
        print("PySide6 not installed or failed to import:", e)
        print("Falling back to headless mode.")
        USE_GUI = False

if USE_GUI:
    class MainWindow(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Face Recognition (PySide6)')
            self.setGeometry(475, 300, 500, 150)
            self.layout = QtWidgets.QVBoxLayout(self)

            self.button = QtWidgets.QPushButton('Capture Face')
            self.button.clicked.connect(self.find_name)
            self.layout.addWidget(self.button)

            self.status = QtWidgets.QLabel('')
            self.layout.addWidget(self.status)

            self.show()

        def find_name(self):
            name, dist, locs = capture_and_detect()
            if name is None:
                self.status.setText('No face detected')
                return
            if name in data:
                self.status.setText(f'Already registered: {name}')
            else:
                self.status.setText(f'Register: {name}')
                # enable register button inline for simplicity
                ret = QtWidgets.QMessageBox.question(self, 'Register', f'Register {name}?')
                if ret == QtWidgets.QMessageBox.Yes:
                    data.append(name)
                    with open('./signups.json', 'w') as f:
                        json.dump(data, f)
                    self.status.setText(f'Registered: {name}')

    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.exec()
else:
    print('Running in headless mode (PySide6 GUI disabled). To enable GUI set FORCE_GUI=1 or upgrade macOS to 14.0.8+')
    name, dist, locs = capture_and_detect()
    if name is None:
        print('No face detected')
    else:
        print(f'Detected: {name} (distance {dist})')
        if name in data:
            print('Already registered')
        else:
            data.append(name)
            with open('./signups.json', 'w') as f:
                json.dump(data, f)
            print(f'Registered {name}')

cap.release()

            self.button.clicked.connect(self.find_name)            self.button.clicked.connect(self.find_name)

            self.layout.addWidget(self.button)            self.layout.addWidget(self.button)



            self.status = QtWidgets.QLabel('')            self.status = QtWidgets.QLabel('')

            self.layout.addWidget(self.status)            self.layout.addWidget(self.status)



            self.show()            self.show()



        def find_name(self):        def find_name(self):

            name, dist, locs = capture_and_detect()            name, dist, locs = capture_and_detect()

            if name is None:            if name is None:

                self.status.setText('No face detected')                self.status.setText('No face detected')

                return                return

            if name in data:            if name in data:

                self.status.setText(f'Already registered: {name}')                self.status.setText(f'Already registered: {name}')

            else:            else:

                self.status.setText(f'Register: {name}')                self.status.setText(f'Register: {name}')

                # enable register button inline for simplicity                # enable register button inline for simplicity

                ret = QtWidgets.QMessageBox.question(self, 'Register', f'Register {name}?')                ret = QtWidgets.QMessageBox.question(self, 'Register', f'Register {name}?')

                if ret == QtWidgets.QMessageBox.Yes:                if ret == QtWidgets.QMessageBox.Yes:

                    data.append(name)                    data.append(name)

                    with open('./signups.json', 'w') as f:                    with open('./signups.json', 'w') as f:

                        json.dump(data, f)                        json.dump(data, f)

                    self.status.setText(f'Registered: {name}')                    self.status.setText(f'Registered: {name}')



    app = QtWidgets.QApplication([])    app = QtWidgets.QApplication([])


    import cv2

    from simple_facerec import SimpleFacerec

    import numpy as np

    import json

    import platform

    import os


    # Determine whether to use GUI
    USE_GUI = True
    if os.environ.get("FORCE_GUI", "") == "0":
        USE_GUI = False
    elif platform.system() == 'Darwin':
        mac_ver = platform.mac_ver()[0] or ""
        try:
            parts = mac_ver.split('.')
            if len(parts) >= 3:
                patch = int(parts[2])
                if int(parts[0]) == 14 and patch < 8:
                    USE_GUI = False
        except Exception:
            USE_GUI = True


    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")


    cap = cv2.VideoCapture(1)


    with open('./signups.json', 'r') as f:
        data = json.load(f)



    def capture_and_detect():
        frames = []
        all_distances = []
        all_names = []
        while len(frames) <= 10:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(sfr.detect_known_faces(frame))

        if not frames:
            return None, None, None

        for past_frame in frames:
            face_locations, face_names = past_frame
            if face_names:
                for possible_face in face_names[0]:
                    all_distances.append(possible_face[1])
                    all_names.append(possible_face[0])

        if not all_names:
            return None, None, None

        best_index = int(np.argmin(all_distances))
        # return name, distance, last frame for possible display
        return all_names[best_index], all_distances[best_index], frames[-1][0]

    if USE_GUI:
        try:
            from PySide6 import QtWidgets, QtGui, QtCore
        except Exception as e:
            print("PySide6 not installed or failed to import:", e)
            print("Falling back to headless mode.")
            USE_GUI = False

    if USE_GUI:
        class MainWindow(QtWidgets.QWidget):
            def __init__(self):
                super().__init__()
                self.setWindowTitle('Face Recognition (PySide6)')
                self.setGeometry(475, 300, 500, 150)
                self.layout = QtWidgets.QVBoxLayout(self)

                self.button = QtWidgets.QPushButton('Capture Face')
                self.button.clicked.connect(self.find_name)
                self.layout.addWidget(self.button)

                self.status = QtWidgets.QLabel('')
                self.layout.addWidget(self.status)

                self.show()

            def find_name(self):
                name, dist, locs = capture_and_detect()
                if name is None:
                    self.status.setText('No face detected')
                    return
                if name in data:
                    self.status.setText(f'Already registered: {name}')
                else:
                    self.status.setText(f'Register: {name}')
                    # enable register button inline for simplicity
                    ret = QtWidgets.QMessageBox.question(self, 'Register', f'Register {name}?')
                    if ret == QtWidgets.QMessageBox.Yes:
                        data.append(name)
                        with open('./signups.json', 'w') as f:
                            json.dump(data, f)
                        self.status.setText(f'Registered: {name}')

        app = QtWidgets.QApplication([])
        window = MainWindow()
        app.exec()
    else:
        print('Running in headless mode (PySide6 GUI disabled). To enable GUI set FORCE_GUI=1 or upgrade macOS to 14.0.8+')
        name, dist, locs = capture_and_detect()
        if name is None:
            print('No face detected')
        else:
            print(f'Detected: {name} (distance {dist})')
            if name in data:
                print('Already registered')
            else:
                data.append(name)
                with open('./signups.json', 'w') as f:
                    json.dump(data, f)
                print(f'Registered {name}')

    cap.release()

