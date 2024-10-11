import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str}) # dtype ensures that the "id" column is loaded as a
                                                                # string, even if it contains numbers


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        """Book a hotel by changing it's availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False) #index=False: By default, pandas writes the DataFrame's
                                                       # row indices (the index) to the CSV file as the first column.
                                                       # Setting index=False tells pandas not to write the index to the
                                                       # CSV file. This means the CSV will only include the DataFrame's
                                                       # data columns, not the index.


class Ticket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your booking data:
        Name: {self.customer_name} 
        Hotel name: {self.hotel.name}
        """
        return content


# main loop:

print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_ticket = Ticket(customer_name=name, hotel_object=hotel)
    print(reservation_ticket.generate())
else:
    print("Hotel isn't free.")