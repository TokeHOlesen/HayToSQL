class Kid:
    def __init__(self, orderline_list) -> None:
        self.address: str = orderline_list[0].address
        self.custname: str = orderline_list[0].custname
        self.pickseries: str = orderline_list[0].pickseries
        self.location: str = orderline_list[0].location
        self.city: str = orderline_list[0].city
        self.postcode: str = orderline_list[0].postcode
        self.country: str = orderline_list[0].country
        
        self.dates: set = set()
        self.ordernumbers: set = set()
        self.number_of_items: int = 0
        self.ldm: float = 0
        self.is_moved_back: bool = False
        self.is_big: bool = False
        self.is_delayed: bool = False
        self.is_hay_direct: bool = False

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

