from SimulatedKidClass import SimulatedKid
from ReportClass import Report


class Day:
    def __init__(self, date) -> None:
        self._date = date
        self._orderlines = []
        self._kids = []
         
    @property    
    def orderlines(self):
        return self._orderlines
    
    @property
    def date(self):
        return self._date
    
    @property
    def kids(self):
        return self._kids

    @property
    def weekday_number(self):
        return self._date.weekday()
    
    @property
    def weekday(self):
        weekdays = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
        return weekdays[self.weekday_number % 7]
    
    @property
    def orders_total(self):
        total = 0
        for kid in self.kids:
            total += len(kid.ordernumbers)
        return total
    
    @property
    def items_total(self):
        total = 0
        for orderline in self.orderlines:
            total += orderline.number_of_items
        return total
    
    @property
    def ldm_total(self):
        total = 0
        for orderline in self.orderlines:
            total += orderline.loadmeter
        return total

    @property
    def kids_total(self):
        return len(self.kids)

    @property
    def hay_direct_total(self):
        total = 0
        for kid in self.kids:
            if kid.is_hay_direct:
                total += 1
        return total

    def potentially_delayed_total(self):
        total = 0
        for kid in self.kids:
            if kid.is_delayed:
                total += 1
        return total
    
    @property
    def all_ordernumbers(self):
        ordernumbers = []
        for kid in self.kids:
            for ordernumber in kid.ordernumbers:
                ordernumbers.append(ordernumber)
        return ordernumbers

    @property
    def countries(self):
        return sorted(list({orderline.country for orderline in self.orderlines}))
    
    @property
    def addresses(self):
        return list({orderline.address for orderline in self.orderlines})
    
    @property
    def dates(self):
        return sorted(list({orderline.date for orderline in self.orderlines}))
    
    def add_line(self, orderline):
        self._orderlines.append(orderline)
    
    def remove_line(self, orderline):
        self._orderlines.remove(orderline)
    
    def calculate_kids(self):
        for address in self.addresses:
            orderline_list = []
            for orderline in self.orderlines:
                if orderline.address == address:
                    orderline_list.append(orderline)
            self._kids.append(SimulatedKid(orderline_list))
        self._kids.sort(key=lambda kid: kid.country)
        self.move_delayed_kids_to_beginning()

    def move_delayed_kids_to_beginning(self):
        for kid in self._kids:
            if kid.is_delayed:
                kid_to_move = kid
                self._kids.remove(kid_to_move)
                self._kids.insert(0, kid_to_move)

    def get_day_report(self):
        day_report = Report.generate_day_head(self.weekday,
                                              self.date,
                                              self.items_total,
                                              self.ldm_total,
                                              self.orders_total,
                                              len(self.kids),
                                              self.dates,
                                              self.countries,
                                              self.all_ordernumbers
                                              )

        for i, kid in enumerate(self.kids):
            day_report += Report.generate_kid(i + 1,
                                              kid.custname,
                                              kid.city,
                                              kid.country,
                                              kid.dates,
                                              len(kid.ordernumbers),
                                              kid.number_of_items,
                                              kid.ldm,
                                              kid.ordernumbers,
                                              kid.is_moved_back,
                                              kid.is_delayed,
                                              kid.is_hay_direct,
                                              kid.is_big)

        day_report += Report.generate_day_tail()
        return day_report
    