#!/home/risnat/miniconda3/envs/scan/bin/python

# !!! Adapt the shebang to the computer you are using !!!

"""
------------------------------------------------------------------------------
GeSSA - GEORISKA SCANNING SOFTWARE FOR AIRPHOTOS
(c) Royal Museum for Central Africa - 2021-2024
------------------------------------------------------------------------------

Version: 0.1.6 (remains a BETA version on which I work)

Author(s):
        - Prof. Dr. Benoît SMETS
          Royal Museum for Central Africa (MRAC-KMMA, BELGIUM)
          Vrije Universiteit Brussel (VUB, BELGIUM)

Repository: 
        Not stored on a GitHub repository yet.

Notes:
    - Please, first read the installation instructions and modify the SETUP
      section before using this script!
    - This python script is based on the initial work of:
        * Augustin COSSON (ENSG, internship at RMCA during Summer 2021)
        * Antoine DILLE (RMCA - former tkinter interface, Dec. 2021)

Requirements:
    - Computer with Ubuntu 22.04 (or any recent Debian-based Linux distro)
    - Similar models of flat-bed scanners; coming from the same manufacturer
    - Admin rights on your computer to install software and libraries

Changelog:
    - See file "GESSA_ChangeLog.md"
"""
SOFT_NAME = "GeoRiskA Scanning Software for Airphotos (GeSSA)"
VERSION = "0.1.6"
DATE = "29/02/2024"
AUTHOR = "B. Smets"
AFFILIATIONS = "MRAC-KMMA / VUB"
COPYRIGHTING = "(c) Royal Museum for Central Africa / Vrije Universiteit Brussel, 2023-2024"

##############################################################################
##########                      1. LIBRARIES                        ##########
##############################################################################

# Processing libraries
import multiprocessing
import os
import subprocess
import concurrent.futures
import usb1
import glob
import shutil
import time
import csv

# Interface libraries
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog 


##############################################################################
##########                        2. SETUP                          ##########
##############################################################################

# !!! SECTION TO HARDCODE ANYTIME IT IS INSTALLED ON A NEW COMPUTER !!!

# Hardware info and setup
# =======================

organisation = "Name of your organisation"
computer_used = "Your computer name"

scanner_model = "Epson Perfection v850 series" # Name of the scanner model
vendor_ID = '0x04b8'
product_ID = '0x0151'
    # The vendor and product IDs can be retrieved using the "lsusb" command in a terminal
    # The scanner ID will be XXXX:YYYY, with XXXX being the vendor ID and YYYY the product ID
    # Just add "0x" before the 4 digits

nbr_of_scanners_expected = 8

# Scanning default parameters
# ===========================

format_file="tiff"    # tiff|png|jpeg
mode="gray"     # lineart|gray|color
depth=16        # 8|12|14|16
l=0             # Top-left x position of scan area (in mm).
t=0             # Top-left y position of scan area (in mm).
x=215.9         # Width of scan-area (in mm).
y=200           # Height of scan-area (in mm).
brightness=0    # -2|-1|0|1|2     

# Manual folder selection
scanning_folder = "/home/user/Desktop"
warmup_folder = "/home/user/Desktop"

# Fix the path to the scans
path = scanning_folder
#path=os.getcwd() # Use this path to save scans in the folder opened in the terminal

resolutionList = ["0","100","200","300","400","600","800","900","1200","1600","1800","2400","3200","4800","6400","9600","12800"]
#50|60|72|75|80|90|100|120|133|144|150|160|175|180|200|216|240|266|300|320|350|360|400|480|600|720|800|900|1200|1600|1800|2400|3200|4800|6400|9600|12800

max_subframe_per_row = 4
   # = maximum number of sets of scanner parameters that can be aligned horizontally in the GUI

# System CPU organization
# =======================

nb_cores=multiprocessing.cpu_count()-4

# Location of the tkinter theme
# ======usb <vendor ID> <product ID>=======================
used_theme = "/home/user/Desktop/MASS_SCANNING/ttk_Theme/sun-valley.tcl" # Available here: https://github.com/rdbende/Sun-Valley-ttk-theme

####################             END OF SETUP             ####################
##############################################################################

