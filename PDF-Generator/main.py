from fpdf import FPDF
import pandas as pd


pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=0)

df = pd.read_csv("topics.csv")

for index,row in df.iterrows():

    for i in range(row["Pages"]):

        # set header
        pdf.add_page()
        pdf.set_font(family="Times", size=24)
        pdf.set_text_color(100, 100, 100)

        if i == 0:
            pdf.cell(w=0, h=12, txt=row["Topic"], align="L", ln=1, border=0)
            pdf.line(x1=10, y1=22, x2=200, y2=22)
            pdf.ln(265)
            pdf.set_font(family="Times", style="I", size=8)
            pdf.set_text_color(180, 180, 180)
            pdf.cell(w=0, h=12, txt=row["Topic"], align="R")
        else:
            # set footer
            pdf.ln(277)
            pdf.set_font(family="Times", style="I", size=8)
            pdf.set_text_color(180, 180, 180)
            pdf.cell(w=0, h=12, txt=row["Topic"], align="R")

        for i in range(22, 290, 10):
            pdf.line(10, i, 200, i)

pdf.output("output.pdf")