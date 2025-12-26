import face_recognition
import os

def verify_face(uploaded_image_path, known_image_path):
    try:
        uploaded_image = face_recognition.load_image_file(uploaded_image_path)
        uploaded_encoding = face_recognition.face_encodings(uploaded_image)[0]

        known_image = face_recognition.load_image_file(known_image_path)
        known_encoding = face_recognition.face_encodings(known_image)[0]

        # Compare faces
        results = face_recognition.compare_faces([known_encoding], uploaded_encoding)
        return results[0]
    except Exception as e:
        print("[ERROR] Face verification failed:", e)
        return False