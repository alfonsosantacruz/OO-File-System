# OO-File-System

This implementation aims to simulate a file system controled by a cmd or terminal

Notice that main.py imports classes and libraries from setup.py

There is a small bug when accessing *.zip files created. It messes up the current path directory during the access. However, all of them are correctly moved and deleted when required. In addition, the resizing and errors work correctly around all the other file objects.

For some reason, the implementation was having issues processing the symbol '\' to divide directories in the paths. Consequently, the symbol was replace by '/' to avoid syntax issues. This did not affect the prints or other issues whatsoever.

Thank you for reading.
