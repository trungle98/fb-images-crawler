import face_recognition
import os
image = face_recognition.load_image_file(f"523323900-0.jpg")
face_locations = face_recognition.face_locations(image)
if len(face_locations) == 0:
    os.remove(f"523323900-0.jpg")