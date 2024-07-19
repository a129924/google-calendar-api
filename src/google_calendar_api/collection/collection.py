from collections.abc import Mapping
from typing import Any

__all__ = ["remove_dict_value_none"]


def remove_dict_value_none(dic: Mapping[str, Any]) -> Mapping[str, Any]:
    return {k: v for k, v in dic.items() if v is not None}
