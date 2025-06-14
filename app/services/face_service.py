import face_recognition
import numpy as np
import os
from typing import Dict, List
import cv2

class FaceService:
    def __init__(self, face_dir: str = "faces"):
        self.face_dir = face_dir
        self.know_faces: List[np.ndarray] = []
        self.know_names: List[str] = []
        self.reload_faces()

    def reload_faces(self):
        self.know_faces.clear()
        self.know_names.clear()
        for name in os.listdir(self.face_dir):
            person_dir = os.path.join(self.face_dir, name)
            for file in os.listdir(person_dir):
                path = os.path.join(person_dir, file)
                image = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.know_faces.append(encodings[0])
                    self.know_names.append(name)

    def recognize_face(self, image_bytes: bytes) -> Dict:
        npimg = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            return {"recognized": False, "reason": "no_face"}
        
        for encoding in encodings:
            matches = face_recognition.compare_faces(self.know_faces, encoding)
            if True in matches:
                idx = matches.index(True)
                return {"recognized": True, "name": self.know_names[idx]}
            
        return {"recognized": False, "reason": "unknown"}