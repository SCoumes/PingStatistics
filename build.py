import PyInstaller.__main__
import shutil
import os
import platform

# Build on windows
if platform.system() == "Windows":
    windows_build_dir = os.path.join("dist","PinStater_v1.0_windows")
    if os.path.exists(windows_build_dir):
        shutil.rmtree(windows_build_dir)
    # Run PyInstaller to create the executable
    PyInstaller.__main__.run([
        "main.py",
        "--onefile",
        "--noconsole",
        "--name",
        "PingStater",
        "--icon=icon.ico"
    ])
    # Create a zip file containing the executable and other relevant files for the windows build
    os.makedirs(windows_build_dir)
    shutil.copy(os.path.join("dist","PingStater.exe"), windows_build_dir)
    shutil.copy("icon.png", windows_build_dir)
    shutil.copy(os.path.join("Licenses","Release_license_text.txt"), os.path.join(windows_build_dir,"LICENSE.txt"))
    shutil.copy("README.md", windows_build_dir)
    shutil.make_archive(windows_build_dir, 'zip', windows_build_dir)

# Build on linux
elif platform.system() == "Linux":
    linux_build_dir = os.path.join("dist","PingStater_v1.0_linux")
    if os.path.exists(linux_build_dir):
        shutil.rmtree(linux_build_dir)
    # Run PyInstaller to create the executable
    PyInstaller.__main__.run([
        "main.py",
        "--onefile",
        "--noconsole",
        "--name",
        "PingStater",
    ])
    # Create a tarball file containing the executable and other relevant files for the linux build
    os.makedirs(linux_build_dir)
    shutil.copy(os.path.join("dist","PingStater"), linux_build_dir)
    shutil.copy("icon.png", linux_build_dir)
    shutil.copy(os.path.join("Licenses","Release_license_text.txt"), os.path.join(linux_build_dir,"LICENSE.txt"))
    shutil.copy("README.md", linux_build_dir)
    shutil.make_archive(linux_build_dir, 'gztar', linux_build_dir)

else:
    print("Compilation only supports windows and linux. It seems you are not running either platform. Perhaps run the python code directly?")