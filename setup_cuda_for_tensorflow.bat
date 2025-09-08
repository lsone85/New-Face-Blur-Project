@echo off
echo This script will set up TensorFlow with GPU support
echo in the project's virtual environment using the latest compatible versions.
echo.

:: Activate virtual environment
echo Activating virtual environment...
call "%~dp0\.venv\Scripts\activate.bat"

:: Clear existing TensorFlow and CUDA packages
echo Removing any existing TensorFlow and CUDA packages...
pip uninstall -y tensorflow tensorflow-intel tensorflow-gpu nvidia-cudnn-cu11 nvidia-cublas-cu11 nvidia-cuda-runtime-cu11 nvidia-cuda-nvrtc-cu11 nvidia-cufft-cu11 nvidia-cusolver-cu11 nvidia-cusparse-cu11

:: Install TensorFlow with CUDA support
echo Installing TensorFlow with CUDA...
pip install tensorflow[and-cuda]

:: Create a specialized test script
echo Creating GPU test script...
(
    echo import os
    echo import tensorflow as tf
    echo.
    echo print("TensorFlow version:", tf.__version__)
    echo print("GPU Available:", "Yes" if tf.config.list_physical_devices('GPU') else "No")
    echo print("GPU Devices:", tf.config.list_physical_devices('GPU'))
    echo print("Num GPUs Available:", len(tf.config.list_physical_devices('GPU')))
    echo try:
    echo     with tf.device('/GPU:0'):
    echo         a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    echo         b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    echo         c = tf.matmul(a, b)
    echo         print("GPU Test Result:", c)
    echo     print("GPU Test: SUCCESS")
    echo except RuntimeError as e:
    echo     print("GPU Test: FAILED")
    echo     print(e)
) > gpu_test.py

:: Run the test
echo.
echo Running GPU test...
python gpu_test.py

echo.
echo Setup complete. Please try running the application with GPU mode now.
pause
python gpu_test.py

echo.
echo Setup complete. Please try running the application with GPU mode now.
pause
