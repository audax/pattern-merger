# Pattern Merger

This project provides a tool to assemble a PDF pattern on one page, trim margins, and filter specific layers using Python and the PyMuPDF library.

## Features

- Trim margins of PDF pages
- Assemble multiple PDF pages into a single page with a specified layout
- Save the resulting PDF and its dimensions

## Requirements

- Python 3.x
- PyMuPDF library

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies using Poetry:
    ```sh
    poetry install
    ```

## Usage

The script can be run from the command line with the following arguments:

```sh
python pattern_merger/__init__.py <input_pdf> <start_page> <end_page> <rows> <output_pdf>
