from datetime import datetime, timedelta

from DayClass import Day
from OrderlineClass import Orderline
from ReportClass import Report


class Week:
    SHIPPING_DAYS = {
        "BG": (2,),
        "CH": (2, 4),
        "CZ": (0, 3),
        "EE": (0, 3),
        "ES": (0, 2, 4),
        "FI": (2, 4),
        "FR": (0, 3, 4),
        "GR": (3,),
        "HR": (3,),
        "HU": (0, 3),
        "IT": (0, 2, 4),
        "LT": (0, 3),
        "LV": (0, 3),
        "NO": (3,),
        "PL": (0, 3),
        "PT": (0, 3),
        "RO": (2,),
        "SI": (3,),
        "SK": (0, 3),
        "SM": (0, 2, 4),
        "TR": (3,)
    }

    def __init__(self, cursor, start_date, end_date) -> None:
        self._days = []
        self.start_date = datetime.strptime(start_date, r"%Y-%m-%d").date()
        self.end_date = datetime.strptime(end_date, r"%Y-%m-%d").date()
        for i in range((self.end_date - self.start_date).days + 1):
            day_date = (self.start_date + timedelta(days=i))
            day = Day(day_date)
            cursor.execute("""SELECT * FROM hay
                                   WHERE address IN
                                   (SELECT address FROM hay GROUP BY address HAVING MIN(date) = ?)
                                   AND location IS NOT 'DSV';""", (day_date,))
            day_data_line = cursor.fetchone()
            while day_data_line is not None:
                day.add_line(Orderline(day_data_line))
                day_data_line = cursor.fetchone()
            self.add_day(day)
        self.move_lines_to_match_date()
        self.calculate_kids_for_all_days()

        self.dsv_orderlines = []
        cursor.execute("""SELECT * FROM hay WHERE location IS 'DSV';""")
        dsv_data_line = cursor.fetchone()
        while dsv_data_line is not None:
            self.dsv_orderlines.append(Orderline(dsv_data_line))
            dsv_data_line = cursor.fetchone()

    def __iter__(self):
        return iter(self._days)

    def add_day(self, day):
        self._days.append(day)

    @property
    def number_of_orders(self):
        total = 0
        for day in self._days:
            total += day.orders_total
        return total

    @property
    def number_of_items(self):
        total = 0
        for day in self._days:
            total += day.items_total
        return total

    @property
    def number_of_dsv_items(self):
        total = 0
        for dsv_orderline in self.dsv_orderlines:
            total += dsv_orderline.number_of_items
        return total

    @property
    def ldm_total(self):
        total = 0
        for day in self._days:
            total += day.ldm_total
        return round(total, 2)

    @property
    def dsv_ldm_total(self):
        total = 0
        for orderline in self.dsv_orderlines:
            total += orderline.loadmeter
        return round(total, 2)

    @property
    def kids_total(self):
        total = 0
        for day in self._days:
            total += day.kids_total
        return total

    @property
    def hay_direct_kids_total(self):
        total = 0
        for day in self._days:
            total += day.hay_direct_total
        return total

    @property
    def potentially_delayed_orders_total(self):
        total = 0
        for day in self._days:
            total += day.potentially_delayed_total()
        return total

    def calculate_kids_for_all_days(self):
        for day in self._days:
            day.calculate_kids()

    def move_lines_to_match_date(self):
        """
        If an orderline's date falls on a day on which orders to the orderline's country may not be shipped,
        moves the orderline back to the nearest allowed date.
        If the orderline is moved all the way back to monday without reaching an allowed day, the orderline's
        "is_delayed" property is set to True to mark is as delayed.
        """
        for day in self._days:
            for country in day.countries:
                weekday = target_weekday = day.weekday_number
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

    def generate_report(self):
        weekly_report = Report.generate_html_head()
        weekly_report += Report.generate_header(self.start_date, self.end_date)
        weekly_report += Report.generate_week_summary(self.number_of_items,
                                                      self.number_of_dsv_items,
                                                      self.number_of_orders,
                                                      self.ldm_total,
                                                      self.dsv_ldm_total,
                                                      self.kids_total,
                                                      self.hay_direct_kids_total,
                                                      self.potentially_delayed_orders_total)

        for day in self._days:
            weekly_report += day.get_day_report()

        weekly_report += Report.generate_html_tail()

        return weekly_report
