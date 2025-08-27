"""
Face Blur Application - UI Module using Tkinter
Compatible with Python 3.9+ and PyCharm 2024.2.6
"""

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ImportError as e:
    print("Error: tkinter is not available. Please install tkinter:")
    print("  - On Ubuntu/Debian: sudo apt-get install python3-tk")
    print("  - On CentOS/RHEL: sudo yum install tkinter")
    print("  - On macOS: Install Python from python.org")
    print("  - On Windows: Reinstall Python with tkinter option")
    raise e

import os
from face_processing import process_video, add_to_whitelist

OUTPUT_DIR = "output"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def select_video():
    """Select input video and process it with face blurring."""
    # Fix file dialog filters for better cross-platform compatibility
    video_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[
            ("Video files", "*.mp4 *.avi *.mov *.mkv"),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("All files", "*.*")
        ]
    )
    
    if video_path:
        ensure_output_dir()
        output_path = filedialog.asksaveasfilename(
            title="Save Processed Video As",
            defaultextension=".avi", 
            initialdir=OUTPUT_DIR,
            filetypes=[
                ("AVI Video", "*.avi"),
                ("MP4 Video", "*.mp4"),
                ("All files", "*.*")
            ]
        )
        
        if output_path:
            try:
                success = process_video(video_path, output_path)
                if success:
                    messagebox.showinfo("Success", f"Video exported to {output_path}")
                else:
                    messagebox.showerror("Error", "Could not process video. Check the console for details.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

def add_face():
    """Add a face image to the whitelist."""
    img_path = filedialog.askopenfilename(
        title="Select Face Image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
    )
    
    if img_path:
        try:
            add_to_whitelist(img_path)
            messagebox.showinfo("Success", "Face added to whitelist successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add face to whitelist: {str(e)}")

def run_ui():
    """Run the main application UI."""
    root = tk.Tk()
    root.title("Face Blur Application")
    root.geometry("400x300")
    root.resizable(False, False)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Main title
    title_frame = tk.Frame(root)
    title_frame.pack(pady=20)
    
    tk.Label(
        title_frame, 
        text="Face Blur Application", 
        font=("Arial", 18, "bold")
    ).pack()
    
    tk.Label(
        title_frame, 
        text="Powered by DeepFace & OpenCV", 
        font=("Arial", 10), 
        fg="gray"
    ).pack()

    # Buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=20)

    btn_video = tk.Button(
        buttons_frame, 
        text="📹 Select Video and Process", 
        width=35, 
        height=2,
        font=("Arial", 11),
        command=select_video,
        bg="#4CAF50",
        fg="white",
        relief="raised"
    )
    btn_video.pack(pady=10)

    btn_add_face = tk.Button(
        buttons_frame, 
        text="👤 Add Face to Whitelist", 
        width=35, 
        height=2,
        font=("Arial", 11),
        command=add_face,
        bg="#2196F3",
        fg="white",
        relief="raised"
    )
    btn_add_face.pack(pady=10)

    # Instructions frame
    instructions_frame = tk.Frame(root)
    instructions_frame.pack(pady=10, padx=20)
    
    tk.Label(
        instructions_frame, 
        text="Instructions:",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")
    
    tk.Label(
        instructions_frame, 
        text="1. Add clear, front-facing face images to whitelist first",
        font=("Arial", 9),
        fg="gray"
    ).pack(anchor="w")
    
    tk.Label(
        instructions_frame, 
        text="2. Then select and process your video file",
        font=("Arial", 9),
        fg="gray"
    ).pack(anchor="w")
    
    tk.Label(
        instructions_frame, 
        text="3. Output videos will be saved in the 'output' folder",
        font=("Arial", 9),
        fg="gray"
    ).pack(anchor="w")

    # Status bar
    status_frame = tk.Frame(root)
    status_frame.pack(side="bottom", fill="x", padx=5, pady=5)
    
    tk.Label(
        status_frame,
        text="Ready | Python 3.9+ | PyCharm Compatible",
        font=("Arial", 8),
        fg="darkgray"
    ).pack()

    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()