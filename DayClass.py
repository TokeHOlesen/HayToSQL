import datetime

from KidClass import Kid
from OrderlineClass import Orderline
from ReportClass import Report


class Day:
    def __init__(self, date: datetime.date) -> None:
        self._date: datetime.date = date
        self._orderlines: list[Orderline] = []
        self._kids: list[Kid] = []

    @property    
    def orderlines(self) -> list[Orderline]:
        return self._orderlines
    
    @property
    def date(self) -> datetime.date:
        return self._date
    
    @property
    def kids(self) -> list[Kid]:
        return self._kids

    @property
    def weekday_number(self) -> int:
        return self._date.weekday()
    
    @property
    def weekday(self) -> str:
        weekdays = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
        return weekdays[self.weekday_number % 7]
    
    @property
    def orders_total(self) -> int:
        total: int = 0
        for kid in self.kids:
            total += len(kid.ordernumbers)
        return total
    
    @property
    def items_total(self) -> int:
        total: int = 0
        for orderline in self.orderlines:
            total += orderline.number_of_items
        return total

    @property
    def furniture_total(self) -> int:
        total: int = 0
        for orderline in self.orderlines:
            if "cushion" not in orderline.itemname.lower():
                total += orderline.number_of_items
        return total

    @property
    def cushions_total(self) -> int:
        total: int = 0
        for orderline in self.orderlines:
            if "cushion" in orderline.itemname.lower():
                total += orderline.number_of_items
        return total
    
    @property
    def ldm_total(self) -> float:
        total: float = 0
        for orderline in self.orderlines:
            total += orderline.loadmeter
        return total

    @property
    def kids_total(self) -> int:
        return len(self.kids)

    @property
    def hay_direct_total(self) -> int:
        total: int = 0
        for kid in self.kids:
            if kid.is_hay_direct:
                total += 1
        return total

    @property
    def potentially_delayed_total(self) -> int:
        total: int = 0
        for kid in self.kids:
            if kid.is_delayed:
                total += 1
        return total

    @property
    def kids_in_pick_series(self) -> int:
        total: int = 0
        for kid in self.kids:
            if kid.pickseries:
                total += 1
        return total

    @property
    def all_ordernumbers(self) -> list[str]:
        ordernumbers: list[str] = []
        for kid in self.kids:
            for ordernumber in kid.ordernumbers:
                ordernumbers.append(ordernumber)
        return ordernumbers

    @property
    def countries(self) -> list[str]:
        return sorted(list({orderline.country for orderline in self.orderlines}))
    
    @property
    def addresses(self) -> list[str]:
        return list({orderline.address for orderline in self.orderlines})
    
    @property
    def dates(self) -> list[datetime.date]:
        return sorted(list({orderline.date for orderline in self.orderlines}))
    
    def add_line(self, orderline) -> None:
        self._orderlines.append(orderline)
    
    def remove_line(self, orderline) -> None:
        self._orderlines.remove(orderline)
    
    def calculate_kids(self) -> None:
        for address in self.addresses:
            orderline_list: list[Orderline] = []
            for orderline in self.orderlines:
                if orderline.address == address:
                    orderline_list.append(orderline)
            self._kids.append(Kid(orderline_list))
        self._kids.sort(key=lambda kid: kid.country)
        self.move_delayed_kids_to_beginning()

    def move_delayed_kids_to_beginning(self) -> None:
        for kid in self._kids:
            if kid.is_delayed:
                kid_to_move: Kid = kid
                self._kids.remove(kid_to_move)
                self._kids.insert(0, kid_to_move)

    def get_day_report(self) -> str:
        day_report = Report.generate_day_head(self.weekday,
                                              self.date,
                                              self.items_total,
                                              self.ldm_total,
                                              self.orders_total,
                                              len(self.kids),
                                              self.kids_in_pick_series,
                                              self.dates,
                                              self.countries,
                                              self.all_ordernumbers
                                              )

        for i, kid in enumerate(self.kids):
            day_report += Report.generate_kid(i + 1,
                                              kid.custname,
                                              kid.pickseries,
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
    