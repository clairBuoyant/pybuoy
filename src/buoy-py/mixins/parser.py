"""Provide the ParserMixin class."""


class ParserMixin:
    """Interface for Buoy classes and its composites."""

    def parse(self, data: str):
        ...
