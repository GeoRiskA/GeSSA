<div align="center">
	<img src="https://github.com/GeoRiskA/GeSSA/blob/main/GeSSA_logo_GUI.png">
</div> 

<h3 align="center">
<i>Speed-up airphoto digitising by parallelising flatbed photo-scanners!</i>
</h3>

<br>

*Version 0.2.0*  


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14145222.svg)](https://doi.org/10.5281/zenodo.14145222) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  

GeSSA is a software working on Linux computers allowing users to control several similar (i.e., same brand and model) flatbed scanners at the same time and perform parallelised scanning. This software has been developed with the unique idea of speeding-up the process of digitising paper-format historical aerial photographs to preserve their content and exploit them for scientific research.  

There are two versions of GeSSA:  
- **GeSSA:** Regular version of the software with options to scan paper, glass plate and film media.
- **GeSSA Lite:** simplified version of the software solely dedicated to paper photos. This version is compatible with scanners with less scanning options, such as A3 scanners.

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 

-------

***Software Creation, Management and Coordination:***  
- Prof. Dr. Benoît SMETS – Royal Museum for Central Africa (RMCA) / Vrije Universiteit Brussel (VUB) – BE  

***Contributors:***. 
- Mr. Augustin COSSON – Former student of ENSG-Géomatique – FR  
  > *Previous Python code that led to the creation of the first version of GeSSA*
- Dr. Antoine DILLE – Royal Museum for Central Africa (RMCA) — BE
  > *First version of the Tkinter interface*
- Mr. Toufik MOUSSOUNI — Royal Museum for Central Africa (RMCA) — BE
  > *Main beta tester and user of GeSSA, at the RMCA*

***Citation:*** *(in progress)*  

When using GeSSA or part of it, please cite the following references in you work:  

- ***The repository:*** Smets, B., 2024.  GeSSA — GeoRiskA Scanning Software for Airphotos, Version 0.2.0. DOI: https://doi.org/10.5281/zenodo.14145222
- ***The publication:*** *In preparation*

--------------

## INSTALLATION PROCEDURE  

GeSSA is a single Python file. To use it we highly recommend that you create a virtual environment dedicated to its use. Here is the installation procedure we propose using `conda`:  

1) Open a terminal on you Linux.
2) Install the SANE library. For Debian-based linux, use: `sudo apt install libsane`
3) Create a new "scan" environment: `conda create -n scan -c conda-forge python=3.12`
4) Activate your new virtual environment: `conda activate scan`
5) Install the required dependencies: `conda install libusb1 python-tk`
6) Download the GeSSA script you would like to use (i.e., "GeSSA" or "GeSSA_lite") and "GeSSA_config.py", and store the files on your computer wherever you like. (You can alternatively download the entire repository
7) Download the Tkinter theme for GeSSA [here](https://github.com/rdbende/Sun-Valley-ttk-theme), and save it in the folder where you stored GeSSA and GeSSA_config.
8) Open the GeSSA Python file in a text editor and do the following modification:
   - Adapt the shebang (first line) to your virtual environment (e.g., `#!/home/user/miniconda3/envs/scan/bin/python`)  
10) Make GeSSA executable. In your terminal, run `sudo chmod +x path/to/your/script/GeSSA_v0.x.y.py` *(replace the path with the one of GeSSA script saved on your computer)*  
11) In a text editor, create a .Desktop file as a shortcut to launch the script directly from the desktop (see [this procedure](https://github.com/GeoRiskA/GeSSA/blob/main/Desktop_logo/Example_Desktop_shortcut.md))  
12) Shutdown you computer, and connect via USB all your scanners to the computer.  
13) Turn on the scanners (all scanners must be the same model from the same brand). Once (and only once) they are all turned on, boot your computer.
14) Open the *GeSSA_config.py* file in a text editor and do the following modification:
   - Adapt the different variables according to your hardware configuration and your preferred scanning parameters  


## HOW TO RUN GeSSA  

To launch GeSSA, you have two options:
- You double-click on your .Desktop icon
- You open a terminal and run `python3 /path/to/your/script/GeSSA_v020.py` *(Adapt the path and GeSSA script name according to your configuration)*   

**BEFORE THE VERY FIRST SCANS WITH GeSSA:**  

Once GeSSA is ready to work for the first time, we need to identify which scanners will be Scanner 1, Scanner 2, etc. As scanner manufacturers do not provide a unique ID to each scanner of the same model, it is necessary to run a first scan to distinguish them. The easiest way is to follow this manual procedure:  

1) Switch on your scanners before booting the computer.  
2) Boot the computer.  
3) Place a sheet of paper in the scanner with the number you would like the scanner to have written on the paper.  
4) Launch GeSSA.py and scan the sheets of paper.  
5) Compare the scanner number in GeSSA with the number on the scanned image.  
6) Shutdown the computer and scanners.  
7) Replug the USB cables in the appropriate ports to fit with the paper numbers.  
8) Redo the steps 1) to 4) to check you did plug the USB cables in the appropriate corresponding ports.  

**BEFORE THE FIRST SCANS OF THE DAY:**  

Before any scanning session, **it is highly recommended to warmup the scanners**, eventhough manufacturers say otherwise. This is why a warmup button is available in GeSSA. This warmup will launch scans at low resolution several times, for all scanners, to be sure that the grayscale values in the scans remain relatively identical between scans. The scans performed during warmup are momentarily saved on the computer. They are deleted at the end of each warmup scan.

----------------

*&copy; Royal Museum for Central Africa / Vrije Universiteit Brussel – 2021-2024*
