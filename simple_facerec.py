import face_recognition
import cv2
import os
import glob
import numpy as np
import pickle
import json

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

        # @Kevin play with this to get the better results?

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding

            # Write to dump

            # img_encoding = face_recognition.face_encodings(rgb_img)[0]
            # with open("./newPickle/" + filename + ".pkl", 'w+b') as file:
            #     pickle.dump(img_encoding, file)

            # Read from dump

            with open("./newPickle/" + filename + ".pkl", 'rb') as file:
                img_encoding = pickle.load(file)

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
            print(img_path)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            possible_names = []

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            sorted_face_distance_indices = np.argsort(face_distances)

            for best_face_distance_index in sorted_face_distance_indices[:5]:
                if (matches[best_face_distance_index]):
                    possible_names.append((self.known_face_names[best_face_distance_index], face_distances[best_face_distance_index]))

            face_names.append(possible_names)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names

    def comparisons(self):
        comparisons = []
        for i1, face1 in enumerate(self.known_face_encodings):
            self_name = self.known_face_names[i1]
            distances = face_recognition.face_distance(self.known_face_encodings, face1)
            best_index = np.argsort(distances)[1]
            best_name = self.known_face_names[best_index]
            comparisons.append({"self": self_name, "match": best_name, "distance": distances[best_index]})

        comparisons.sort(key=lambda x: x["distance"])
            
        # print(face_recognition.face_distance(self.known_face_encodings, self.known_face_encodings[self.known_face_names.index("Daphne Huang '25")])[self.known_face_names.index("Peggy Huang '27")])
        # print(face_recognition.face_distance(self.known_face_encodings, self.known_face_encodings[self.known_face_names.index("Daphne Huang '25")])[self.known_face_names.index("Julie Yan '26")])
        return comparisons

    def contrasts(self):
        contrasts = []
        for i1, face1 in enumerate(self.known_face_encodings):
            self_name = self.known_face_names[i1]
            distances = face_recognition.face_distance(self.known_face_encodings, face1)
            best_index = np.argsort(distances)[-1]
            best_name = self.known_face_names[best_index]
            contrasts.append({"self": self_name, "match": best_name, "distance": distances[best_index]})

        contrasts.sort(key=lambda x: x["distance"])
            
        # print(face_recognition.face_distance(self.known_face_encodings, self.known_face_encodings[self.known_face_names.index("Daphne Huang '25")])[self.known_face_names.index("Peggy Huang '27")])
        # print(face_recognition.face_distance(self.known_face_encodings, self.known_face_encodings[self.known_face_names.index("Daphne Huang '25")])[self.known_face_names.index("Julie Yan '26")])
        return contrasts
    
    def compare_face(self, face1, face2):
        distances = face_recognition.face_distance(self.known_face_encodings, self.known_face_encodings[self.known_face_names.index(face2)])
        index = self.known_face_names.index(face1)            
        return distances[index]