# Printing initial information in the console/terminal
print("\nrepertoire :",os.getcwd())
print("\nCores used for the scanners :",nb_cores)
print("Cores used for linux system :",multiprocessing.cpu_count()-nb_cores,"\n")
print(" ")
print(" ")
print("================================================================")
print("        GeSSA - GeoRiskA Scanning Software for Airphotos        ")
print("================================================================")
print(f"Version: {VERSION} ({DATE})")
print(f"(c) {AUTHOR} - {AFFILIATIONS}")
print(" ")
print(f"CONFIGURATION MADE FOR: {organisation}")
print(f"COMPUTER: {computer_used}")
print(f"SCANNER MODEL: {scanner_model}")
#print(dict(os.environ))
print(" ")
print(" ")


##############################################################################
##########                      3. FUNCTIONS                        ##########
##############################################################################

# 3.1. CHECKING CONNECTED SCANNERS AND LINKING THEM
# =================================================

class Scanner:
    def __init__(self, device, nickname):
        self.device = device
        self.nickname = nickname
        self.bus_number = device.getBusNumber()
        self.device_address = device.getDeviceAddress()
        self.libsane_name = f"epson2:libusb:{self.bus_number:03d}:{self.device_address:03d}"
    
    def __str__(self):
        return f"{self.nickname}: {self.libsane_name} (Bus: {self.bus_number}, Device: {self.device_address})"

def list_usb_scanners(vendor_id, product_id):
    context = usb1.USBContext()
    
    scanner_list = []
    
    try:
        devices = context.getDeviceList(skip_on_error=True)
        for device in devices:
            if device.getVendorID() == int(vendor_id, 16) and device.getProductID() == int(product_id, 16):
                scanner_list.append(device)
    except usb1.USBErrorNotFound:
        pass
    
    return scanner_list

# Replace these with the desired vendor ID and product ID in hexadecimal format
desired_vendor_id = vendor_ID
desired_product_id = product_ID

scanners = list_usb_scanners(desired_vendor_id, desired_product_id)

if scanners:
    print("Detected USB-connected scanners")
    print("-------------------------------")
    print(" ")
    scanner_nbr = len(scanners)
    print(f"Number of scanners matching the criteria = {scanner_nbr} devices")
    print(f"Number of scanners expected = {nbr_of_scanners_expected}")
    if scanner_nbr == nbr_of_scanners_expected:
        print("   --> We are good to go!")
    else:
        print("!!!!!!!!!!")
        print("   CAUTION: the number of scanners detected does not match the number of scanners expected")
        print("!!!!!!!!!!")
    print(" ")
    print("Scanner details: ")
    print(" ")
    scanner_instances = []
    for index, device in enumerate(scanners, start=1):
        nickname = f"SCANNER_{index}"
        scanner_instances.append(Scanner(device, nickname))
        print(scanner_instances[-1])  # Print the scanner instance details
        print(" ")

else:
    print("-----------------------------------------")
    print("No matching USB-connected scanners found.")
    print("-----------------------------------------")
    print(" ")

print("================================================================")
print(" ")

list_devices_name = scanners
device_count = len(scanners)

# 3.2. ROOT FUNCTIONS
# ===================

# CHOOSE FOLDER FUNCTION

def choose_folder():
    global save_directory_var
    selected_directory = filedialog.askdirectory()
    save_directory_var.set(selected_directory)

# SCAN FUNCTION
scantype_List = ["nothing", "photo", "glass"]

