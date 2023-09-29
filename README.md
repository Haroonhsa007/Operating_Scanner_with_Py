# Operating Scanner with Python (A5 Scanner)

# Report on the Scanner Program

## Introduction

The provided program is a Python script that interfaces with a scanner device
to perform scanning operations. It utilizes the `pyinsane2` library,
which is a Python wrapper for the Sane scanner access library. The program 
is designed to scan a document with specific settings, save it as a 
JPEG image, and handle potential multiple output files with distinct names.

## Program Workflow

The program follows a sequential workflow, as described below:

### 1. Importing Libraries

The program starts by importing necessary libraries:

- `os`: Provides a way to interact with the operating system, used for file operations.
- `PIL`: Stands for Python Imaging Library, used for handling images.
- `pyinsane2`: The main library used to interact with the scanner device.

### 2. Setting Scan Area for A5

The function `set_scan_area_A5` is defined to set the scan area to A5 size. 
 It calculates the pixel dimensions corresponding to A5 dimensions in
  millimeters and adjusts the scan area accordingly.

### 3. Main Function

The `main` function is where the core functionality of the program resides.

#### a. Detecting Scanners

The program first attempts to discover available scanners 
using `pyinsane2.get_devices()`. If no scanner is detected, 
it prints a message and terminates.

#### b. Selecting Scanner

If a scanner is detected, the first available scanner is selected.

#### c. Setting Scanner Options

Several scanner options are configured:

- `source`: Specifies the source of the scan (Auto or FlatBed).
- `resolution`: Sets the scanning resolution to 600 dpi.
- `set_scan_area_A5`: Calls the function to set the scan area to A5.
- `mode`: Specifies the scan mode (Color).

#### d. Scanning

The program initiates the scanning process using 
`device.scan(multiple=False)`. It then enters a loop to continuously
 read scan data until an End of File (EOF) error is raised.

$$ The below code can be changed for any Size depending on your Scanner 
$$ Either A5 or A4 or any other size

```
def set_scan_area_A5(device):
    options = device.options

    # Define A5 dimensions in millimeters
    a5_width_mm = 148
    a5_height_mm = 210

    # Convert A5 dimensions to pixels at 600dpi (1 inch = 25.4mm)
    a5_width_pixels = int(a5_width_mm / 25.4 * 600)
    a5_height_pixels = int(a5_height_mm / 25.4 * 600)

    # Set the top-left corner coordinates (0, 0)
    pyinsane2.set_scan_area_pos(options,'tl-x', lambda min_val, max_val: 0, {'tl-x': 0} )
    pyinsane2.set_scan_area_pos(options, 'tl-y', lambda min_val, max_val: 0, {'tl-y': 0} )

    # Set the bottom-right corner coordinates (a5_width_pixels, a5_height_pixels)
    
    pyinsane2.set_scan_area_pos(options, 'br-x', lambda min_val, max_val: a5_width_pixels, {'br-x': a5_width_pixels} )
    pyinsane2.set_scan_area_pos(options, 'br-y', lambda min_val, max_val: a5_height_pixels, {'br-y': a5_height_pixels} )

    device.options = options
```
 
#### e. Saving Output File

The output file is named "output.jpg" initially. 
If a file with that name already exists, the program iterates 
through numbered names (e.g., "output_1.jpg", "output_2.jpg", etc.)
 until a unique name is found. The scanned image is then saved in JPEG format.

#### f. Cleanup

After the scanning process is complete, the program prints a 
success message and exits gracefully.

### 4. Executing the Program

The `if __name__ == "__main__":` block ensures that the program is
 executed only if it is run directly (not imported as a module). 
 It initializes the `pyinsane2` library, executes the `main` function, 
 and then ensures that `pyinsane2` is properly exited
  even if an error occurs during execution.

## Conclusion

This program demonstrates a practical use case of 
interfacing with a scanner device in Python. It sets 
specific scan parameters, performs the scan, and
 handles the output in an organized manner. The resulting scanned
  image is saved in JPEG format for further use.
