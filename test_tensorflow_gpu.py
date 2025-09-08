#!/usr/bin/env python
"""
TensorFlow GPU Test Script

This script tests if TensorFlow can detect and use your GPU.
It will provide detailed information about your GPU configuration
and run a small benchmark to verify it's working correctly.
"""

import os
import sys
import time
import argparse
import platform

# Parse command line arguments
parser = argparse.ArgumentParser(description="Test TensorFlow GPU detection and performance")
parser.add_argument("--cpu", action="store_true", help="Force CPU mode for comparison")
parser.add_argument("--verbose", action="store_true", help="Show detailed information")
args = parser.parse_args()

# Print system information
print("\n===== System Information =====")
print(f"Python version: {platform.python_version()}")
print(f"Platform: {platform.platform()}")

# Set environment variable to force CPU mode if requested
if args.cpu:
    print("\n===== Forcing CPU mode =====")
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Try to import TensorFlow
try:
    import tensorflow as tf
    print(f"\n===== TensorFlow {tf.__version__} =====")
    
    # Check CUDA build
    cuda_built = tf.test.is_built_with_cuda()
    print(f"Built with CUDA support: {cuda_built}")
    
    # Check if TensorFlow sees the GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"TensorFlow detects {len(gpus)} GPU(s):")
        for i, gpu in enumerate(gpus):
            print(f"  - GPU {i}: {gpu}")
            
        # Try to get more information about the GPU
        try:
            for i, gpu in enumerate(gpus):
                details = tf.config.experimental.get_device_details(gpu)
                print(f"  - GPU {i} details: {details}")
        except Exception as e:
            if args.verbose:
                print(f"Could not get device details: {str(e)}")
    else:
        print("No TensorFlow-compatible GPUs detected")
    
    # Check if CUDA is accessible
    try:
        device_name = tf.test.gpu_device_name()
        if device_name:
            print(f"Default GPU device: {device_name}")
        else:
            print("No default GPU device")
    except Exception as e:
        if args.verbose:
            print(f"Error getting GPU device name: {str(e)}")
    
    # Check environment variables
    print("\n===== Environment Variables =====")
    env_vars = ['CUDA_VISIBLE_DEVICES', 'CUDA_PATH', 'LD_LIBRARY_PATH', 
               'PATH', 'TF_FORCE_GPU_ALLOW_GROWTH', 'TF_GPU_THREAD_MODE']
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            if len(value) > 50 and not args.verbose:
                value = value[:50] + "..."
            print(f"{var}: {value}")
        elif args.verbose:
            print(f"{var}: Not set")
    
    # Run a simple test to verify GPU is working
    print("\n===== GPU Performance Test =====")
    print("Creating test tensors...")
    
    # Create some test data
    start_time = time.time()
    with tf.device('/CPU:0'):
        cpu_a = tf.random.normal([5000, 5000])
        cpu_b = tf.random.normal([5000, 5000])
        print(f"CPU tensor creation time: {time.time() - start_time:.2f} seconds")
    
    # Run operations on CPU
    start_time = time.time()
    with tf.device('/CPU:0'):
        cpu_result = tf.matmul(cpu_a, cpu_b)
    cpu_time = time.time() - start_time
    print(f"CPU matrix multiplication time: {cpu_time:.2f} seconds")
    
    # Check if GPU is available for the test
    if gpus and not args.cpu:
        # Configure for GPU
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except:
            print("Could not set memory growth (may be already configured)")
            
        # Run operations on GPU
        start_time = time.time()
        with tf.device('/GPU:0'):
            gpu_a = tf.random.normal([5000, 5000])
            gpu_b = tf.random.normal([5000, 5000])
            gpu_result = tf.matmul(gpu_a, gpu_b)
        # Force execution with sync
        _ = gpu_result.numpy()  
        gpu_time = time.time() - start_time
        print(f"GPU matrix multiplication time: {gpu_time:.2f} seconds")
        
        # Compare performance
        if cpu_time > 0 and gpu_time > 0:
            speedup = cpu_time / gpu_time
            print(f"GPU is {speedup:.1f}x faster than CPU")
            
            if speedup < 1.5:
                print("Warning: GPU performance is not significantly better than CPU.")
                print("This may indicate the GPU is not being utilized properly.")
            
except ImportError:
    print("TensorFlow not installed. Please install it with:")
    print("pip install tensorflow")
    sys.exit(1)
except Exception as e:
    print(f"Error during TensorFlow test: {str(e)}")
    if args.verbose:
        import traceback
        traceback.print_exc()

print("\nTest completed.")
