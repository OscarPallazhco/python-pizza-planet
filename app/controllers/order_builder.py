from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class OrderBuilder(ABC):
    """
    The OrderBuilder interface specifies methods for creating the different parts of
    the Order objects.
    """
    @abstractmethod
    def set_data(self, data) -> None:
        pass

    @abstractmethod
    def check_required_info(self) -> None:
        pass

    @abstractmethod
    def check_size(self) -> None:
        pass

    @abstractmethod
    def calculate_order_price(self) -> None:
        pass

    @abstractmethod
    def create(self) -> None:
        pass