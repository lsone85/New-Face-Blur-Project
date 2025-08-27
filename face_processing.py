"""
Face Processing Module for Face Blur Application
Compatible with Python 3.9+ and PyCharm 2024.2.6
Handles face detection, recognition, and video processing
"""

import cv2
import numpy as np
import os
from PIL import Image

# Try to import DeepFace with proper error handling
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
    print("DeepFace imported successfully")
except ImportError as e:
    print(f"Warning: DeepFace not available - {e}")
    print("Some functionality will be limited. Install with: pip install deepface==0.0.75 tensorflow==2.15.1")
    DEEPFACE_AVAILABLE = False
except Exception as e:
    print(f"Warning: DeepFace initialization error - {e}")
    print("Consider checking your TensorFlow installation")
    DEEPFACE_AVAILABLE = False

WHITELIST_DIR = "whitelist"

def get_face_embeddings():
    """Load whitelist images and generate their embeddings."""
    embeddings = []
    
    # Check if DeepFace is available
    if not DEEPFACE_AVAILABLE:
        print("DeepFace is not available. Cannot generate embeddings.")
        return embeddings
    
    # Check if whitelist directory exists
    if not os.path.exists(WHITELIST_DIR):
        print(f"Whitelist directory '{WHITELIST_DIR}' does not exist.")
        return embeddings
    
    # Check if directory is empty
    if not os.listdir(WHITELIST_DIR):
        print(f"Whitelist directory '{WHITELIST_DIR}' is empty.")
        return embeddings
    
    for img_file in os.listdir(WHITELIST_DIR):
        img_path = os.path.join(WHITELIST_DIR, img_file)
        
        # Skip non-image files
        if not img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
            continue
            
        try:
            embedding = DeepFace.represent(img_path=img_path, model_name="VGG-Face")[0]["embedding"]
            embeddings.append((img_file, embedding))
            print(f"Successfully processed {img_file}")
        except Exception as e:
            print(f"Failed to process {img_file}: {e}")
    
    print(f"Loaded {len(embeddings)} face embeddings from whitelist.")
    return embeddings

def is_face_whitelisted(face_img, whitelist_embeddings, threshold=0.5):
    """Check if detected face matches any in the whitelist."""
    if not DEEPFACE_AVAILABLE:
        print("DeepFace not available, cannot check whitelist")
        return False
        
    try:
        # Convert OpenCV image (BGR) to RGB for DeepFace
        if len(face_img.shape) == 3 and face_img.shape[2] == 3:
            face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        else:
            face_img_rgb = face_img
        face_embedding = DeepFace.represent(img_path=face_img_rgb, model_name="VGG-Face")[0]["embedding"]
    except Exception as e:
        print(f"Error generating embedding for face: {e}")
        return False
    
    for _, emb in whitelist_embeddings:
        distance = np.linalg.norm(np.array(face_embedding) - np.array(emb))
        if distance < threshold:
            return True
    return False

def process_video(input_path, output_path, progress_callback=None, log_callback=None):
    """Process video to blur faces except whitelisted ones."""
    if not DEEPFACE_AVAILABLE:
        error_msg = "DeepFace is not available. Cannot process video."
        if log_callback: 
            log_callback(error_msg)
        print(error_msg)
        return False
    
    whitelist_embeddings = get_face_embeddings()
    if not whitelist_embeddings:
        if log_callback: 
            log_callback("Whitelist is empty. Add faces to the whitelist first.")
        return False
    
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        if log_callback: 
            log_callback("Failed to open video.")
        return False

    width, height = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if log_callback:
        log_callback(f"Processing {frame_count} frames...")

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
            if log_callback: 
                log_callback(f"Error on frame {frame_idx}: {str(e)}")
        
        out.write(frame)
        if progress_callback and frame_count > 0:
            progress_callback(int((frame_idx+1)/frame_count * 100))
    
    cap.release()
    out.release()
    if log_callback: 
        log_callback(f"Video saved to {output_path}")
    return True

def crop_face(image_path):
    """Detect and crop the largest face from an image, return PIL Image or None."""
    if not DEEPFACE_AVAILABLE:
        print("DeepFace not available, cannot crop face")
        return None
        
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
        # Try to auto-crop the face first if DeepFace is available
        if DEEPFACE_AVAILABLE:
            cropped = crop_face(img_path)
            if cropped:
                cropped.save(dest)
                print(f"Added cropped face from {base} to whitelist.")
                return
        
        # Fallback: copy original image
        import shutil
        shutil.copy(img_path, dest)
        print(f"Added {base} to whitelist (original image).")

# Fallback functions for when DeepFace is not available
def use_opencv_face_detection(image_path):
    """Fallback face detection using OpenCV Haar cascades."""
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Return the largest face
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face
            cropped = img[y:y+h, x:x+w]
            pil_image = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
            return pil_image
        return None
    except Exception as e:
        print(f"OpenCV face detection failed: {e}")
        return None