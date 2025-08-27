import cv2
import numpy as np
import os
from deepface import DeepFace
from PIL import Image

WHITELIST_DIR = "whitelist"

def get_face_embeddings():
    """Load whitelist images and generate their embeddings."""
    embeddings = []
    for img_file in os.listdir(WHITELIST_DIR):
        img_path = os.path.join(WHITELIST_DIR, img_file)
        try:
            embedding = DeepFace.represent(img_path=img_path, model_name="VGG-Face")[0]["embedding"]
            embeddings.append((img_file, embedding))
        except Exception as e:
            print(f"Failed to process {img_file}: {e}")
    return embeddings

def is_face_whitelisted(face_img, whitelist_embeddings, threshold=0.5):
    """Check if detected face matches any in the whitelist."""
    try:
        # Convert OpenCV image (BGR) to RGB for DeepFace
        if len(face_img.shape) == 3 and face_img.shape[2] == 3:
            face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        else:
            face_img_rgb = face_img
        face_embedding = DeepFace.represent(img_path=face_img_rgb, model_name="VGG-Face")[0]["embedding"]
    except Exception:
        return False
    for _, emb in whitelist_embeddings:
        distance = np.linalg.norm(np.array(face_embedding) - np.array(emb))
        if distance < threshold:
            return True
    return False

def process_video(input_path, output_path, progress_callback=None, log_callback=None):
    whitelist_embeddings = get_face_embeddings()
    if not whitelist_embeddings:
        if log_callback: log_callback("Whitelist is empty. Add faces to the whitelist.")
        return False
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        if log_callback: log_callback("Failed to open video.")
        return False

    width, height = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame_idx in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        try:
            faces = DeepFace.extract_faces(img_path=frame, detector_backend="opencv", enforce_detection=False)
            for face in faces:
                area = face['facial_area']
                x, y, w, h = area['x'], area['y'], area['w'], area['h']
                face_img = frame[y:y+h, x:x+w]
                if not is_face_whitelisted(face_img, whitelist_embeddings):
                    # Blur face
                    blurred_face = cv2.GaussianBlur(face_img, (99, 99), 30)
                    frame[y:y+h, x:x+w] = blurred_face
        except Exception as e:
            if log_callback: log_callback(f"Error on frame {frame_idx}: {str(e)}")
        out.write(frame)
        if progress_callback and frame_count > 0:
            progress_callback(int((frame_idx+1)/frame_count * 100))
    cap.release()
    out.release()
    if log_callback: log_callback(f"Video saved to {output_path}")
    return True

def crop_face(image_path):
    """Detect and crop the largest face from an image, return PIL Image or None."""
    try:
        faces = DeepFace.extract_faces(img_path=image_path, detector_backend="opencv", enforce_detection=True)
        if not faces:
            return None
        area = faces[0]['facial_area']
        img = Image.open(image_path)
        cropped = img.crop((area['x'], area['y'], area['x']+area['w'], area['y']+area['h']))
        return cropped
    except Exception as e:
        print(f"Could not crop face: {e}")
        return None

def add_to_whitelist(img_path, cropped_img=None):
    """Add (cropped) face image to whitelist folder."""
    os.makedirs(WHITELIST_DIR, exist_ok=True)
    base = os.path.basename(img_path)
    dest = os.path.join(WHITELIST_DIR, base)
    if cropped_img:
        cropped_img.save(dest)
    else:
        import shutil
        shutil.copy(img_path, dest)
    print(f"Added {base} to whitelist.")