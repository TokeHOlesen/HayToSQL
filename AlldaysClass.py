class Alldays:
    SHIPPING_DAYS = {
    "BG": (2, ),
    "CH": (2, 4),
    "CZ": (0, 3),
    "EE": (0, 3),
    "ES": (0, 2, 4),
    "FI": (2, 4),
    "FR": (0, 3, 4),
    "GR": (3, ),
    "HR": (3, ),
    "HU": (0, 3),
    "IT": (0, 2, 4),
    "LT": (0, 3),
    "LV": (0, 3),
    "NO": (3, ),
    "PL": (0, 3),
    "PT": (0, 3),
    "RO": (2, ),
    "SI": (3, ),
    "SK": (0, 3),
    "SM": (0, 2, 4),
    "TR": (3, )
}
    
    def __init__(self) -> None:
        self._days = []
        
    def __iter__(self):
        return iter(self._days)
    
    def get_day(self, index):
        return self.days[index]
    
    def add_day(self, day):
        self._days.append(day)
    
    def calculate_kids_for_all_days(self):
        for day in self._days:
            day.calculate_kids()
    
    def move_lines_to_match_date(self):
        """
        If an orderline's date falls on a day on which orders to the orderline's country may not be shipped,
        moves the orderline back to the nearest allowed date.
        If the orderline is moved all the way back to monday without reaching an allowed day, the orderline's
        "message" property is set to "Forsinket" to mark is as delayed.
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
                                    orderline.message = "Forsinket"
                                self._days[target_weekday].add_line(orderline)
                                day.remove_line(orderline)