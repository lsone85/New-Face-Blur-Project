import tkinter as tk
from tkinter import filedialog, messagebox
import os
from face_processing import process_video, add_to_whitelist

OUTPUT_DIR = "output"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def select_video():
    print("[DEBUG] select_video called", flush=True)
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if video_path:
        ensure_output_dir()
        output_path = filedialog.asksaveasfilename(defaultextension=".avi", initialdir=OUTPUT_DIR,
                                                   filetypes=[("AVI Video", "*.avi")])
        if output_path:
            success = process_video(video_path, output_path)
            if success:
                messagebox.showinfo("Done", f"Video exported to {output_path}")
            else:
                messagebox.showerror("Error", "Could not process video.")

def add_face():
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if img_path:
        add_to_whitelist(img_path)
        messagebox.showinfo("Success", "Face added to whitelist.")

def run_ui():
    root = tk.Tk()
    root.title("Face Blur App")

    tk.Label(root, text="Face Blur App", font=("Arial", 16)).pack(pady=10)

    btn_video = tk.Button(root, text="Select Video and Export", width=30, command=select_video)
    btn_video.pack(pady=10)

    btn_add_face = tk.Button(root, text="Add Face to Whitelist", width=30, command=add_face)
    btn_add_face.pack(pady=10)

    tk.Label(root, text="Whitelist images must be clear, front-facing faces.", fg="grey").pack(pady=5)
    root.mainloop()