class SimulatedKid:
    def __init__(self, orderline_list) -> None:
        self.address = orderline_list[0].address
        self.custname = orderline_list[0].custname
        self.pickseries = orderline_list[0].pickseries
        self.location = orderline_list[0].location
        self.city = orderline_list[0].city
        self.postcode = orderline_list[0].postcode
        self.country = orderline_list[0].country
        
        self.dates = set()
        self.ordernumbers = set()
        self.number_of_items = 0
        self.ldm = 0
        self.is_moved_back = False
        self.is_big = False
        self.is_delayed = False
        self.is_hay_direct = False

        for orderline in orderline_list:
            self.dates.add(orderline.date)
            self.ordernumbers.add(orderline.ordernumber)
            self.number_of_items += orderline.number_of_items
            self.ldm += orderline.loadmeter
            if orderline.is_moved_back:
                self.is_moved_back = True
            if orderline.is_hay_direct:
                self.is_hay_direct = True
            if orderline.is_delayed:
                self.is_delayed = True

        if self.number_of_items >= 30:
            self.is_big = True
        self.dates = list(self.dates)
        self.dates.sort()

