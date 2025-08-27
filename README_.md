# Face Blur App (PyQt5)

A Windows application that blurs all faces in a video except those whitelisted using DeepFace recognition.

## Features

- Modern PyQt5 UI
- Add faces to whitelist (cropped for best results)
- Remove faces from whitelist
- Preview faces in whitelist
- Select and process videos (MP4, AVI)
- Progress bar and error log during processing
- Blurs all faces except whitelisted ones
- Exports processed video

## Setup

1. Clone the repository.
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run in PyCharm or from command line:
   ```
   python main.py
   ```
4. Add faces to the whitelist before processing videos.

## Notes

- Whitelist images should be clear, front-facing.
- Output videos are saved in the `output/` folder.
- Cropping uses DeepFace to detect the largest face in the image.