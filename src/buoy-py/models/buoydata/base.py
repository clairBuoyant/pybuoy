"""Provide the BuoyDataBase class."""
from ..base import BuoypyBase


class BuoyDataBase(BuoypyBase):
    def __init__(self, value=None, unit=None):
        self._unit = unit
        self._value = value
        super().__init__()

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value

    @unit.setter
    def unit(self, new_unit):
        self._unit = new_unit

    @value.setter
    def value(self, new_value):
        self._value = new_value
