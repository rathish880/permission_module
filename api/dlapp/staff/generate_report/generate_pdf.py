from reportlab.pdfgen import canvas
from datetime import date
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import purple


def render_pdf():
    fileName = date.today().strftime("%d-%m-%Y") + ".pdf"

    file = canvas.Canvas(fileName)
    file.setFont("Courier", 18)
    file.setFillColor(purple)
    file.drawString(2 * inch, 8 * inch, "Pdf is successfully rendered in server.")
    file.save()

    return fileName
