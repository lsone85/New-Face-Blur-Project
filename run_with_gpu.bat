@echo off
echo Activating virtual environment...
call "%~dp0.venv\Scripts\activate.bat"

echo Setting CUDA environment variables...
set "CUDA_PATH=%VIRTUAL_ENV%\Lib\site-packages\nvidia\cuda_runtime"
set "PATH=%VIRTUAL_ENV%\Lib\site-packages\nvidia\cudnn\bin;%VIRTUAL_ENV%\Lib\site-packages\nvidia\cublas\bin;%VIRTUAL_ENV%\Lib\site-packages\nvidia\cuda_runtime\bin;%VIRTUAL_ENV%\Lib\site-packages\nvidia\cufft\bin;%VIRTUAL_ENV%\Lib\site-packages\nvidia\cusolver\bin;%VIRTUAL_ENV%\Lib\site-packages\nvidia\cusparse\bin;%PATH%"

echo Running the application with GPU...
python "%~dp0run_face_blur.py" --version improved --gpu

pause
