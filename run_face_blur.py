#!/usr/bin/env python
"""
Face Blur Application Launcher

This script provides a simple command-line interface to run the face blur application
with different options and modes, including selecting between different versions
and enabling/disabling GPU acceleration.
"""

import os
import sys
import argparse
import importlib.util
import subprocess
import platform

def check_module_installed(module_name):
    """Check if a Python module is installed."""
    return importlib.util.find_spec(module_name) is not None

def get_script_path(script_name):
    """Get the absolute path to a script in the current directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), script_name))

def install_requirements():
    """Install required packages."""
    try:
        requirements_path = get_script_path("requirements.txt")
        print(f"Installing required packages from {requirements_path}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        return True
    except subprocess.CalledProcessError:
        print("Error installing requirements. Please install them manually using:")
        print(f"pip install -r {requirements_path}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run Face Blur Application")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU acceleration (if available)")
    parser.add_argument("--cpu", action="store_true", help="Force CPU mode even if GPU is available")
    parser.add_argument("--install", action="store_true", help="Install requirements before running")
    
    args = parser.parse_args()
    
    # Install requirements if requested
    if args.install:
        success = install_requirements()
        if not success:
            print("Continuing anyway, but the application may not work properly.")
    
    script_name = "improved_face_blur_app.py"
    script_path = get_script_path(script_name)
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found")
        return
    
    # Set environment variable for GPU/CPU
    env = os.environ.copy()
    
    cmd = [sys.executable, script_path]
    
    # Process GPU/CPU flags
    if args.cpu:
        # Force CPU mode
        env["CUDA_VISIBLE_DEVICES"] = "-1"
        cmd.append("--cpu")
        print("Forcing CPU mode - GPU will not be used")
    elif args.gpu:
        # Try to enable GPU
        cmd.append("--gpu")
        print("GPU acceleration enabled")
    
    # Run the application
    print(f"Running {script_name}...")
    subprocess.call(cmd, env=env)

if __name__ == "__main__":
    main()
