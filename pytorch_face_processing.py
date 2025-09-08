"""
PyTorch Face Processor

This module uses the facenet-pytorch library for face detection and recognition,
providing a PyTorch-based alternative to the TensorFlow/MTCNN implementation.
"""

import torch
import cv2
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

class PyTorchFaceProcessor:
    """
    A face processor that uses PyTorch for face detection and blurring.
    """
    def __init__(self, use_gpu=True):
        """
        Initialize the PyTorch Face Processor.
        
        Args:
            use_gpu (bool): Whether to use GPU if available.
        """
        self.device = torch.device('cuda:0' if torch.cuda.is_available() and use_gpu else 'cpu')
        print(f"PyTorch Face Processor using device: {self.device}")

        # Initialize models and move them to the selected device
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        
        self.whitelist_embeddings = []
        self.whitelist_updated = False

    def update_whitelist(self, whitelist_images):
        """
        Update the whitelist with new face embeddings.
        
        Args:
            whitelist_images (list): A list of paths to whitelist images.
        """
        self.whitelist_embeddings = []
        print(f"Updating whitelist with {len(whitelist_images)} images...")
        
        for img_path in whitelist_images:
            try:
                img = Image.open(img_path).convert('RGB')
                # Detect faces and get embeddings
                boxes, _ = self.mtcnn.detect(img)
                if boxes is not None:
                    # Get embedding for the first face found in the image
                    face_tensor = self.mtcnn.extract(img, boxes[0:1], save_path=None)
                    if face_tensor is not None:
                        embedding = self.resnet(face_tensor.to(self.device)).detach().cpu()
                        self.whitelist_embeddings.append(embedding)
                        print(f"Added embedding from {img_path} to whitelist.")
            except Exception as e:
                print(f"Error processing whitelist image {img_path}: {e}")
        
        self.whitelist_updated = True
        print("Whitelist update complete.")

    def detect_and_blur_faces(self, frame, detection_confidence=0.9, embedding_threshold=0.8):
        """
        Detect faces in a frame, compare against the whitelist, and blur non-whitelisted faces.
        
        Args:
            frame (np.array): The video frame to process.
            detection_confidence (float): The confidence threshold for face detection.
            embedding_threshold (float): The distance threshold for face recognition.
            
        Returns:
            np.array: The processed frame with faces blurred.
            int: The number of faces detected.
            int: The number of faces blurred.
        """
        num_detected = 0
        num_blurred = 0
        
        try:
            # Convert frame to PIL Image for detection
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # Detect faces
            boxes, probs = self.mtcnn.detect(img)
            
            if boxes is not None:
                num_detected = len(boxes)
                
                for i, (box, prob) in enumerate(zip(boxes, probs)):
                    if prob < detection_confidence:
                        continue

                    # Extract face tensor for embedding
                    face_tensor = self.mtcnn.extract(img, [box], save_path=None)
                    
                    if face_tensor is None:
                        continue

                    # Get embedding
                    embedding = self.resnet(face_tensor.to(self.device)).detach().cpu()
                    
                    # Check against whitelist
                    is_whitelisted = False
                    if self.whitelist_embeddings:
                        for wl_embedding in self.whitelist_embeddings:
                            distance = (embedding - wl_embedding).norm().item()
                            if distance < embedding_threshold:
                                is_whitelisted = True
                                break
                    
                    # Blur if not whitelisted
                    if not is_whitelisted:
                        num_blurred += 1
                        x1, y1, x2, y2 = [int(b) for b in box]
                        face = frame[y1:y2, x1:x2]
                        
                        # Apply Gaussian blur
                        if face.size > 0:
                            blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
                            frame[y1:y2, x1:x2] = blurred_face
                            
        except Exception as e:
            print(f"Error during face detection and blurring: {e}")
            
        return frame, num_detected, num_blurred

def check_pytorch_gpu():
    """Check if PyTorch can access the GPU."""
    return torch.cuda.is_available()
