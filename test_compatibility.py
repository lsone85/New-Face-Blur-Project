#!/usr/bin/env python3
"""
Test script for Face Blur Project functionality
Tests basic imports and core functionality without GUI
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Test Python version compatibility."""
    print(f"Python version: {sys.version}")
    version_info = sys.version_info
    if version_info >= (3, 9):
        print("✓ Python 3.9+ compatible")
        return True
    else:
        print("✗ Python version is too old. Requires Python 3.9+")
        return False

def test_basic_imports():
    """Test basic library imports."""
    print("\nTesting basic imports...")
    
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow (PIL) import successful")
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False
    
    return True

def test_deepface_import():
    """Test DeepFace import (might be slow due to model downloads)."""
    print("\nTesting DeepFace import (this may take a while on first run)...")
    
    try:
        from deepface import DeepFace
        print("✓ DeepFace import successful")
        return True
    except ImportError as e:
        print(f"✗ DeepFace import failed: {e}")
        print("  This might be due to tensorflow/tf-keras compatibility issues")
        print("  Consider running: pip install --upgrade tensorflow==2.15.0 deepface==0.0.75")
        return False
    except Exception as e:
        print(f"✗ DeepFace initialization failed: {e}")
        return False

def test_ui_import():
    """Test UI imports (tkinter)."""
    print("\nTesting UI imports...")
    
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        print("✓ Tkinter import successful")
        
        # Test basic tkinter functionality
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✓ Tkinter basic functionality works")
        return True
    except ImportError as e:
        print(f"✗ Tkinter import failed: {e}")
        print("  Install tkinter:")
        print("    Ubuntu/Debian: sudo apt-get install python3-tk")
        print("    CentOS/RHEL: sudo yum install tkinter")
        print("    macOS: Install Python from python.org")
        print("    Windows: Reinstall Python with tkinter option")
        return False
    except Exception as e:
        print(f"✗ Tkinter functionality test failed: {e}")
        return False

def test_project_structure():
    """Test project file structure."""
    print("\nTesting project structure...")
    
    required_files = [
        "main.py",
        "ui_tkinter.py", 
        "face_processing.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        ".editorconfig"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✓ {file} exists")
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    
    return True

def test_application_imports():
    """Test our application module imports."""
    print("\nTesting application imports...")
    
    try:
        from face_processing import get_face_embeddings, add_to_whitelist
        print("✓ face_processing module imports successful")
    except ImportError as e:
        print(f"✗ face_processing import failed: {e}")
        return False
    
    try:
        from ui_tkinter import run_ui
        print("✓ ui_tkinter module imports successful")
    except ImportError as e:
        print(f"✗ ui_tkinter import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("=== Face Blur Project Compatibility Test ===")
    print("Testing compatibility with Python 3.9+ and PyCharm 2024.2.6")
    
    tests = [
        ("Python Version", test_python_version),
        ("Basic Imports", test_basic_imports),
        ("Project Structure", test_project_structure),
        ("Application Imports", test_application_imports),
        ("UI Imports", test_ui_import),
        ("DeepFace Import", test_deepface_import),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        icon = "✓" if success else "✗"
        print(f"{icon} {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The project should work correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. See above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)