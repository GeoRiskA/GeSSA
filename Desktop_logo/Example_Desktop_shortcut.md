# Example of .Desktop file to launch GeSSA from the Linux desktop

If you would like to create a desktop shortcut to launch GeSSA more easily, here is an example of .Desktop file you can create.

1) Open a text editor and write this:
```
[Desktop Entry]
Name=GeSSA
Version=0.1.6
Icon=/home/user/Scripts/GeSSA/Desktop_logo/logo.png
Exec=/home/user/Scripts/GeSSA/GeSSA_v016.py
Terminal=true
Type=Application
```
*(Adapt the paths of the logo and GeSSA script according to your computer)*

2) Save the text as `GeSSA.Desktop` on your ~/Desktop

3) While looking at the desktop, right-click on th GeSSA.Desktop icon and select "Allow launching"
