class Orderline:
    def __init__(self, sql_data) -> None:
        (self.id,
        self.ordernumber,
        self.pickseries,
        self.location,
        self.itemnumber,
        self.itemname,
        self.color,
        self.number,
        self.loadmeter,
        self.date,
        self.kid,
        self.custname,
        self.address,
        self.city,
        self.postcode,
        self.country) = sql_data
    
        self.message = ""