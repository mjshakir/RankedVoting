#!/bin/bash

# Install the software-properties-common package to manage independent software vendor (ISV) applications
sudo apt-get install software-properties-common

# Add the deadsnakes PPA to your system's software repository list
sudo add-apt-repository ppa:deadsnakes/ppa

# Update your system's package list
sudo apt-get update

# Check for Python 3 and install if necessary
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed"
else
    echo "Python 3 is not installed"
    echo "Installing Python 3..."
    sudo apt-get install python3.10
fi

# Check for pip and install if necessary
if command -v pip3 &>/dev/null; then
    echo "pip is installed"
else
    echo "pip is not installed"
    echo "Installing pip..."
    sudo apt-get install python3-pip
fi

# Install Python packages from requirements.txt
echo "Installing required Python packages..."
pip3 install -r requirements.txt
