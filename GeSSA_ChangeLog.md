# CHANGE LOG
## GeSSA - GeoRiskA Scanning Software for Airphotos

**Last Update = 2/02/2024**  

### IMPORTANT NOTICE
The current version(s) of GeSSA should still be considered as beta version(s), as no extensive use or application outside of the AfricaMuseum has been performed.   

### TO DO LIST
- [x] Ensure that a terminal opens when GeSSA is launched.  --> "Terminal=true" in the .desktop file (29/02/2024)
- [ ] Get the setup section out of the main Python script, to make changes easier for non-coders
- [ ] Write down a detailed user guide including installation, use, and best practices  
- [ ] Be more autonomous for the tkinter theme that is used. 
  
---------------------

### Version 0.1.6  (normal + lite versions) – 29/02/2024  
- [x] Prevent overwriting of an image it already exists (even if already implemented)   
- [x] Creation of a Lite version, without transparency option, developed specifically for EPSON A3 scanners (to avoid compatibility issues)  
- [x] Removed unnecessary information in the text of the header   

### Version 0.1.5 – 1/09/2023  
- [x] Add the possibility to select paper photo and slide (transparency). [Does not work properly for A3 scanners]  
- [x] Debug the resolution selection when SCAN is pressed.  
- [x] Add a warmup function and button for glass plates (not same scan light).  
- [x] Optimise position of action buttons (incl. 2-line text label).  

### Version 0.1.4 – 31/08/2023  
- [x] Allow user to define default save directory in setup section.  
- [x] Print time spent to scan in console/terminal.  
- [x] When "scan successfully performed" printed, specify which scanner    
- [x] Change colour of WARMUP and PREVIEW buttons.  
- [x] Automatically create a scanlog CSV file with all info on the scan.  
- [x] Preview function opens the image preview file after scanning.  

### Version 0.1.2 – 28/08/2023  
- [x] Create the warmup function   
- [x] Create the preview function  
- [x] Allow user to define default save directory in setup section   
- [x] Prevent overwriting of an image it already exists   
- [x] Make the SCAN button blue and not gray    

### Version 0.1.1 – 25/08/2023 
- [x] Allow running scanners in parallel   
