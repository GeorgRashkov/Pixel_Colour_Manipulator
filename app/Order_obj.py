from Enums import Enum_order

class Order_obj():

    def __init__(self, order_type:Enum_order = Enum_order.ascending, start:int = None, end:int = None, step:int = None):
        
        self.order_type = order_type
        self.start = start
        self.end = end
        self.step = step