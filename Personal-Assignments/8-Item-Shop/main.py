import pandas as pd
from fpdf import FPDF

df = pd.read_csv("items.csv", dtype={"id": str})


class Item:
    def __init__(self, item_id):
        self.id = item_id
        self.name = df.loc[df["id"] == self.id, "name"].squeeze().title()
        self.price = df.loc[df["id"] == self.id, "price"].squeeze()

    def in_stock(self):
        in_stock = df.loc[df["id"] == self.id, "in stock"].squeeze()
        return in_stock

    def buy(self):
        df.loc[df["id"] == self.id, "in stock"] = df.loc[df["id"] == self.id, "in stock"] - 1
        df.to_csv("items.csv", index=False)


class Receipt:
    def __init__(self, item_object):
        self.item = item_object

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.item.id}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.item.name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.item.price}", ln=1)

        pdf.output("receipt.pdf")


# MAIN LOOP
print(df)
item_id = input("Choose and item to buy: ")
item = Item(item_id=item_id)

if item.in_stock():
    item.buy()
    receipt = Receipt(item_object=item)
    receipt.generate()
    print("Item successfully purchased!")
else:
    print("Item is currently out of stock.")