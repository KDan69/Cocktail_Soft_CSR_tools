# Cocktail Soft CSR tools
Scripts for converting Cocktail Soft PC-98 cursor graphics to PNG and vice versa. Created specifically for editing cursors in Travel Junction, but it should work on different games by Cocktail Soft as well (I tested `MOUSE.DAT` from Pia Carrot).
## CSR format structure
Travel Junction had two cursor files: `CMDCSR.CSR` containing a single image and `TJ.CSR` containing the rest. The single cursor file contains an 8 byte header followed by the uncompressed 4bpp image data. The file containing multiple cursors has some unknown data before the header of the first cursor appears. This data gets saved later as `header.dat` so it can be injected back when converting from PNG to CSR. The cursor images are separated by two zero bytes.
### Header format (8 bytes)
Most important bytes are the first two (or four perhaps) with magic numbers `4D 43` (`MC` in ASCII) and the last two bytes containing the image size info.
#### Example
`4D 43 00 4F 00 00 03 18` - 24x24 image (note - the image width is given in multiple of 8, so 0x03 actually means 3*8 in pixels)<br>
`4D 43 00 4F 00 00 04 18` - 32x24 image<br>
## Notes
- Color palettes aren't supported yet, the images are converted to 16 shades of grey
- The output PNG files are actually 8bpp because of the limitation of the Python PIL library
## Usage
### split.py
Splits CSR files containing multiple images into single CSR files. Creates a new folder with `header.dat` and the individual files `0000.CSR`, `0001.CSR`, `0002.CSR` etc. Also useful for `MOUSE.DAT` from Pia Carrot (it's a single image, but with an extra header).
### csr_png.py
Main script for image conversion. Use it with a batch file for processing multiple cursors.
### consolidate.py
Joins the split CSR files back into a single CSR file. You must specify a subfolder containing `header.dat` and the CSR files as an input.
