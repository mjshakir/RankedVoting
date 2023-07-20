import subprocess

def install_dependencies():
    try:
        # Read the requirements.txt file
        with open('requirements.txt', 'r') as file:
            requirements = file.read().splitlines()
        
        # Install the dependencies using pip
        subprocess.check_call(['pip', 'install', *requirements])
        print("Dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")

if __name__ == "__main__":
    install_dependencies()
