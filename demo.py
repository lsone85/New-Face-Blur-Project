#!/usr/bin/env python3
"""
Demo script to show Face Blur Project functionality without GUI
This demonstrates the core components work correctly
"""

import os
import sys
from pathlib import Path

def demo_basic_functionality():
    """Demonstrate basic functionality without DeepFace dependency."""
    print("=== Face Blur Project - Basic Functionality Demo ===")
    
    # Test imports
    try:
        import cv2
        import numpy as np
        from PIL import Image
        print("✓ Core libraries imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test face processing module
    try:
        from face_processing import DEEPFACE_AVAILABLE, WHITELIST_DIR, get_face_embeddings
        print(f"✓ Face processing module imported")
        print(f"  - DeepFace available: {DEEPFACE_AVAILABLE}")
        print(f"  - Whitelist directory: {WHITELIST_DIR}")
    except ImportError as e:
        print(f"✗ Face processing import error: {e}")
        return False
    
    # Test directory creation
    if not os.path.exists(WHITELIST_DIR):
        os.makedirs(WHITELIST_DIR, exist_ok=True)
        print(f"✓ Created {WHITELIST_DIR} directory")
    else:
        print(f"✓ {WHITELIST_DIR} directory exists")
    
    # Test output directory
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ Created {output_dir} directory")
    else:
        print(f"✓ {output_dir} directory exists")
    
    # Test OpenCV face detection capability
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if face_cascade.empty():
            print("✗ OpenCV Haar cascade not loaded")
        else:
            print("✓ OpenCV face detection ready (fallback method)")
    except Exception as e:
        print(f"✗ OpenCV face detection error: {e}")
    
    # Test whitelist functionality
    try:
        embeddings = get_face_embeddings()
        print(f"✓ Whitelist check completed ({len(embeddings)} faces loaded)")
    except Exception as e:
        print(f"✗ Whitelist error: {e}")
    
    print("\n=== Project Structure ===")
    files_to_check = [
        "main.py",
        "ui_tkinter.py", 
        "face_processing.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        ".editorconfig",
        ".env.example",
        "test_compatibility.py",
        "setup.sh",
        "setup.bat",
        "TROUBLESHOOTING.md"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"✗ {file} missing")
    
    print("\n=== PyCharm Configuration ===")
    idea_files = [
        ".idea/misc.xml",
        ".idea/modules.xml", 
        ".idea/New-Face-Blur-Project.iml"
    ]
    
    for file in idea_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} missing")
    
    return True

def demo_opencv_functionality():
    """Demonstrate OpenCV functionality with a simple example."""
    print("\n=== OpenCV Functionality Demo ===")
    
    try:
        import cv2
        import numpy as np
        
        # Create a simple test image
        test_img = np.zeros((300, 400, 3), dtype=np.uint8)
        test_img[:] = (50, 100, 150)  # Fill with color
        
        # Add some text
        cv2.putText(test_img, "Face Blur Project", (50, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(test_img, "OpenCV Working!", (100, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Save test image
        test_output = "output/test_image.png"
        cv2.imwrite(test_output, test_img)
        
        if os.path.exists(test_output):
            print(f"✓ Test image created: {test_output}")
            print(f"✓ OpenCV image operations working")
            return True
        else:
            print("✗ Failed to create test image")
            return False
            
    except Exception as e:
        print(f"✗ OpenCV demo error: {e}")
        return False

def main():
    """Run the demo."""
    print("Face Blur Project - Functionality Demo")
    print("=" * 50)
    
    success1 = demo_basic_functionality()
    success2 = demo_opencv_functionality()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 Demo completed successfully!")
        print("The project structure and basic functionality are working correctly.")
        print("\nNext steps:")
        print("1. Install tkinter for GUI functionality")
        print("2. Fix TensorFlow/DeepFace compatibility for full functionality")
        print("3. Run: python test_compatibility.py")
        print("4. Try running: python main.py")
    else:
        print("⚠️ Some issues were found. Check the output above.")
        print("See TROUBLESHOOTING.md for solutions.")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)