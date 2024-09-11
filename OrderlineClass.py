class Orderline:
    """
    Each object of this class contains selected data from one order line, as well as some flags describing the order.
    """
    def __init__(self, sql_data: tuple) -> None:
        """Populates each field with corresponding data from the SQL database."""
        (self.id,
         self.ordernumber,
         self.pickseries,
         self.location,
         self.itemnumber,
         self.itemname,
         self.color,
         self.number_of_items,
         self.ldm,
         self.date,
         self.kid,
         self.custname,
         self.address,
         self.city,
         self.postcode,
         self.country) = sql_data
        # Sets flags
        self.is_delayed: bool = False
        self.is_big: bool = False
        self.is_hay_direct: bool = (self.location == "HAY-DIRECT")
        self.is_moved_back: bool = False
