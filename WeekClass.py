import sqlite3
from datetime import datetime, timedelta

from DayClass import Day
from OrderlineClass import Orderline
from ReportClass import Report


class Week:
    SHIPPING_DAYS = {
        "AT": (0, 1, 2, 3, 4),
        "BE": (0, 1, 2, 3, 4),
        "BG": (2,),
        "CH": (2, 4),
        "CZ": (0, 3),
        "DE": (0, 1, 2, 3, 4),
        "DK": (0, 1, 2, 3, 4),
        "EE": (0, 3),
        "ES": (0, 2, 4),
        "FI": (2, 4),
        "FR": (0, 3, 4),
        "GB": (0, 1, 2, 3, 4),
        "GR": (3,),
        "HR": (3,),
        "HU": (0, 3),
        "IE": (0, 1, 2, 3, 4),
        "IT": (0, 2, 4),
        "LT": (0, 3),
        "LU": (0, 1, 2, 3, 4),
        "LV": (0, 3),
        "NL": (0, 1, 2, 3, 4),
        "NO": (3,),
        "PL": (0, 3),
        "PT": (0, 3),
        "RO": (2,),
        "SE": (0, 1, 2, 3, 4),
        "SI": (3,),
        "SK": (0, 3),
        "SM": (0, 2, 4),
        "TR": (3,),
        "XI": (0, 1, 2, 3, 4)
    }

    def __init__(self,
                 cursor: sqlite3.Cursor,
                 start_date: str,
                 end_date: str) -> None:
        self._days: list[Day] = []
        self.start_date: datetime.date = datetime.strptime(start_date, r"%Y-%m-%d").date()
        self.end_date: datetime.date = datetime.strptime(end_date, r"%Y-%m-%d").date()
        for i in range((self.end_date - self.start_date).days + 1):
            day_date: datetime.date = (self.start_date + timedelta(days=i))
            day: Day = Day(day_date)
            cursor.execute("""SELECT * FROM hay
                                   WHERE address IN
                                   (SELECT address FROM hay GROUP BY address HAVING MIN(date) = ?)
                                   AND location IS NOT 'DSV';""", (day_date,))
            day_data_line: tuple = cursor.fetchone()
            while day_data_line is not None:
                day.add_line(Orderline(day_data_line))
                day_data_line = cursor.fetchone()
            self.add_day(day)
        self.move_lines_to_match_date()
        self.calculate_kids_for_all_days()

        self.dsv_orderlines: list[Orderline] = []
        cursor.execute("""SELECT * FROM hay WHERE location IS 'DSV';""")
        dsv_data_line: tuple = cursor.fetchone()
        while dsv_data_line is not None:
            self.dsv_orderlines.append(Orderline(dsv_data_line))
            dsv_data_line = cursor.fetchone()

    def move_lines_to_match_date(self) -> None:
        """
        If an orderline's date falls on a day on which orders to the orderline's country may not be shipped,
        moves the orderline back to the nearest allowed date.
        If the orderline is moved all the way back to monday without reaching an allowed day, the orderline's
        "is_delayed" property is set to True to mark is as delayed.
        """
        for day in self._days:
            for country in day.countries:
                weekday: int = day.weekday_number
                target_weekday: int = day.weekday_number
                if country in self.SHIPPING_DAYS:
                    if weekday not in self.SHIPPING_DAYS[country]:
                        while target_weekday not in self.SHIPPING_DAYS[country] and target_weekday > 0:
                            target_weekday -= 1
                        for orderline in day.orderlines[:]:
                            if orderline.country == country:
                                if target_weekday == 0 and target_weekday not in self.SHIPPING_DAYS[country]:
                                    orderline.is_delayed = True
                                orderline.is_moved_back = True
                                self._days[target_weekday].add_line(orderline)
                                day.remove_line(orderline)

    def calculate_kids_for_all_days(self) -> None:
        for day in self._days:
            day.calculate_kids()

    def __iter__(self) -> iter:
        return iter(self._days)

    def add_day(self, day) -> None:
        self._days.append(day)

    @property
    def number_of_orders(self) -> int:
        return sum(day.orders_total for day in self._days)

    @property
    def number_of_big_orders(self) -> int:
        return sum(day.big_orders_total for day in self._days)

    @property
    def number_of_small_orders(self) -> int:
        return sum(day.small_orders_total for day in self._days)

    @property
    def number_of_items(self) -> int:
        return sum(day.items_total for day in self._days)

    @property
    def number_of_items_in_big_orders(self) -> int:
        return sum(day.items_in_big_orders_total for day in self._days)

    @property
    def number_of_items_in_small_orders(self) -> int:
        return sum(day.items_in_small_orders_total for day in self._days)

    @property
    def number_of_dsv_items(self) -> int:
        return sum(dsv_orderline.number_of_items for dsv_orderline in self.dsv_orderlines)

    @property
    def number_of_furniture(self) -> int:
        return sum(day.furniture_total for day in self._days)

    @property
    def number_of_dsv_furniture(self) -> int:
        return sum(orderline.number_of_items
                   for orderline in self.dsv_orderlines
                   if "cushion" not in orderline.itemname.lower())

    @property
    def number_of_cushions(self) -> int:
        return sum(day.cushions_total for day in self._days)

    @property
    def number_of_dsv_cushions(self) -> int:
        return sum(orderline.number_of_items
                   for orderline in self.dsv_orderlines
                   if "cushion" in orderline.itemname.lower())

    @property
    def ldm_total(self) -> float:
        return round(sum(day.ldm_total for day in self._days), 2)

    @property
    def dsv_ldm_total(self) -> float:
        return round(sum(orderline.ldm for orderline in self.dsv_orderlines), 2)

    @property
    def kids_total(self) -> int:
        return sum(day.kids_total for day in self._days)

    @property
    def hay_direct_kids_total(self) -> int:
        return sum(day.hay_direct_total for day in self._days)

    @property
    def kids_with_pick_series(self) -> int:
        return sum(day.kids_in_pick_series for day in self._days)

    @property
    def potentially_delayed_orders_total(self) -> int:
        return sum(day.potentially_delayed_total for day in self._days)

    def generate_report(self) -> str:
        weekly_report = Report.generate_html_head()
        weekly_report += Report.generate_header(self.start_date, self.end_date)
        weekly_report += Report.generate_week_summary(self.number_of_items,
                                                      self.number_of_items_in_small_orders,
                                                      self.number_of_items_in_big_orders,
                                                      self.number_of_dsv_items,
                                                      self.number_of_furniture,
                                                      self.number_of_dsv_furniture,
                                                      self.number_of_cushions,
                                                      self.number_of_dsv_cushions,
                                                      self.number_of_orders,
                                                      self.number_of_small_orders,
                                                      self.number_of_big_orders,
                                                      self.ldm_total,
                                                      self.dsv_ldm_total,
                                                      self.kids_total,
                                                      self.kids_with_pick_series,
                                                      self.hay_direct_kids_total,
                                                      self.potentially_delayed_orders_total)

        for day in self._days:
            weekly_report += day.get_day_report()

        weekly_report += Report.generate_html_tail()

        return weekly_report
