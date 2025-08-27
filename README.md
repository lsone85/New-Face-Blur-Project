# Face Blur Application

A cross-platform application that blurs all faces in a video except those whitelisted using DeepFace recognition technology.

## Features

- Modern Tkinter GUI interface
- Add faces to whitelist (automatically cropped for best results)
- Remove faces from whitelist
- Preview faces in whitelist
- Select and process videos (MP4, AVI formats)
- Progress tracking and error logging during processing
- Advanced face recognition using DeepFace and VGG-Face model
- Blurs all faces except whitelisted ones
- Exports processed videos to output directory

## System Requirements

- Python 3.9 or higher
- PyCharm 2024.2.6 (recommended IDE)
- Operating System: Windows, macOS, or Linux
- At least 4GB RAM (8GB recommended for video processing)
- GPU acceleration (optional, but recommended for faster processing)

## Setup Instructions

### Option 1: PyCharm Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lsone85/New-Face-Blur-Project.git
   cd New-Face-Blur-Project
   ```

2. **Open in PyCharm:**
   - Launch PyCharm 2024.2.6
   - Select "Open" and navigate to the cloned repository folder
   - PyCharm will automatically detect the project structure

3. **Configure Python Interpreter:**
   - Go to File → Settings (Windows/Linux) or PyCharm → Preferences (macOS)
   - Navigate to Project → Python Interpreter
   - Click the gear icon and select "Add..."
   - Choose "Virtualenv Environment" → "New environment"
   - Set Base interpreter to Python 3.9
   - Location should be `./venv` in your project directory
   - Click "OK"

4. **Install Dependencies:**
   - Open the Terminal in PyCharm (View → Tool Windows → Terminal)
   - Run: `pip install -r requirements.txt`

5. **Run the Application:**
   - Right-click on `main.py` in the Project view
   - Select "Run 'main'" or use Ctrl+Shift+F10 (Windows/Linux) or Cmd+Shift+R (macOS)
   - Or configure a run configuration: Run → Edit Configurations → + → Python Script

### Option 2: Command Line Setup

1. **Clone and setup:**
   ```bash
   git clone https://github.com/lsone85/New-Face-Blur-Project.git
   cd New-Face-Blur-Project
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

## Usage Guide

1. **Add faces to whitelist:**
   - Click "Add Face to Whitelist"
   - Select a clear, front-facing photo of the person
   - The application will automatically detect and crop the face
   - Repeat for all people you want to remain unblurred

2. **Process videos:**
   - Click "Select Video and Export"
   - Choose your input video file (MP4 or AVI)
   - Select the output location and filename
   - The application will process the video, blurring all faces except whitelisted ones

## Project Structure

```
New-Face-Blur-Project/
├── main.py                 # Application entry point
├── ui_tkinter.py          # User interface implementation
├── face_processing.py     # Face detection and video processing logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── .editorconfig         # Code style configuration
├── .gitignore           # Git ignore rules
├── .idea/               # PyCharm project configuration
│   ├── misc.xml
│   ├── modules.xml
│   └── New-Face-Blur-Project.iml
├── output/              # Generated video files (created automatically)
└── whitelist/           # Whitelisted face images (created automatically)
```

## Configuration

Copy `.env.example` to `.env` and modify settings as needed:
- Adjust face matching threshold
- Change default blur parameters
- Modify UI settings

## Troubleshooting

### Common Issues

1. **"No module named 'tkinter'" error:**
   - On Linux: `sudo apt-get install python3-tk`
   - On macOS: Install Python from python.org (not Homebrew)
   - On Windows: Reinstall Python with tkinter option checked

2. **DeepFace model download issues:**
   - Ensure stable internet connection
   - Models are downloaded automatically on first run
   - Check firewall/proxy settings if download fails

3. **Video processing errors:**
   - Ensure input video is not corrupted
   - Check that whitelist contains valid face images
   - Verify sufficient disk space for output

4. **PyCharm configuration issues:**
   - Ensure Python 3.9+ interpreter is selected
   - Verify virtual environment is activated
   - Check that all dependencies are installed in the correct environment

## Performance Tips

- Use GPU acceleration for faster processing (requires CUDA setup)
- Process videos in smaller segments for very large files
- Use SSD storage for better I/O performance
- Close unnecessary applications while processing large videos

## Notes

- Whitelist images should be clear, front-facing photos for best results
- Output videos are saved in the `output/` folder
- Face detection uses DeepFace with OpenCV backend for optimal speed
- VGG-Face model provides high accuracy for face recognition
- The application automatically creates necessary directories