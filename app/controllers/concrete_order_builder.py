from .order_builder import OrderBuilder
from ..common.utils import check_required_keys
from ..repositories.managers import (IngredientManager, OrderManager,
                                     SizeManager, BeverageManager)


class ConcreteOrderBuilder(OrderBuilder):

    def __init__(self):
        self.manager = OrderManager
        self.data = {}
        self.ingredients = []
        self.beverages = []
        self.error = None
        self.price = None
        self.size = None


    def set_data(self, data) -> None:
        self.data = data


    def check_required_info(self, required_info) -> None:
        if not check_required_keys(required_info, self.data):
            self.error = (None, 'Invalid order payload')


    def check_size(self) -> None:
        if self.error: return self
        size = SizeManager.get_by_id(self.data.get('size_id'))
        if not size:
            self.error = (None, 'Invalid size for Order')
        self.size = size


    def calculate_order_price(self) -> None:
        if self.error: return self
        price = self.size.get('price') + self.__calculate_ingredients_price() + self.__calculate_beverages_price()
        self.price = round(price, 2)


    def __calculate_ingredients_price(self) -> None:
        if self.error: return self
        ingredient_ids = self.data.pop('ingredients', [])
        self.ingredients = IngredientManager.get_by_id_list(ingredient_ids)
        return sum(ingredient.price for ingredient in self.ingredients)
        

    def __calculate_beverages_price(self) -> None:
        if self.error: return self
        beverage_ids = self.data.pop('beverages', [])
        self.beverages = BeverageManager.get_by_id_list(beverage_ids)
        return sum(beverage.price for beverage in self.beverages)

    def create(self) -> None:
        if self.error: return self.error
        self.data["total_price"] = self.price
        return self.manager.create(self.data, self.ingredients, self.beverages), None