import argparse
import os
import sys
import shutil
from pathlib import Path
from typing import List, Set

# 이미지 처리를 위한 라이브러리 임포트
try:
    from PIL import Image
    import pillow_heif
    import rawpy
    import io
    import imageio
except ImportError:
    print("Error: Required libraries are not installed.")
    print("Please run: pip install Pillow pillow-heif rawpy imageio")
    sys.exit(1)

# pillow_heif를 활성화하여 Pillow가 .heic/.heif 파일을 열 수 있도록 등록
pillow_heif.register_heif_opener()


def get_image_files(directory: str, extensions: Set[str]) -> List[Path]:
    """
    Find image files with specific extensions in the given directory.
    Args:
        directory: Directory path to search
        extensions: Set of file extensions to find (e.g., {'.heic', '.dng'})
    Returns:
        List of Path objects for found image files
    """
    directory_path = Path(directory)
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")
    image_files = []
    for ext in extensions:
        image_files.extend(directory_path.glob(f"**/*{ext.lower()}"))
        image_files.extend(directory_path.glob(f"**/*{ext.upper()}"))
    return list(set(image_files))


def convert_image_files(from_dir: str, to_dir: str, target_extension: str) -> None:
    """
    Convert image files to the specified extension and save them to the target directory.
    Args:
        from_dir: Source directory containing image files
        to_dir: Target directory to save converted files
        target_extension: Extension to convert to (e.g., '.jpg', '.png')
    """
    supported_extensions = {'.heic', '.dng', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    try:
        image_files = get_image_files(from_dir, supported_extensions)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    if not image_files:
        print(f"No supported image files found in '{from_dir}'.")
        return
    to_path = Path(to_dir)
    to_path.mkdir(parents=True, exist_ok=True)
    print(f"Processing {len(image_files)} image files...")
    for image_file in image_files:
        try:
            new_filename = image_file.stem + target_extension
            new_file_path = to_path / new_filename
            counter = 1
            while new_file_path.exists():
                new_filename = f"{image_file.stem}_{counter}{target_extension}"
                new_file_path = to_path / new_filename
                counter += 1
            print(f"Converting: {image_file.name} -> {new_filename}")
            source_ext = image_file.suffix.lower()
            if source_ext == '.dng':
                with rawpy.imread(str(image_file)) as raw:
                    try:
                        thumb = raw.extract_thumb()
                        if thumb.format == 'JPEG':
                            image = Image.open(io.BytesIO(thumb.data))
                        elif thumb.format == 'BITMAP':
                            image = Image.fromarray(thumb.data)
                        else:
                            raise Exception("Unknown thumbnail format")
                    except Exception:
                        rgb = raw.postprocess(use_camera_wb=True)
                        image = Image.fromarray(rgb)
            else:
                image = Image.open(image_file)
            if target_extension.lower() in ['.jpg', '.jpeg']:
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
            image.save(new_file_path)
        except Exception as e:
            print(f"!! Error processing file ({image_file.name}): {e}")
    print(f"\nDone! Converted files are saved in '{to_dir}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert image files to another format and save them to a new directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py .jpg ./images ./converted_images
  python main.py .png "C:\\Users\\User\\Pictures" "C:\\Users\\User\\Converted"
  python main.py .webp ./source_folder ./converted_folder
        """
    )
    parser.add_argument(
        "extension",
        help="Target file extension (e.g., .jpg, .png, .webp)"
    )
    parser.add_argument(
        "from_dir",
        help="Source directory containing image files (including subfolders)"
    )
    parser.add_argument(
        "to_dir",
        help="Target directory to save converted files"
    )
    args = parser.parse_args()
    target_extension = args.extension.lower()
    if not target_extension.startswith('.'):
        target_extension = '.' + target_extension
    print(f"Image File Format Converter")
    print(f"Target extension: {target_extension}")
    print(f"Source directory: {args.from_dir}")
    print(f"Target directory: {args.to_dir}")
    print("-" * 50)
    try:
        convert_image_files(args.from_dir, args.to_dir, target_extension)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()