"""
------------------------------------------------------------------------------
GeSSA - GEORISKA SCANNING SOFTWARE FOR AIRPHOTOS
(c) Royal Museum for Central Africa - 2021-2024
------------------------------------------------------------------------------

##############################################################################
##########                    CONFIGURATION FILE                    ##########
##############################################################################

PLEASE ADAPT THE FOLLOWING VARIABLES TO YOUR COMPUTER USED BEFORE USING GeSSA

GeSSA repository:
        https://github.com/GeoRiskA/GeSSA
"""

# Hardware info and setup
# =======================

organisation = "Name of your organisation"
computer_used = "Your computer name"

scanner_model = "Epson Perfection v850 series"  # Name of the scanner model
vendor_ID = '0x04b8'
product_ID = '0x0151'
# The vendor and product IDs can be retrieved using the "lsusb" command in a terminal
# The scanner ID will be XXXX:YYYY, with XXXX being the vendor ID and YYYY the product ID
# Just add "0x" before the 4 digits

nbr_of_scanners_expected = 8

# Scanning default parameters
# ===========================

format_file = "tiff"  # tiff|png|jpeg
mode = "gray"  # lineart|gray|color
depth = 16  # 8|12|14|16
l = 0  # Top-left x position of scan area (in mm).
t = 0  # Top-left y position of scan area (in mm).
x = 215.9  # Width of scan-area (in mm).
y = 200  # Height of scan-area (in mm).
brightness = 0  # -2|-1|0|1|2

# Manual folder selection
scanning_folder = "/home/user/Desktop"
warmup_folder = "/home/user/Desktop"

# Fix the path to the scans
path = scanning_folder
# path=os.getcwd() # Use this path to save scans in the folder opened in the terminal

resolutionList = ["0", "100", "200", "300", "400", "600", "800", "900", "1200", "1600", "1800", "2400", "3200", "4800",
                  "6400", "9600", "12800"]
# 50|60|72|75|80|90|100|120|133|144|150|160|175|180|200|216|240|266|300|320|350|360|400|480|600|720|800|900|1200|1600|1800|2400|3200|4800|6400|9600|12800

max_subframe_per_row = 4
# = maximum number of sets of scanner parameters that can be aligned horizontally in the GUI

# System CPU organization
# =======================

nb_cores = multiprocessing.cpu_count() - 4

# Location of the tkinter theme
# ======usb <vendor ID> <product ID>=======================
used_theme = "/home/user/Desktop/MASS_SCANNING/ttk_Theme/sun-valley.tcl"  # Available for download here: https://github.com/rdbende/Sun-Valley-ttk-theme

# Options for testing and debugging (you should not play with these options)
# ==========================================================================
warmup_test = False  # If True, the warmup images will be saved in the designated folder
warmup_resolution_test = "600"  # Resolution for the warmup images (in dpi) when tested