def scan(scanner_name, scanner_nickname, scantype, resolution, image_name, width, height, left, top, format_image, save_directory):
    global mode, depth, brightness  # Specify that you're using the global variables
    
    if format_file == "tiff":
        suffix = ".tif"
    elif format_file == "png":
        suffix = ".png"
    elif format_file == "jpeg":
        suffix = ".jpg"
    
    selected_path = f"{save_directory}/{image_name}{suffix}"
    
    if scantype == 'photo':
        scansource = 'Flatbed'
        selected_width = width
    elif scantype == 'glass':
        scansource = 'TPU8x10'
        selected_width = 203.2
    else:
        scansource = 'Flatbed'
        selected_width = width
    
    # Check if the file name already exists
    existing_files = os.listdir(save_directory)
    for filename in existing_files:
        if filename.endswith(suffix) and image_name in filename:
            # If yes, increment the filename with a copy number
            current_copy_number = 1
            new_filename = f"{image_name}_{current_copy_number}{suffix}"

            while new_filename in existing_files:
                current_copy_number += 1
                new_filename = f"{image_name}_{current_copy_number}{suffix}"

            # Update the file path with the new filename
            selected_path = f"{save_directory}/{new_filename}"
    
    command = [
        "scanimage",
        f"--device={scanner_name}",
        f"--brightness={brightness}",
        f"-l {left}",                # !!! No "=" for this argument
        f"-t {top}",                 # !!! No "=" for this argument
        f"-x {selected_width}",               # !!! No "=" for this argument
        f"-y {height}",              # !!! No "=" for this argument
        "--progress",
        f"--format={format_image}",
        f"--mode={mode}",
        f"--depth={depth}",
        f"--resolution={resolution}",
        f"--output-file={selected_path}",
        f"--source={scansource}"
    ]
    
    try:
        print(f"{scanner_nickname}")
        print("Executing command:", " ".join(command))
        print(" ")
        process = subprocess.run(command, capture_output=True, check=True)
        
        if process.returncode == 0:
            print(" ")
            print(f"--> SCAN SUCCESSFULLY PERFORMED ({scanner_nickname})")
        else:
            print (" ")
            print(f"--> SCAN FAILED ({scanner_nickname}) - Error message:")
            print(process.stderr)
            print(" ")
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
        print(" ")

    # Create and save scan log information
    scanlog = []
    current_scantime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    scanlog.append([image_name, current_scantime, save_directory, scanner_nickname])
    
    csv_logfile = os.path.join(save_directory, "_SCANLOG.csv")
    csv_exists = os.path.exists(csv_logfile)
    
    with open(csv_logfile, "a", newline="") as f:
        csv_writer = csv.writer(f)
        if not csv_exists:
            csv_writer.writerow(["Image_name", "Scan_datetime", "Save_directory", "scanner_name"])
        csv_writer.writerows(scanlog)

# PREVIEW FUNCTION

def preview(scanner_name, scanner_nickname, preview_image_name, width, height, left, top, scantype, preview_folder):
    global mode, depth, brightness  # Specify that you're using the global variables
    
    suffix = ".png"
    preview_path = f"{preview_folder}/{preview_image_name}{suffix}"
    preview_resolution = "100"
    
    if scantype == 'photo':
        scansource = 'Flatbed'
        selected_width = width
    elif scantype == 'glass':
        scansource = 'TPU8x10'
        selected_width = 203.2
    else:
        scansource = 'Flatbed'
        selected_width = width

    preview_command = [
        "scanimage",
        f"--device={scanner_name}",
        f"--brightness={brightness}",
        f"-l {left}",                # !!! No "=" for this argument
        f"-t {top}",                 # !!! No "=" for this argument
        f"-x {selected_width}",      # !!! No "=" for this argument
        f"-y {height}",              # !!! No "=" for this argument
        "--progress",
        "--format=png",
        f"--mode={mode}",
        f"--depth={depth}",
        f"--resolution={preview_resolution}",
        f"--output-file={preview_path}",
        f"--source={scansource}"
    ]
    
    try:
        print(f"{scanner_nickname}")
        print("Executing command:", " ".join(preview_command))
        print(" ")
        process = subprocess.run(preview_command, capture_output=True, check=True)
        
        if process.returncode == 0:

            print(f"--> PREVIEW SUCCESSFULLY PRODUCED ({scanner_nickname})")
            print(" ")
            subprocess.run(["xdg-open", preview_path])
        else:
            print(f"--> PREVIEW SCAN FAILED ({scanner_nickname}) - Error message:")
            print(" ")
            print(process.stderr)
            print(" ")
    except subprocess.CalledProcessError as e:
#        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        print("An error occurred:", e)
        print(" ")

# WARMUP FUNCTIONS

