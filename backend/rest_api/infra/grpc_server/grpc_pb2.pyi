from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BillUrl(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class BillInfo(_message.Message):
    __slots__ = ("date", "seller", "summ")
    DATE_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    SUMM_FIELD_NUMBER: _ClassVar[int]
    date: str
    seller: str
    summ: float
    def __init__(self, date: _Optional[str] = ..., seller: _Optional[str] = ..., summ: _Optional[float] = ...) -> None: ...

class TotalSumm(_message.Message):
    __slots__ = ("summ",)
    SUMM_FIELD_NUMBER: _ClassVar[int]
    summ: float
    def __init__(self, summ: _Optional[float] = ...) -> None: ...
