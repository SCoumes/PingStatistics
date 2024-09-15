import PyInstaller.__main__
import shutil
import os
import platform

version_numer = "1.1"

# Build on windows
if platform.system() == "Windows":
    windows_build_dir = os.path.join("dist",f"Pingstats_v{version_numer}_windows")
    if os.path.exists(windows_build_dir):
        shutil.rmtree(windows_build_dir)
    # Run PyInstaller to create the executable
    PyInstaller.__main__.run([
        "main.py",
        "--onefile",
        "--noconsole",
        "--name", "Pingstats",
        "--icon=pingstats.ico"
    ])
    # Create a zip file containing the executable and other relevant files for the windows build
    os.makedirs(windows_build_dir)
    shutil.copy(os.path.join("dist","Pingstats.exe"), windows_build_dir)
    shutil.copy("pingstats.png", windows_build_dir)
    shutil.copy(os.path.join("Licenses","Release_license_text.txt"), os.path.join(windows_build_dir,"LICENSE.txt"))
    shutil.copy("README.md", windows_build_dir)
    shutil.make_archive(windows_build_dir, 'zip', windows_build_dir)

# Build on linux
elif platform.system() == "Linux":
    linux_build_dir = os.path.join("dist",f"Pingstats_v{version_numer}_linux")
    if os.path.exists(linux_build_dir):
        shutil.rmtree(linux_build_dir)
    # Run PyInstaller to create the executable
    PyInstaller.__main__.run([
        "main.py",
        "--onefile",
        "--noconsole",
        "--name", "Pingstats",
        "--hidden-import", "PyQt6", # No clue why this is needed, but it is. The import is present at the top of multiples files in the code
    ])
    # Create a tarball file containing the executable and other relevant files for the linux build
    os.makedirs(linux_build_dir)
    shutil.copy(os.path.join("dist","Pingstats"), linux_build_dir)
    shutil.copy("pingstats.png", linux_build_dir)
    shutil.copy("install.sh", linux_build_dir)
    shutil.copy(os.path.join("Licenses","Release_license_text.txt"), os.path.join(linux_build_dir,"LICENSE.txt"))
    shutil.copy("README.md", linux_build_dir)
    shutil.make_archive(linux_build_dir, 'gztar', linux_build_dir)

else:
    print("Compilation only supports windows and linux. It seems you are not running either platform. Perhaps run the python code directly?")