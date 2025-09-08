import torch

def check_pytorch_gpu():
    """Checks for PyTorch GPU availability and prints details."""
    print(f"PyTorch version: {torch.__version__}")
    
    if torch.cuda.is_available():
        print("PyTorch CUDA is available.")
        print(f"Number of GPUs: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"    CUDA capability: {torch.cuda.get_device_capability(i)}")
    else:
        print("PyTorch CUDA is NOT available.")

if __name__ == "__main__":
    check_pytorch_gpu()
