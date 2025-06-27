# Image File Format Converter

This program is a CLI tool that converts various image file formats (such as HEIC, DNG, etc.) and saves them to a new directory.

## Features

- Supports various image formats: HEIC, DNG, JPG, PNG, BMP, TIFF, WebP, and more
- Fully supports Korean and Unicode paths
- Automatically adds a number if a filename conflict occurs
- Original files are preserved (only copies are created)
- Detailed progress output

## Usage

```bash
python main.py <extension> <source_directory> <target_directory>
```

### Arguments

- `extension`: Target file extension (e.g., `.jpg`, `.png`, `.webp`)
- `source_directory`: Directory containing the image files
- `target_directory`: Directory to save the converted files

### Examples

```bash
# Convert images in the current directory to JPG and save them in the 'converted' folder
python main.py .jpg ./images ./converted

# Using Unicode (Korean) paths
python main.py .png "C:\Users\User\Pictures" "C:\Users\User\ConvertedImages"

# Using relative paths
python main.py .webp ./source_folder ./converted_folder
```

## Supported Image Formats

- HEIC (.heic)
- DNG (.dng)
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Notes

- This program actually converts the image data, not just the file extension
- The original files remain unchanged; converted copies are created in the target directory
- If filenames conflict, a number is automatically appended (e.g., image_1.jpg, image_2.jpg)

## Requirements

- Python 3.12 or higher
- Only standard and listed libraries are required (see pyproject.toml)

---

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
