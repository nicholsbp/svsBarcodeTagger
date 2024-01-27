# Aperio SVS Label Decoder

## Description
This program is designed to process Aperio SVS slide image files. It extracts the barcode tile (either DataMatrix, QR, or 1D) from the label of an SVS file and renames the file by prefixing it with the decoded barcode data. Includes batch processing functionality with parallel processing.

## Features
- Extracts barcodes (DataMatrix, QR, or 1D) from SVS file labels.
- Renames SVS files with the barcode data as a prefix.
- Handles individual SVS files or batches of files in a directory.
- Parallel processing capabilities for improved performance in batch mode.
- Provides performance metrics upon completion.

## Usage
For help and information about the program's arguments, run:
```
python svstag.py --help
```
Process a single file:
```
python svstag.py <path-to-svs-file> [--barcode <barcode-type>] [--threads <num-threads>]
```
Batch process a directory of SVS files:
```
python svstag.py <path-to-directory> [--barcode <barcode-type>] [--threads <num-threads>]
```
Where:
- <path-to-svs-file> is the path to the SVS file.
- <path-to-directory> is the path to the directory containing SVS files.
- <barcode-type> is the type of barcode to decode (datamatrix, QR, 1D). Default is datamatrix.
- <num-threads> is the number of threads for parallel processing. Default is the number of CPU cores.

### Installation
Requires python 3.10+

Install the required libraries using the following command:
```
pip install -r requirements.txt
```
