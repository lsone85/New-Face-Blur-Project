# Face Blur Project - Troubleshooting Guide

This guide helps resolve common issues when setting up and running the Face Blur Project with Python 3.9+ and PyCharm 2024.2.6.

## Common Setup Issues

### 1. Python Version Issues

**Problem**: "Python version is too old" or compatibility warnings
**Solution**: 
- Install Python 3.9 or higher from [python.org](https://python.org)
- Verify installation: `python --version` or `python3 --version`
- Make sure PATH is configured correctly

### 2. Tkinter Missing

**Problem**: `ModuleNotFoundError: No module named 'tkinter'`

**Solutions by OS**:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL/Fedora**: `sudo dnf install tkinter` or `sudo yum install tkinter`
- **macOS**: Install Python from python.org (not Homebrew)
- **Windows**: Reinstall Python with "tcl/tk and IDLE" option checked

### 3. TensorFlow/DeepFace Compatibility Issues

**Problem**: `You have tensorflow X.X.X and this requires tf-keras package`

**Solutions**:
```bash
# Option 1: Install tf-keras
pip install tf-keras

# Option 2: Use compatible versions
pip uninstall tensorflow deepface
pip install tensorflow==2.15.1 deepface==0.0.75

# Option 3: Clean install
pip uninstall tensorflow deepface tf-keras
pip install -r requirements.txt
```

### 4. Virtual Environment Issues

**Problem**: Virtual environment not activating or packages not found

**Solutions**:
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## PyCharm 2024.2.6 Specific Issues

### 1. Python Interpreter Not Detected

**Problem**: PyCharm can't find Python interpreter

**Solution**:
1. Go to File → Settings → Project → Python Interpreter
2. Click the gear icon → Add...
3. Select "Virtualenv Environment" → "Existing environment"
4. Point to: `./venv/bin/python` (Linux/macOS) or `.\venv\Scripts\python.exe` (Windows)

### 2. Module Import Errors in PyCharm

**Problem**: "Module not found" errors despite successful pip install

**Solutions**:
1. Check Python interpreter is correct (see above)
2. Ensure virtual environment is selected
3. Restart PyCharm
4. File → Invalidate Caches and Restart

### 3. Run Configuration Issues

**Problem**: Can't run main.py from PyCharm

**Solution**:
1. Right-click on `main.py` → Run
2. Or: Run → Edit Configurations → + → Python Script
3. Set Script path to: `$PROJECT_DIR$/main.py`
4. Ensure Working directory is: `$PROJECT_DIR$`

## Runtime Issues

### 1. DeepFace Model Download Failures

**Problem**: Models fail to download on first run

**Solutions**:
- Check internet connection
- Disable VPN/proxy temporarily
- Run with administrator privileges
- Clear DeepFace cache: `~/.deepface/weights/` (delete folder)

### 2. Video Processing Errors

**Problem**: Video processing fails or produces corrupted output

**Solutions**:
- Ensure input video is not corrupted
- Check sufficient disk space (2x video size recommended)
- Add faces to whitelist before processing
- Try smaller video files first

### 3. Face Detection Issues

**Problem**: Faces not detected or incorrectly processed

**Solutions**:
- Use clear, front-facing images for whitelist
- Ensure good lighting in source videos
- Consider cropping whitelist images manually
- Adjust face matching threshold in `.env` file

## Performance Issues

### 1. Slow Processing

**Solutions**:
- Use GPU acceleration if available
- Process smaller video segments
- Close unnecessary applications
- Use SSD storage

### 2. Memory Issues

**Problem**: Out of memory errors during processing

**Solutions**:
- Process smaller videos
- Increase virtual memory/swap
- Close other applications
- Use 64-bit Python

## Testing and Validation

### Run Compatibility Test

```bash
python test_compatibility.py
```

This script tests:
- Python version compatibility
- Required imports
- Project structure
- DeepFace functionality
- UI components

### Manual Testing

1. Test basic imports:
```python
import cv2, numpy, PIL
print("Basic imports work")
```

2. Test tkinter:
```python
import tkinter as tk
root = tk.Tk()
root.destroy()
print("Tkinter works")
```

3. Test face processing (if DeepFace works):
```python
from face_processing import get_face_embeddings
print("Face processing works")
```

## Alternative Solutions

### 1. If DeepFace Won't Work

The application includes fallback face detection using OpenCV Haar cascades. While less accurate, it provides basic functionality without DeepFace.

### 2. If Tkinter Won't Work

Consider using PyQt5 as an alternative (included in requirements):
```python
# Modify ui_tkinter.py to use PyQt5 instead
from PyQt5.QtWidgets import QApplication, QMainWindow
```

### 3. Docker Alternative

For consistent environments, consider using Docker:
```dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y python3-tk libgl1-mesa-glx
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## Getting Help

If issues persist:

1. Run the compatibility test: `python test_compatibility.py`
2. Check system requirements in README.md
3. Review error messages carefully
4. Search for specific error messages online
5. Check DeepFace and TensorFlow documentation
6. Consider using older/stable versions of dependencies

## Environment Information

When reporting issues, please include:
- Operating system and version
- Python version (`python --version`)
- PyCharm version
- Virtual environment status
- Output of `pip list`
- Full error message and stack trace