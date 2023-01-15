from typing import Protocol, BinaryIO


class IExporter(Protocol):
    def save(self, data: list) -> BinaryIO:
        ...
