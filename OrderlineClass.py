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
        # Flags:
        # 1: Order delayed
        # 2: Large order
        # 3: Hay-Direct order
        self.flags = 0b0000
