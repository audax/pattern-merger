import fitz  # PyMuPDF
import argparse
import sys

def cm_to_points(cm):
    return cm * 72 / 2.54

def points_to_cm(points):
    return points * 2.54 / 72

def create_pattern_pdf(input_pdf, start_page, end_page, output_pdf, rows):
    # Configuration of trim margins (in mm)
    trim_left = 10.0    # left side
    trim_right = 10.0   # right side
    trim_top = 23.6     # top side
    trim_bottom = 23.6  # bottom side

    # Conversion factor from mm to points (1 point = 1/72 inch)
    mm_to_points = 72 / 25.4
    trim_left_points = trim_left * mm_to_points
    trim_right_points = trim_right * mm_to_points
    trim_top_points = trim_top * mm_to_points
    trim_bottom_points = trim_bottom * mm_to_points

    # Load the PDF document
    doc = fitz.open(input_pdf)

    # Calculate the trimmed size of each page
    page_width = doc[0].rect.width - trim_left_points - trim_right_points
    page_height = doc[0].rect.height - trim_top_points - trim_bottom_points

    # Calculate the total number of pages to be processed
    total_pages = end_page - start_page + 1

    # Calculate the number of columns based on the total number of pages and rows
    columns = (total_pages + rows - 1) // rows

    # Calculate the total size of the target file
    total_width = page_width * columns
    total_height = page_height * rows

    # Create the result PDF with one page in the calculated total size
    result_pdf = fitz.open()
    result_page = result_pdf.new_page(width=total_width, height=total_height)

    # Place each page of the input file in the target PDF
    page_index = 0
    for row in range(rows):
        for col in range(columns):
            page_number = start_page + page_index
            if page_number > end_page:  # Stop if all pages have been placed
                break
            x_offset = col * page_width
            y_offset = row * page_height
            page = doc[page_number - 1]

            # Define the trim area for each page
            trimmed_rect = fitz.Rect(
                trim_left_points,
                trim_top_points,
                page.rect.width - trim_right_points,
                page.rect.height - trim_bottom_points
            )

            # Add the trimmed page at the calculated position on the target page
            result_page.show_pdf_page(
                fitz.Rect(x_offset, y_offset, x_offset + page_width, y_offset + page_height),
                doc,
                page_number - 1,
                clip=trimmed_rect,
            )

            page_index += 1
        else:
            continue
        break

    # Save the resulting document as a PDF with one page
    result_pdf.save(output_pdf)
    result_pdf.close()
    doc.close()

    # Print the dimensions of the document in cm
    total_width_cm = points_to_cm(total_width)
    total_height_cm = points_to_cm(total_height)

    # Check if the output PDF fits within standard paper sizes
    paper_size = check_paper_sizes(total_width, total_height, columns, rows, output_pdf)

    # Save the dimensions and paper size to a file
    with open(output_pdf.replace('.pdf', '-size.txt'), "w") as f:
        f.write(f"Document dimensions: {total_width_cm:.2f} x {total_height_cm:.2f} cm\n")
        f.write(f"Fits in: {paper_size}\n")

    print(f"Document dimensions: {total_width_cm:.2f} x {total_height_cm:.2f} cm")
    print(f"Fits in: {paper_size}")

def check_paper_sizes(total_width, total_height, columns, rows, output_pdf):
    paper_sizes = {
        "A4": (595, 842),
        "A3": (842, 1191),
        "A2": (1191, 1684),
        "A1": (1684, 2384),
        "A0": (2384, 3370)
    }

    print(f"Composite PDF with trim and layout {columns}x{rows} saved as {output_pdf}")
    for paper, (width, height) in paper_sizes.items():
        if total_width <= width and total_height <= height:
            return paper
    return "None"

def main():
    parser = argparse.ArgumentParser(description="Assembles a PDF pattern on one page, trims margins, and filters specific layers.")
    parser.add_argument("input_pdf", type=str, help="Path to the input PDF file.")
    parser.add_argument("start_page", type=int, help="Start page of the pattern.")
    parser.add_argument("end_page", type=int, help="End page of the pattern.")
    parser.add_argument("rows", type=int, help="Number of rows in the layout.")
    parser.add_argument("output_pdf", type=str, help="Path to the output PDF file.")

    args = parser.parse_args()

    create_pattern_pdf(args.input_pdf, args.start_page, args.end_page, args.output_pdf, args.rows)

if __name__ == "__main__":
    main()