# For paper media
def warmup_photo(scanner_name, warmup_image_name, warmup_temp_folder):
    global mode, depth, brightness  # Specify that you're using the global variables
    
    iterations = 10
    
    suffix = ".png"
    warmup_path = f"{warmup_temp_folder}/{warmup_image_name}{suffix}"
    warmup_resolution = "600"
    
    # Check if the warmup file name already exists
    existing_warmup_files = os.listdir(warmup_temp_folder)
    for filename in existing_warmup_files:
        if filename.endswith(suffix) and warmup_image_name in filename:
            # If yes, increment the filename with a copy number
            current_copy_number = 1
            new_warmup_filename = f"{warmup_image_name}_{current_copy_number}{suffix}"

            while new_warmup_filename in existing_warmup_files:
                current_copy_number += 1
                new_warmup_filename = f"{warmup_image_name}_{current_copy_number}{suffix}"

            # Update the file path with the new filename
            selected_path = f"{warmup_temp_folder}/{new_warmup_filename}"
    
    warmup_command = [
        "scanimage",
        f"--device={scanner_name}",
        f"--brightness={brightness}",
        "--progress",
        "--format=png",
        f"--mode={mode}",
        f"--depth={depth}",
        f"--resolution={warmup_resolution}",
        f"--output-file={warmup_path}"
    ]
    
    for i in range(1, iterations + 1):
        try:
            print("Executing command:", " ".join(warmup_command))
            process = subprocess.run(warmup_command, capture_output=True, check=True)
        
            if process.returncode == 0:
                print("--> WARMUP ITERATION DONE SUCCESSFULLY")
                print(" ")
            else:
                print("--> WARMUP FAILED - Error message:")
                print(" ")
                print(process.stderr)
        except subprocess.CalledProcessError as e:
            print("An error occurred:", e)
            print(" ")

# For glass plates
def warmup_glass(scanner_name, warmup_image_name, warmup_temp_folder):
    global mode, depth, brightness  # Specify that you're using the global variables
    
    iterations = 5
    
    suffix = ".png"
    warmup_path = f"{warmup_temp_folder}/{warmup_image_name}{suffix}"
    warmup_resolution = "600"

    # Check if the warmup file name already exists
    existing_warmup_files = os.listdir(warmup_temp_folder)
    for filename in existing_warmup_files:
        if filename.endswith(suffix) and warmup_image_name in filename:
            # If yes, increment the filename with a copy number
            current_copy_number = 1
            new_warmup_filename = f"{warmup_image_name}_{current_copy_number}{suffix}"

            while new_warmup_filename in existing_warmup_files:
                current_copy_number += 1
                new_warmup_filename = f"{warmup_image_name}_{current_copy_number}{suffix}"

            # Update the file path with the new filename
            selected_path = f"{warmup_temp_folder}/{new_warmup_filename}"
    
    warmup_glass_command = [
        "scanimage",
        f"--device={scanner_name}",
        f"--brightness={brightness}",
        "--progress",
        "--format=png",
        f"--mode={mode}",
        f"--depth={depth}",
        f"--resolution={warmup_resolution}",
        f"--output-file={warmup_path}",
        "--source=TPU8x10"
    ]
    
    for i in range(1, iterations + 1):
        try:
            print("Executing command:", " ".join(warmup_glass_command))
            process = subprocess.run(warmup_glass_command, capture_output=True, check=True)
        
            if process.returncode == 0:
                print("--> WARMUP ITERATION DONE SUCCESSFULLY")
                print(" ")
            else:
                print("--> WARMUP FAILED - Error message:")
                print(" ")
                print(process.stderr)
        except subprocess.CalledProcessError as e:
            print("An error occurred:", e)
            print(" ")


# 3.3. ACTION FUNCTIONS
# =====================

# RUN SCAN FOR SELECTED SCANNER(S)

# First, function to avoid overwriting a filename
def generate_unique_filename(base_name, directory):
    suffix = ""
    count = 0
    new_name = base_name
    while os.path.exists(os.path.join(directory, new_name + suffix)):
        count += 1
        suffix = f"_{count}"
        new_name = base_name + suffix
    return new_name

# Then, the run function
def run_selected_scanners():
    format_image = format_file
    save_directory = save_directory_var.get()
    scanner_infos = []  # List to store scanner info tuples

    for scanner_info in scanner_vars:
        scanner_var, scanner_instance, scantype_var, resolution_var, image_name_var, width_var, height_var, left_var, top_var = scanner_info

        if scanner_var.get():
            image_name = image_name_var.get()
            scantype = scantype_var.get()
            resolution = resolution_var.get()
            width = width_var.get()
            height = height_var.get()
            left = left_var.get()
            top = top_var.get()
            
            scanner_infos.append((scanner_instance.libsane_name, scanner_instance.nickname, scantype, resolution, image_name, width, height, left, top, format_image, save_directory))
    
    # Record start time
    start_time = time.time()
    
    # Create a ThreadPoolExecutor with the maximum number of workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(scanner_infos)) as executor:
        # Use the map function to apply the scan function to each scanner info tuple
        results = executor.map(lambda args: scan(*args), scanner_infos)

    # You can optionally process the results if needed
    for result in results:
        pass
    
    # Calculate and display elapsed time
    elapsed_time = time.time() - start_time
    print(" ")
    print(f"Scan processing time = {elapsed_time: .2f} seconds")
    print(" ")

