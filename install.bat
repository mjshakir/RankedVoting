@echo off
py -3.10 -V >nul 2>&1 || (
    echo Python 3.10 is not installed.
    echo Installing Python 3.10...
    powershell -Command "iwr https://www.python.org/ftp/python/3.10.1/python-3.10.1-amd64.exe -OutFile python3.10.1-amd64.exe"
    python3.10.1-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python3.10.1-amd64.exe
)
pip -V >nul 2>&1 || (
    echo pip is not installed.
    echo Installing pip...
    py -3.10 -m ensurepip --upgrade
)
echo Installing required Python packages...
py -3.10 -m pip install -r requirements.txt