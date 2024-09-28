import glob
from fpdf import FPDF


filepaths = glob.glob("*.txt")

pdf = FPDF(orientation="P", unit="mm", format="A4")

for filepath in filepaths:
    pdf.add_page()
    pdf.set_font(family="Times", size=16, style="B")
    title = filepath.split(".")[0]
    title = title.capitalize()
    pdf.cell(w=50, h=8, txt=title, align="L", ln=1)
    pdf.set_font(family="Times", size=12, style="B")
    with open(filepath, 'r') as file:
        content = file.readlines()
    for line in content:
        pdf.multi_cell(w=0, h=6, txt=line)

pdf.output("output.pdf")