# RUN PREVIEW FOR SELECTED SCANNER(S)

def preview_selected():
    save_directory = save_directory_var.get()
    preview_folder = os.path.join(save_directory, "Preview")
    
    # Create the 'Preview' folder if it doesn't exist
    if not os.path.exists(preview_folder):
        os.makedirs(preview_folder)
    
    scanner_infos = []  # List to store scanner info tuples

    for scanner_info in scanner_vars:
        scanner_var, scanner_instance, scantype_var, _, image_name_var, width_var, height_var, left_var, top_var = scanner_info

        if scanner_var.get():
            image_name = image_name_var.get()
            scantype = scantype_var.get()
            width = width_var.get()
            height = height_var.get()
            left = left_var.get()
            top = top_var.get()
            
            preview_image_name = f"preview_{image_name}"
            scanner_infos.append((scanner_instance.libsane_name, scanner_instance.nickname, preview_image_name, width, height, left, top, scantype, preview_folder))

    # Create a ThreadPoolExecutor with the maximum number of workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(scanner_infos)) as executor:
        # Use the map function to apply the scan function to each scanner info tuple
        results = executor.map(lambda args: preview(*args), scanner_infos)

    # You can optionally process the results if needed
    for result in results:
        pass

# RUN A WARMUP OF THE SELECTED SCANNERS, FOR PAPER PHOTOS

def warmup_photo_selected():
    global warmup_folder
    warmup_temp_folder = os.path.join(warmup_folder, "warmup_temp")
    
    # Create the 'warmup_temp' folder if it doesn't exist
    if not os.path.exists(warmup_temp_folder):
        os.makedirs(warmup_temp_folder)
    
    scanner_infos = []  # List to store scanner info tuples

    for scanner_info in scanner_vars:
        scanner_var, scanner_instance, _, _, _, _, _, _, _ = scanner_info

        if scanner_var.get():
            image_name = generate_unique_filename(f"warmup_{scanner_instance.nickname}", warmup_temp_folder)
            scanner_infos.append((scanner_instance.libsane_name, image_name, warmup_temp_folder))

    # Create a ThreadPoolExecutor with the maximum number of workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(scanner_infos)) as executor:
        # Use the map function to apply the scan function to each scanner info tuple
        results = executor.map(lambda args: warmup_photo(*args), scanner_infos)

    # You can optionally process the results if needed
    for result in results:
        pass
    
    # Delete the scanned warmup images after scanning
    for png_file in glob.glob(os.path.join(warmup_temp_folder, "*.png")):
        os.remove(png_file)
    
    # Remove the 'warmup_temp' folder
    shutil.rmtree(warmup_temp_folder)

# RUN A WARMUP OF THE SELECTED SCANNERS, FOR GLASS PLATES

def warmup_glass_selected():
    global warmup_folder
    warmup_temp_folder = os.path.join(warmup_folder, "warmup_temp")
    
    # Create the 'warmup_temp' folder if it doesn't exist
    if not os.path.exists(warmup_temp_folder):
        os.makedirs(warmup_temp_folder)
    
    scanner_infos = []  # List to store scanner info tuples

    for scanner_info in scanner_vars:
        scanner_var, scanner_instance, _, _, _, _, _, _, _ = scanner_info

        if scanner_var.get():
            image_name = generate_unique_filename(f"warmup_{scanner_instance.nickname}", warmup_temp_folder)
            scanner_infos.append((scanner_instance.libsane_name, image_name, warmup_temp_folder))

    # Create a ThreadPoolExecutor with the maximum number of workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(scanner_infos)) as executor:
        # Use the map function to apply the scan function to each scanner info tuple
        results = executor.map(lambda args: warmup_glass(*args), scanner_infos)

    # You can optionally process the results if needed
    for result in results:
        pass
    
    # Delete the scanned warmup images after scanning
    for png_file in glob.glob(os.path.join(warmup_temp_folder, "*.png")):
        os.remove(png_file)
    
    # Remove the 'warmup_temp' folder
    shutil.rmtree(warmup_temp_folder)


##############################################################################
##########               4. GRAPHICAL USER INTERFACE                ##########
##############################################################################

# 4.1. CREATE THE MAIN WINDOW
# ===========================

