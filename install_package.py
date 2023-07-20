import platform
import subprocess
import sys

# List of required Python packages
REQUIRED_PACKAGES = [
    "numpy",
    "tabulate",
    "pyyaml",
]

def install_package(package_name):
    """
    Install the specified Python package using pip.

    Args:
        package_name (str): Name of the Python package to install.
    """
    print(f"Installing {package_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def main():
    # Get the current platform
    current_platform = platform.system()

    # Check for missing dependencies and install them if needed
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            install_package(package)

    print("All dependencies are installed and ready to use.")

if __name__ == "__main__":
    main()
