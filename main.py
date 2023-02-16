import io
from tkinter.filedialog import askopenfilename

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def new_filename(filename: str, company: str) -> str:
    "Takes the base filename and adds the company name to it."
    return f"{filename[:-4]}_{company}.pdf"


def add_watermark(
    company: str, filename: str, font_size: int, opacity: float, x: int, y: int
):
    "Adds a watermark to every page of the PDF."

    # This is all the settings for what the watermark will look like
    the_string = f"Confidential - {company}"
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.rotate(45)
    can.setFontSize(font_size)
    # This is an RBGA color, so the numbers represent (red, green, blue, alpha)
    # ALpha is the transparency, 0 is fully transparent, 1 is fully opaque
    can.setFillColorRGB(0, 0, 0, opacity)
    can.drawString(x, y, the_string)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    output = PdfWriter()
    # read your existing PDF
    with open(filename, "rb") as read_file:
        existing_pdf = PdfReader(read_file)
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
    # finally, write "output" to a real file
    new_file = new_filename(filename, company)
    with open(new_file, "wb") as output_stream:
        output.write(output_stream)


if __name__ == "__main__":
    COMPANIES = ["Walmart"]
    target_file = askopenfilename()
    print(target_file)
    for item in COMPANIES:
        add_watermark(
            company=item, filename=target_file, font_size=50, opacity=0.5, x=350, y=250
        )
