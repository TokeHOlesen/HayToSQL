from OrderlineClass import Orderline


class Item:
    def __init__(self,
                 item_number: str,
                 item_name: str,
                 item_color: str,
                 number: int):
        self.item_number = item_number
        self.item_name = item_name
        self.item_color = item_color
        self.number = number


class Kid:
    """
    Each object of this class contains information about a group of orders that share a delivery address and can be
    packaged together.
    """
    BIG_ORDER: int = 30  # If an object of this class has orders for this many items, self.is_big will be set to True

    def __init__(self,
                 orderline_list: list[Orderline]
                 ) -> None:
        # Since these values are shared between all orders making up a KID, those from element [0] are copied
        first_orderline: Orderline = orderline_list[0]
        self.address: str = first_orderline.address
        self.custname: str = first_orderline.custname
        self.pickseries: str = first_orderline.pickseries
        self.location: str = first_orderline.location
        self.city: str = first_orderline.city
        self.postcode: str = first_orderline.postcode
        self.country: str = first_orderline.country

        # These two are sets so the elements are unique
        self.dates: set = set()
        self.ordernumbers: set = set()

        self.number_of_items: int = 0
        self.ldm: float = 0
        self.is_moved_back: bool = False
        self.is_big: bool = False
        self.is_delayed: bool = False
        self.is_hay_direct: bool = False

        self.all_items: list[Item] = []

        for orderline in orderline_list:
            self.dates.add(orderline.date)
            self.ordernumbers.add(orderline.ordernumber)
            self.number_of_items += orderline.number_of_items
            self.ldm += orderline.ldm
            # Sets these to True if at least one Orderline's corresponding property is True
            self.is_moved_back = orderline.is_moved_back if orderline.is_moved_back else self.is_moved_back
            self.is_hay_direct = orderline.is_hay_direct if orderline.is_hay_direct else self.is_hay_direct
            self.is_delayed = orderline.is_delayed if orderline.is_delayed else self.is_delayed
            # Counts all items and adds a new Item object to self.all_items - or updates the total number of items with
            # that number if the item already exists
            for item in self.all_items:
                if item.item_number == orderline.itemnumber:
                    item.number += orderline.number_of_items
                    break
            else:
                self.all_items.append(Item(orderline.itemnumber,
                                           orderline.itemname,
                                           orderline.color if orderline.color is not None else "",
                                           orderline.number_of_items))
            self.all_items.sort(key=lambda this_item: this_item.item_number)

        self.is_big = (self.number_of_items >= self.BIG_ORDER)

        # Converts the set to a list, so it can be sorted
        self.dates = list(self.dates)
        self.dates.sort()
