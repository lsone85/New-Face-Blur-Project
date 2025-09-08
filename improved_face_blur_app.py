#!/usr/bin/env python
"""
Improved Face Blur Application with Multiple Processor Backends

This application provides a user-friendly interface for face detection and blurring in videos.
It supports multiple processing backends, including TensorFlow/MTCNN and PyTorch/FaceNet,
and allows for GPU acceleration.
"""

import os
import sys
import argparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import threading
from PIL import Image, ImageTk
import time
import platform
from pytorch_face_processing import PyTorchFaceProcessor


class FaceBlurApp:
    """
    Main application class for the Face Blur UI.
    """
    def __init__(self, root, args):
        """
        Initialize the Face Blur application UI.
        
        Args:
            root: The root Tkinter window.
            args: Command-line arguments.
        """
        self.root = root
        self.root.title("Face Blur Application")
        self.root.geometry("1000x800")

        # Initialize variables
        self.processor = None
        self.video_source = None
        self.cap = None
        self.is_processing = False
        self.is_paused = False
        self.start_time = 0
        self.total_frames = 0
        self.processed_frames = 0
        self.output_path = ""
        self.whitelist_paths = []

        # UI variables
        self.status_text = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        self.use_gpu = tk.BooleanVar(value=args.gpu)
        self.processor_choice = tk.StringVar(value="pytorch")

        # Create UI
        self.create_ui()
        
        # Determine hardware availability and set up processor
        self.setup_processor(args)

        # Log initialization status
        self.log(f"Selected processor: {self.processor_choice.get()}")
        if self.use_gpu.get():
            self.log("GPU acceleration enabled.")
        else:
            self.log("Running in CPU mode.")

    def setup_processor(self, args):
        """
        Initialize the selected face processor based on availability and user choice.
        """
        use_gpu_flag = not args.cpu and args.gpu
        self.log(f"Attempting to set up processor with GPU: {use_gpu_flag}")

        try:
            self.log("Initializing PyTorch processor...")
            self.processor = PyTorchFaceProcessor(use_gpu=use_gpu_flag)
            self.log(f"Processor setup complete. self.processor is {'set' if self.processor else 'None'}.")
        except Exception as e:
            self.log(f"Error during processor setup: {e}")
            messagebox.showerror("Error", f"Failed to initialize processor: {e}")
            self.root.quit()

    def create_ui(self):
        """
        Create the main user interface.
        """
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top frame for controls
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)

        # File selection
        file_frame = ttk.LabelFrame(top_frame, text="Input/Output", padding="5")
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.select_video_btn = ttk.Button(file_frame, text="Select Video", command=self.select_video)
        self.select_video_btn.pack(side=tk.LEFT, padx=5)
        self.video_label = ttk.Label(file_frame, text="No video selected")
        self.video_label.pack(side=tk.LEFT, padx=5)

        # Whitelist controls
        whitelist_frame = ttk.LabelFrame(top_frame, text="Whitelist", padding="5")
        whitelist_frame.pack(side=tk.LEFT, fill=tk.X, padx=5)
        
        self.add_whitelist_btn = ttk.Button(whitelist_frame, text="Add Whitelist Images", command=self.add_whitelist_images)
        self.add_whitelist_btn.pack(side=tk.LEFT, padx=5)
        self.whitelist_label = ttk.Label(whitelist_frame, text="0 images")
        self.whitelist_label.pack(side=tk.LEFT, padx=5)

        # Video display
        video_frame = ttk.LabelFrame(main_frame, text="Video Preview", padding="5")
        video_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.canvas = tk.Canvas(video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Processing controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)

        self.start_btn = ttk.Button(control_frame, text="Start Processing", command=self.start_processing)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_processing, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Processor selection
        processor_frame = ttk.Frame(control_frame)
        processor_frame.pack(side=tk.RIGHT, padx=20)
        ttk.Label(processor_frame, text="Processor:").pack(side=tk.LEFT)
        
        ttk.Radiobutton(processor_frame, text="PyTorch", variable=self.processor_choice, value="pytorch", command=self.on_processor_change).pack(side=tk.LEFT)
        
        # GPU checkbox
        self.gpu_check = ttk.Checkbutton(processor_frame, text="Use GPU", variable=self.use_gpu, command=self.on_processor_change)
        self.gpu_check.pack(side=tk.LEFT, padx=10)
        self.use_gpu.set(self.use_gpu.get())

        # Progress and status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_text)
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Log text
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.pack(fill=tk.X, pady=5)
        self.log_text = tk.Text(log_frame, height=6, state=tk.DISABLED)
        self.log_text.pack(fill=tk.X, expand=True)

    def on_processor_change(self):
        """Handle change in processor or GPU selection."""
        self.log(f"Changing processor to {self.processor_choice.get()} with GPU: {self.use_gpu.get()}")
        # Re-initialize the processor with the new settings
        self.setup_processor(argparse.Namespace(
            cpu=not self.use_gpu.get(),
            gpu=self.use_gpu.get(),
            version=self.processor_choice.get()
        ))
        self.log("Processor changed successfully.")

    def select_video(self):
        """Open a dialog to select a video file."""
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if path:
            self.video_source = path
            self.video_label.config(text=os.path.basename(path))
            self.log(f"Selected video: {path}")
            self.load_video_preview()

    def load_video_preview(self):
        """Load the first frame of the video as a preview."""
        if self.video_source:
            cap = cv2.VideoCapture(self.video_source)
            ret, frame = cap.read()
            if ret:
                self.display_frame(frame)
            cap.release()

    def add_whitelist_images(self):
        """Open a dialog to select whitelist images."""
        paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if paths:
            self.whitelist_paths.extend(paths)
            self.whitelist_label.config(text=f"{len(self.whitelist_paths)} images")
            self.log(f"Added {len(paths)} images to whitelist.")
            if self.processor:
                self.processor.update_whitelist(self.whitelist_paths)

    def start_processing(self):
        """Start the video processing thread."""
        if not self.video_source:
            messagebox.showerror("Error", "Please select a video file first.")
            return

        self.output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4", "*.mp4"), ("AVI", "*.avi")])
        if not self.output_path:
            return

        self.is_processing = True
        self.is_paused = False
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.processing_thread = threading.Thread(target=self.process_video)
        self.processing_thread.start()

    def process_video(self):
        """The main video processing loop."""
        self.cap = cv2.VideoCapture(self.video_source)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

        self.start_time = time.time()
        self.processed_frames = 0

        while self.is_processing and self.cap.isOpened():
            if self.is_paused:
                time.sleep(0.1)
                continue

            ret, frame = self.cap.read()
            if not ret:
                break

            # Process the frame
            processed_frame, detected, blurred = self.processor.detect_and_blur_faces(frame)
            out.write(processed_frame)
            
            self.processed_frames += 1
            
            # Update UI
            self.display_frame(processed_frame)
            self.update_status()

        self.cap.release()
        out.release()
        self.stop_processing(finished=True)

    def display_frame(self, frame):
        """Display a frame on the canvas."""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        h, w, _ = frame.shape
        aspect_ratio = w / h
        
        if canvas_w / aspect_ratio < canvas_h:
            new_w = canvas_w
            new_h = int(new_w / aspect_ratio)
        else:
            new_h = canvas_h
            new_w = int(new_h * aspect_ratio)
            
        resized_frame = cv2.resize(frame, (new_w, new_h))
        
        img = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        self.photo = ImageTk.PhotoImage(image=img)
        
        self.canvas.create_image(canvas_w/2, canvas_h/2, image=self.photo, anchor=tk.CENTER)

    def update_status(self):
        """Update the status bar and progress."""
        if self.total_frames > 0:
            progress = (self.processed_frames / self.total_frames) * 100
            self.progress_var.set(progress)
            
            elapsed_time = time.time() - self.start_time
            fps = self.processed_frames / elapsed_time if elapsed_time > 0 else 0
            
            status = f"Processing: {self.processed_frames}/{self.total_frames} | FPS: {fps:.2f}"
            self.status_text.set(status)

    def toggle_pause(self):
        """Pause or resume processing."""
        self.is_paused = not self.is_paused
        self.pause_btn.config(text="Resume" if self.is_paused else "Pause")
        self.log("Processing paused." if self.is_paused else "Processing resumed.")

    def stop_processing(self, finished=False):
        """Stop the video processing."""
        self.is_processing = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED, text="Pause")
        self.stop_btn.config(state=tk.DISABLED)
        
        if finished:
            self.log(f"Processing finished. Output saved to {self.output_path}")
            self.status_text.set("Finished")
        else:
            self.log("Processing stopped by user.")
            self.status_text.set("Stopped")

    def log(self, message):
        """Log a message to the text widget."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

def main():
    parser = argparse.ArgumentParser(description="Run Face Blur Application")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU acceleration (if available)")
    parser.add_argument("--cpu", action="store_true", help="Force CPU mode even if GPU is available")
    args = parser.parse_args()

    root = tk.Tk()
    app = FaceBlurApp(root, args)
    root.mainloop()

if __name__ == "__main__":
    main()
