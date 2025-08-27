#!/bin/bash
# Setup script for Face Blur Project on Linux/macOS
# Compatible with Python 3.9+ and PyCharm 2024.2.6

echo "=== Face Blur Project Setup Script ==="
echo "Setting up for Python 3.9+ and PyCharm compatibility"

# Check if Python 3.9+ is available
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ $(echo "$PYTHON_VERSION < $REQUIRED_VERSION" | bc -l 2>/dev/null || echo "0") -eq 1 ]; then
    echo "Warning: Python version $PYTHON_VERSION is less than required $REQUIRED_VERSION"
    echo "Consider upgrading to Python 3.9 or higher for best compatibility"
fi

echo "Python version: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install tkinter if on Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux. Checking for tkinter..."
    python3 -c "import tkinter" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "tkinter not found. Please install it manually:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
        echo "  CentOS/RHEL: sudo yum install tkinter"
        echo ""
        echo "After installing tkinter, re-run this script."
    else
        echo "tkinter is available"
    fi
fi

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Setup completed successfully!"
    echo ""
    echo "To run the application:"
    echo "  1. Activate the virtual environment: source venv/bin/activate"
    echo "  2. Run the application: python main.py"
    echo ""
    echo "To run in PyCharm:"
    echo "  1. Open the project folder in PyCharm 2024.2.6"
    echo "  2. Configure Python interpreter to use: ./venv/bin/python"
    echo "  3. Run main.py"
    echo ""
    echo "Test compatibility: python test_compatibility.py"
else
    echo "Error: Failed to install dependencies"
    echo "Check the error messages above and resolve any issues"
    exit 1
fi