from typing import Protocol, Callable, TypeVar

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

T = TypeVar(name="T")


class PageController(Protocol):
    offset: int
    limit: int

    def pack(self):
        ...


class IPaginate(Protocol):
    limit: int
    offset: int
    pages: int
    current_page: int


def add_paginate_buttons(
    builder: InlineKeyboardBuilder,
    callback_data: Callable[..., PageController],
    paginate: IPaginate,
):
    current_page = f"{paginate.current_page}/{paginate.pages}"
    back_callback_data = callback_data(
        offset=paginate.offset - paginate.limit,
        limit=paginate.limit,
    )
    forward_callback_data = callback_data(
        offset=paginate.offset + paginate.limit, limit=paginate.limit
    )
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=back_callback_data.pack()),
        InlineKeyboardButton(text=current_page, callback_data="none"),
        InlineKeyboardButton(text="➡️", callback_data=forward_callback_data.pack()),
    )
