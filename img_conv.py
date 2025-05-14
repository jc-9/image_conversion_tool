import os
import argparse
from PIL import Image


def convert_image(input_path, output_path, output_format, quality = 80):
    """Converts a single image to the specified format.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the converted image.
        output_format (str): The desired output format (e.g., "webp", "png", "jpg").
        quality (int, optional): Quality for lossy formats (0-100). Defaults to 80.
    """
    try:
        img = Image.open(input_path)
        output_filename = os.path.splitext(os.path.basename(input_path))[0] + f".{output_format.lower()}"
        final_output_path = os.path.join(output_path, output_filename)

        if output_format.lower() == "webp":
            img = img.convert("RGB")  # WebP doesn't always handle all modes well
            img.save(final_output_path, "webp", quality = quality)
        elif output_format.lower() in ["png", "jpeg", "jpg"]:
            img.save(final_output_path)
        else:
            print(f"Unsupported output format: {output_format}")
            return

        print(f"Converted '{input_path}' to '{final_output_path}'")

    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred while processing '{input_path}': {e}")


def process_directory(input_dir, output_dir, output_format, quality):
    """Processes all image files in the input directory and converts them.

    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory to save converted images.
        output_format (str): The desired output format.
        quality (int): Quality for lossy formats.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path):
            try:
                # Try to open the file as an image to filter non-image files
                Image.open(input_path)
                convert_image(input_path, output_dir, output_format, quality)
            except Exception:
                print(f"Skipping non-image file or unsupported format: '{input_path}'")


def main():
    parser = argparse.ArgumentParser(description = "Convert a directory of images to a specified format.")
    parser.add_argument("input_dir", help = "Path to the input directory containing images.")
    parser.add_argument("output_dir", help = "Path to the output directory to save converted images.")
    parser.add_argument("output_format", help = "The desired output format (e.g., webp, png, jpg).")
    parser.add_argument("--quality", type = int, default = 80,
                        help = "Quality for lossy formats (0-100), default is 80.")

    args = parser.parse_args()

    input_directory = args.input_dir
    output_directory = args.output_dir
    output_format = args.output_format.lower()
    quality = args.quality

    if not os.path.isdir(input_directory):
        print(f"Error: Input directory '{input_directory}' does not exist.")
        return

    process_directory(input_directory, output_directory, output_format, quality)
    print("Image conversion process completed.")


if __name__ == "__main__":
    main()
