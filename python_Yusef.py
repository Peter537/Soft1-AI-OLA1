import os
import csv
import pkg_resources
import subprocess

required_packages = [
    'numpy',
    'pandas',
    'scikit-learn',
    'matplotlib',
    'seaborn'
]

def check_and_install_packages():
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    csv_file = "hasInstalled.csv"
    
    # Create or read existing CSV file
    package_status = {}
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    package_status[row[0]] = row[1]
    
    # Check and install packages
    for package in required_packages:
        if package not in package_status or package_status[package] != "installed":
            if package in installed_packages:
                package_status[package] = "installed"
                print(f"{package} is already installed")
            else:
                try:
                    print(f"Installing {package}...")
                    subprocess.check_call(['pip', 'install', package], stdout=subprocess.DEVNULL)
                    package_status[package] = "installed"
                    print(f"Successfully installed {package}")
                except subprocess.CalledProcessError:
                    package_status[package] = "failed"
                    print(f"Failed to install {package}")
    
    # Write updated status to CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for package, status in package_status.items():
            writer.writerow([package, status])