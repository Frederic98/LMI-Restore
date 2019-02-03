# Barcode printer

This script prints a 2D barcode (DataMatrix) with the written ID for the containers. This works with a couple of label printers from the Brother QL series.
It uses the Linux kernel to talk to the label printer, so this won't work on Windows.

### Dependencies
- brother_ql
- elaphe3
- PIL

`pip3 install brother_ql elaphe3 pillow`

You have to add yourself to the `lp` group to be able to talk to the label printer.  
`sudo usermod -a -G lp USER_NAME`
