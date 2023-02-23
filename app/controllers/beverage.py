from sqlalchemy.exc import SQLAlchemyError
from ..repositories.managers import BeverageManager
from ..common.utils import check_required_keys
from .base import BaseController


class BeverageController(BaseController):
    manager = BeverageManager
    __required_info = ('name', 'price')

    @classmethod
    def create(cls, beverage: dict):
        current_beverage = beverage.copy()
        if not check_required_keys(cls.__required_info, current_beverage):
            return None, 'Invalid beverage payload'

        try:
            return cls.manager.create(current_beverage), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
