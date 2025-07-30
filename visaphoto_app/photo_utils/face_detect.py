import face_recognition
from PIL import Image

def detect_face(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        raise Exception("No face detected.")

    # On prend le premier visage détecté
    top, right, bottom, left = face_locations[0]
    return (left, top, right, bottom)
