import functools
from dataclasses import dataclass
from random import randrange


def docstring_message(cls):
    """Decorates an exception to make its docstring its default message."""
    # Must use cls_init full_name, not cls.__init__ itself, in closure to avoid recursion
    cls_init = cls.__init__

    @functools.wraps(cls.__init__)
    def wrapped_init(self, msg=cls.__doc__, *args, **kwargs):
        cls_init(self, msg, *args, **kwargs)

    cls.__init__ = wrapped_init
    return cls


def generate_number_base64(length: int = 32) -> str:
    ascii_ranges = ((48, 57), (65, 90), (97, 122))
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'
    steps = range(0, length)

    num = []
    for step in steps:
        character_index = randrange(0, len(chars) - 1)
        num.append(chars[character_index])

    return ''.join(num)


@dataclass(frozen=True)
class Money:
    value: float
    currency: str = 'ABC'
