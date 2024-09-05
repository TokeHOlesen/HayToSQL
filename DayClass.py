from SimulatedKidClass import SimulatedKid

class Day:
    def __init__(self, date) -> None:
        self._date = date
        self._orderlines = []
        self._kids = []
         
    @property    
    def orderlines(self):
        return self._orderlines
    
    def add_line(self, orderline):
        self._orderlines.append(orderline)
    
    def remove_line(self, orderline):
        self._orderlines.remove(orderline)

    @property
    def number_of_lines(self):
        return len(self._orderlines)
    
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
            total += orderline.number
        return total

    @property
    def countries(self):
        return sorted(list({orderline.country for orderline in self.orderlines}))
    
    @property
    def addresses(self):
        return list({orderline.address for orderline in self.orderlines})
    
    def calculate_kids(self):
        for address in self.addresses:
            orderline_list = []
            for orderline in self.orderlines:
                if orderline.address == address:
                    orderline_list.append(orderline)
            self._kids.append(SimulatedKid(orderline_list))
    
    def get_day_report(self):
        day_report = ""
        
        day_report += f"{self.weekday} d. {self.date}:\n\n"
        day_report += f"Varer i alt: {self.items_total}\n"
        day_report += f"Ordrer i alt: {self.orders_total}\n"
        day_report += f"KIDer i alt: {len(self.kids)}\n"
        day_report += f"Destinationer: {', '.join(self.countries)}."
        
        return day_report
    