import os
import sys
import pyinsane2

PROGRESSION_INDICATOR = ['|', '/', '-', '\\', '|', '/', '-', '\\']
"""
def set_scan_area_A5(device):
    options = device.options

    a5_width_mm = 148
    a5_height_mm = 210

    a5_width_pixels = int(a5_width_mm / 25.4 * 600)
    a5_height_pixels = int(a5_height_mm / 25.4 * 600)

    pyinsane2.set_scan_area_pos(options, 'tl-x', lambda min_val, max_val: 0, {'tl-x': 0})
    pyinsane2.set_scan_area_pos(options, 'tl-y', lambda min_val, max_val: 0, {'tl-y': 0})
    pyinsane2.set_scan_area_pos(options, 'br-x', lambda min_val, max_val: a5_width_pixels, {'br-x': a5_width_pixels})
    pyinsane2.set_scan_area_pos(options, 'br-y', lambda min_val, max_val: a5_height_pixels, {'br-y': a5_height_pixels})

    device.options = options


def set_scan_area_A5(device):
    options = device.options

    a5_width_mm = 148
    a5_height_mm = 210

    a5_width_pixels = int(a5_width_mm / 25.4 * 600)
    a5_height_pixels = int(a5_height_mm / 25.4 * 600)

    options_dict = {'tl-x': 0, 'tl-y': 0, 'br-x': a5_width_pixels, 'br-y': a5_height_pixels}
    
    for pos, value in options_dict.items():
        pyinsane2.set_scan_area_pos(options, pos, lambda min_val, max_val: value, {pos: value})

    device.options = options
"""

def set_scan_area_A5(device):
    options = device.options

    a5_width_mm = 148
    a5_height_mm = 210

    a5_width_pixels = int(a5_width_mm / 25.4 * 600)
    a5_height_pixels = int(a5_height_mm / 25.4 * 600)

    options_dict = {'tl-x': 0, 'tl-y': 0, 'br-x': a5_width_pixels, 'br-y': a5_height_pixels}
    
    for pos, value in options_dict.items():
        pyinsane2.set_scan_area_pos(options, pos, lambda min_val, max_val: value, None)

    device.options = options


def main():
    devices = pyinsane2.get_devices()

    if len(devices) <= 0:
        print("No scanner detected !")
        return

    device = devices[0]

    pyinsane2.set_scanner_opt(device, 'source', ['Auto', 'FlatBed'])
    pyinsane2.set_scanner_opt(device, 'resolution', [600])
    set_scan_area_A5(device)
    pyinsane2.set_scanner_opt(device, 'mode', ['Color'])

    print("Scanning ...")
    scan_session = device.scan(multiple=False)

    try:
        i = -1
        while True:
            i += 1
            i %= len(PROGRESSION_INDICATOR)
            sys.stdout.write("\b%s" % PROGRESSION_INDICATOR[i])
            sys.stdout.flush()
            scan_session.scan.read()
    except EOFError:
        pass

    output_file = "output.jpg"
    count = 1

    while os.path.exists(output_file):
        output_file = f"output_{count}.jpg"
        count += 1

    print(f"\nWriting output file: {output_file}")
    img = scan_session.images[0]
    img.save(output_file, "JPEG")
    print("Done")


if __name__ == "__main__":
    pyinsane2.init()
    try:
        main()
    finally:
        pyinsane2.exit()

import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import os
import sys

# Import the functions you want to test
from Scan_5 import set_scan_area_A5, main, pyinsane2, PROGRESSION_INDICATOR

class TestScannerFunctions(unittest.TestCase):

    @patch('pyinsane2.get_devices')
    @patch('sys.stdout', new_callable=StringIO)
    def test_set_scan_area_A5(self, mock_stdout, mock_get_devices):
        # Mock the device and its options
        mock_device = MagicMock()
        mock_options = MagicMock()
        mock_device.options = mock_options
        mock_get_devices.return_value = [mock_device]

        # Define the lambda functions
        a5_width_mm = 148
        a5_height_mm = 210
        a5_width_pixels = int(a5_width_mm / 25.4 * 600)
        a5_height_pixels = int(a5_height_mm / 25.4 * 600)

        options_dict = {'tl-x': 0, 'tl-y': 0, 'br-x': a5_width_pixels, 'br-y': a5_height_pixels}

        set_scan_area_A5(mock_device)  # Call the function once

        # Assertions to check if set_scan_area_pos was called correctly
        for pos, value in options_dict.items():
            pyinsane2.set_scan_area_pos.assert_called_once_with(mock_options, pos, MagicMock(), {pos: value})
            pyinsane2.set_scan_area_pos.reset_mock()

    @patch('pyinsane2.get_devices')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout, mock_get_devices):
        # Mock the device and its options
        mock_device = MagicMock()
        mock_options = MagicMock()
        mock_device.options = mock_options
        mock_get_devices.return_value = [mock_device]

        # Mock the scan session and image
        mock_scan_session = MagicMock()
        mock_image = MagicMock()
        mock_scan_session.images = [mock_image]
        mock_device.scan.return_value = mock_scan_session

        # Mock the user input (EOFError) to exit the loop
        with patch('builtins.input', side_effect=[EOFError]):
            main()

        # Assertions to check if set_scanner_opt and other functions were called correctly
        mock_device.scan.assert_called_once_with(multiple=False)
        mock_scan_session.scan.read.assert_called_once()
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
