from sqlalchemy.exc import SQLAlchemyError

from ..common.utils import check_required_keys
from ..repositories.managers import (IngredientManager, OrderManager,
                                     SizeManager, BeverageManager)
from .base import BaseController
from .concrete_order_builder import ConcreteOrderBuilder


class OrderController(BaseController):
    manager = OrderManager
    __required_info = ('client_name', 'client_dni', 'client_address', 'client_phone', 'size_id')


    @classmethod
    def create(cls, order: dict):
        try:
            builder = ConcreteOrderBuilder()
            builder.set_data(order.copy())
            builder.check_required_info(cls.__required_info)
            builder.check_size()
            builder.calculate_order_price()
            return builder.create()
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