root = tk.Tk()  
root.title(f"{SOFT_NAME} - v. {VERSION}")

# Set appearence theme
root.tk.call("source", used_theme) # See setup section for the selection of the theme
root.tk.call("set_theme", "light") #light or dark theme
root.option_add('*Font', 'TkMenuFont') #define font

# 4.2. CREATE AND ARRANGE SUBFRAMES FOR EACH CONNECTED SCANNER
# ===========================================================

default_save_directory = path
save_directory_var = tk.StringVar(value=default_save_directory)

scanner_vars = []

current_row = 0
current_column = 0

for scanner_instance in scanner_instances:
    subframe = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
    subframe.grid(row=current_row, column=current_column, padx=5, pady=5)

    scanner_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(subframe, text=scanner_instance.nickname, variable=scanner_var).pack(anchor="w")
    
    scantype_var = tk.StringVar()
    scantype_label = ttk.Label(subframe, text="Scan type:")
    scantype_label.pack(anchor="w")
    ttk.OptionMenu(subframe, scantype_var, *scantype_List).pack(anchor="w")
    scantype_var.set(scantype_List[1])

    resolution_var = tk.StringVar()
    resolution_label = ttk.Label(subframe, text="Resolution:")
    resolution_label.pack(anchor="w")
    ttk.OptionMenu(subframe, resolution_var, *resolutionList).pack(anchor="w")
    resolution_var.set(resolutionList[9])

    image_name_var = tk.StringVar()
    ttk.Label(subframe, text="Image Name:").pack(anchor="w")
    ttk.Entry(subframe, textvariable=image_name_var).pack(anchor="w")

    width_var = tk.StringVar(value=x)
    ttk.Label(subframe, text="Width:").pack(anchor="w")
    ttk.Entry(subframe, textvariable=width_var).pack(anchor="w")

    height_var = tk.StringVar(value=y)
    ttk.Label(subframe, text="Height:").pack(anchor="w")
    ttk.Entry(subframe, textvariable=height_var).pack(anchor="w")

    left_var = tk.StringVar(value=l)
    ttk.Label(subframe, text="Left:").pack(anchor="w")
    ttk.Entry(subframe, textvariable=left_var).pack(anchor="w")

    top_var = tk.StringVar(value=t)
    ttk.Label(subframe, text="Top:").pack(anchor="w")
    ttk.Entry(subframe, textvariable=top_var).pack(anchor="w")
    
    scanner_vars.append((scanner_var, scanner_instance, scantype_var, resolution_var, image_name_var, width_var, height_var, left_var, top_var))

    current_column += 1
    if current_column >= max_subframe_per_row:
        current_row += 1
        current_column = 0


# 4.3. CREATE BUTTONS TO SELECT FOLDER AND TRIGGER ACTIONS
# ========================================================

# Folder selection

choose_folder_button = ttk.Button(root, text="Choose Folder", command=choose_folder)
choose_folder_button.grid(row=current_row + 1, column=0, pady=10)

folder_label = ttk.Label(root, textvariable=save_directory_var)
folder_label.grid(row=current_row + 1, column=1, columnspan=2, pady=20)

# Action buttons

warmup_photo_button = ttk.Button(root, text="Warm Up (photos)", style='Accent.TButton', command=lambda: warmup_photo_selected())
warmup_photo_button.grid(row=current_row + 2, column=0, pady=10)

preview_button = ttk.Button(root, text="Preview Scan(s)", style='Accent.TButton', command=lambda: preview_selected())
preview_button.grid(row=current_row + 2, column=1, pady=10)

scan_button = ttk.Button(root, text="— SCAN —", style='Accent.TButton', command=lambda: run_selected_scanners())
scan_button.grid(row=current_row + 2, column=2, pady=10)

warmup_glass_button = ttk.Button(root, text="Warm Up \n(glass plates)", style='Accent.TButton', command=lambda: warmup_glass_selected())
warmup_glass_button.grid(row=current_row + 3, column=0, pady=10)

# 4.4. RUN THE APPLICATION
# ========================

root.mainloop()


#####################################################################################
############################  END OF INTERFACE ######################################
#####################################################################################

print(' ')
print(' ')
print('==========================')
print('  SCANNING SESSION ENDED  ')
print('==========================')
print(f"{COPYRIGHTING}")
print(' ')

#####################################################################################
##############################  END OF SCRIPT #######################################
#####################################################################################
