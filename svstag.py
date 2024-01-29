import tifffile
import cv2
import os
import glob
import argparse
import time
from multiprocessing import Pool
from pylibdmtx.pylibdmtx import decode as decode_datamatrix
from pyzbar.pyzbar import decode as decode_barcode


def extract_label_from_svs(svs_file_path):
    # Extracts the label image from an SVS file, the index might be instrument specific
    with tifffile.TiffFile(svs_file_path) as tif:
        label = tif.series[2].asarray()
        return label


def decode_label(label_image, barcode_type):
    label_image_cv = cv2.cvtColor(label_image, cv2.COLOR_RGB2BGR)
    # Choose decoding method based on barcode type
    if barcode_type == 'datamatrix':
        data = decode_datamatrix(label_image_cv)
    else:
        data = decode_barcode(label_image_cv)
        
    # Return barcode data if found
    for barcode in data:
        if barcode_type == 'datamatrix' or barcode.type in ['QRCODE', 'CODE128', 'EAN13', 'EAN8']:
            return barcode.data.decode('utf-8')
    return None


def rename_file(original_file_path, barcode_data):
    # Renames file with barcode data, potential crash if barcode data contains banned symbol
    directory, filename = os.path.split(original_file_path)
    new_filename = f"{barcode_data}-{filename}"
    new_path = os.path.join(directory, new_filename)
    os.rename(original_file_path, new_path)
    print(f"Renamed '{filename}' to '{new_filename}'")


def process_file(args):
    svs_file_path, barcode_type = args
    label_image = extract_label_from_svs(svs_file_path)
    barcode_value = decode_label(label_image, barcode_type)

    if barcode_value:
        rename_file(svs_file_path, barcode_value)
    else:
        print(f"No {barcode_type} barcode found in the label image of {svs_file_path}")


def process_files_in_directory(directory, barcode_type, num_processes):
    svs_files = glob.glob(os.path.join(directory, '*.svs'))
    start_time = time.time()
    with Pool(processes=num_processes) as pool:
        pool.map(process_file, [(file_path, barcode_type) for file_path in svs_files])
    end_time = time.time()
    # Calculate and display processing time statistics
    total_time = end_time - start_time
    average_time = total_time / len(svs_files) if svs_files else 0
    print(f"Total time elapsed: {total_time:.2f} seconds")
    print(f"Average processing time per slide: {average_time:.2f} seconds")
    print(f"Number of concurrent processes: {num_processes}")


def main():
    parser = argparse.ArgumentParser(description="Process .svs files and rename them based on barcode data.")
    parser.add_argument("path", help="Path to an .svs file or a directory containing .svs files")
    parser.add_argument("--barcode", default="datamatrix", choices=["datamatrix", "QR", "1D"],
                        help="Type of barcode to decode (default: datamatrix)")
    parser.add_argument("--threads", type=int, default=os.cpu_count(),
                        help="Number of parallel processing threads (default: number of CPU cores)")

    args = parser.parse_args()

    if os.path.isfile(args.path) and args.path.endswith('.svs'):
        start_time = time.time()
        process_file((args.path, args.barcode))
        end_time = time.time()
        print(f"Total time elapsed: {end_time - start_time:.2f} seconds")
        print(f"Number of concurrent processes: 1")
    elif os.path.isdir(args.path):
        process_files_in_directory(args.path, args.barcode, args.threads)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
