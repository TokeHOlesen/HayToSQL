class SimulatedKid:
    def __init__(self, orderline_list) -> None:
        self.address = orderline_list[0].address
        self.custname = orderline_list[0].custname
        self.pickseries = orderline_list[0].pickseries
        self.location = orderline_list[0].location
        self.city = orderline_list[0].city
        self.postcode = orderline_list[0].postcode
        self.country = orderline_list[0].country
        self.ordernumbers = set()
        self.number = 0
        self.ldm = 0
        for orderline in orderline_list:
            self.ordernumbers.add(orderline.ordernumber)
            self.number += orderline.number
            self.ldm += orderline.loadmeter
    
    def generate_report(self):
        return f"Number: {self.number}, {self.ldm}"