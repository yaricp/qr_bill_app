from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BillUrl(_message.Message):
    __slots__ = ("url", "tg_user_id")
    URL_FIELD_NUMBER: _ClassVar[int]
    TG_USER_ID_FIELD_NUMBER: _ClassVar[int]
    url: str
    tg_user_id: int
    def __init__(self, url: _Optional[str] = ..., tg_user_id: _Optional[int] = ...) -> None: ...

class BillInfo(_message.Message):
    __slots__ = ("date", "seller", "address", "summ")
    DATE_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUMM_FIELD_NUMBER: _ClassVar[int]
    date: str
    seller: str
    address: str
    summ: float
    def __init__(self, date: _Optional[str] = ..., seller: _Optional[str] = ..., address: _Optional[str] = ..., summ: _Optional[float] = ...) -> None: ...

class TotalSumm(_message.Message):
    __slots__ = ("summ", "tg_user_id")
    SUMM_FIELD_NUMBER: _ClassVar[int]
    TG_USER_ID_FIELD_NUMBER: _ClassVar[int]
    summ: float
    tg_user_id: int
    def __init__(self, summ: _Optional[float] = ..., tg_user_id: _Optional[int] = ...) -> None: ...

class TgUserID(_message.Message):
    __slots__ = ("tg_user_id",)
    TG_USER_ID_FIELD_NUMBER: _ClassVar[int]
    tg_user_id: int
    def __init__(self, tg_user_id: _Optional[int] = ...) -> None: ...

class UserLang(_message.Message):
    __slots__ = ("lang",)
    LANG_FIELD_NUMBER: _ClassVar[int]
    lang: str
    def __init__(self, lang: _Optional[str] = ...) -> None: ...

class UserLangEditForm(_message.Message):
    __slots__ = ("tg_user_id", "lang")
    TG_USER_ID_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    tg_user_id: int
    lang: str
    def __init__(self, tg_user_id: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class LoginURL(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...
