import datetime

from KidClass import Kid
from OrderlineClass import Orderline
from ReportClass import Report


class Day:
    """
    Objects of this class have two list fields: ._orderlines and .kids.
    ._orderlines contains all the orderlines that must be shipped on this day. This includes orderlines with dates not
    equal to the Day's date, but grouped together because they share the delivery address. These will be grouped
    by address and used to contruct Kid objects with .calculate_kids().
    ._kids contains object of the Kid class that in turn contain all the orderlines that share the shipping address and
    will be packaged together - they can be thought of as a self-contained entity (a meta-order of sorts).
    Also has a number of other properties describing the day.
    """
    def __init__(self, date: datetime.date) -> None:
        self._date: datetime.date = date
        self._orderlines: list[Orderline] = []
        self._kids: list[Kid] = []

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
        return sum(len(kid.ordernumbers) for kid in self.kids)
    
    @property
    def items_total(self) -> int:
        return sum(orderline.number_of_items for orderline in self.orderlines)

    @property
    def furniture_total(self) -> int:
        return sum(
            orderline.number_of_items for orderline in self.orderlines if "cushion" not in orderline.itemname.lower())

    @property
    def cushions_total(self) -> int:
        return sum(
            orderline.number_of_items for orderline in self.orderlines if "cushion" in orderline.itemname.lower())
    
    @property
    def ldm_total(self) -> float:
        return sum(orderline.ldm for orderline in self.orderlines)

    @property
    def kids_total(self) -> int:
        return len(self.kids)

    @property
    def hay_direct_total(self) -> int:
        return sum(1 for kid in self.kids if kid.is_hay_direct)

    @property
    def big_orders_total(self) -> int:
        return sum(1 for kid in self.kids if kid.is_big)

    @property
    def small_orders_total(self) -> int:
        return sum(1 for kid in self.kids if not kid.is_big)

    @property
    def potentially_delayed_total(self) -> int:
        return sum(1 for kid in self.kids if kid.is_delayed)

    @property
    def items_in_big_orders_total(self) -> int:
        return sum(kid.number_of_items for kid in self.kids if kid.is_big)

    @property
    def items_in_small_orders_total(self) -> int:
        return sum(kid.number_of_items for kid in self.kids if not kid.is_big)

    @property
    def kids_in_pick_series(self) -> int:
        return sum(1 for kid in self.kids if kid.pickseries)

    @property
    def all_ordernumbers(self) -> list[str]:
        return [ordernumber for kid in self.kids for ordernumber in kid.ordernumbers]

    @property
    def hay_direct_kids(self) -> list[Kid]:
        return [kid for kid in self.kids if kid.is_hay_direct]

    @property
    def big_kids(self) -> list[Kid]:
        return [kid for kid in self.kids if kid.is_big]

    @property
    def small_ordernumbers(self) -> list:
        return [ordernumber for kid in self.kids for ordernumber in kid.ordernumbers if not kid.is_big]

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

    def get_day_report(self) -> str:
        day_report = Report.generate_day_head(self.weekday,
                                              self.date,
                                              self.items_total,
                                              self.items_in_small_orders_total,
                                              self.items_in_big_orders_total,
                                              self.ldm_total,
                                              self.orders_total,
                                              self.small_orders_total,
                                              self.big_orders_total,
                                              len(self.kids),
                                              self.kids_in_pick_series,
                                              self.dates,
                                              self.countries,
                                              self.all_ordernumbers,
                                              self.hay_direct_kids,
                                              self.big_kids,
                                              self.small_ordernumbers)

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
    