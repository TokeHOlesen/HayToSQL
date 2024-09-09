class Orderline:
    def __init__(self, sql_data) -> None:
        (self.id,
         self.ordernumber,
         self.pickseries,
         self.location,
         self.itemnumber,
         self.itemname,
         self.color,
         self.number_of_items,
         self.loadmeter,
         self.date,
         self.kid,
         self.custname,
         self.address,
         self.city,
         self.postcode,
         self.country) = sql_data

        self.is_delayed: bool = False
        self.is_big: bool = False
        self.is_hay_direct: bool = self.location == "HAY-DIRECT"
        self.is_moved_back: bool = False
