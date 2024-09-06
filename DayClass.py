from SimulatedKidClass import SimulatedKid

class Day:
    def __init__(self, date) -> None:
        self._date = date
        self._orderlines = []
        self._kids = []
         
    @property    
    def orderlines(self):
        return self._orderlines

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
    def ldm_total(self):
        total = 0
        for orderline in self.orderlines:
            total += orderline.loadmeter
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
    
    def get_day_report(self):
        day_report = ""
        
        day_report += f"{'#' * 22}\n{self.weekday} d. {self.date}:\n{'#' * 22}\n\n"
        day_report += f"Varer i alt: {self.items_total}\n"
        day_report += f"Ca. ldm i alt: {round(self.ldm_total, 2)}\n"
        day_report += f"Ordrer i alt: {self.orders_total}\n"
        day_report += f"KID'er i alt: {len(self.kids)}\n"
        day_report += f"Ordrerne har følgende bekræftelsesdatoer: {', '.join(self.dates)}.\n"
        day_report += f"Destinationer: {', '.join(self.countries)}.\n"
        day_report += f"Alle ordrenumre: {'|'.join(self.all_ordernumbers)}\n\n"
        
        
        for i, kid in enumerate(self.kids):
            day_report += f"{'*' * 5 } KID nr. {i + 1}: {'*' * 5}\n"
            day_report += f"{kid.custname}, {kid.city}, {kid.country}.\n"
            day_report += f"Ordrerne er bekræftet til d.: {', '.join(kid.dates)}.\n"
            day_report += f"{len(kid.ordernumbers)} ordre{'r' if len(kid.ordernumbers) > 1 else ''}, {kid.number} vare{'r' if kid.number > 1 else ''}, ca. {round(kid.ldm, 2)} ldm.\n"
            day_report += f"{'|'.join(kid.ordernumbers)}\n\n"
        
        return day_report
    