# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import enum
from typing import Any, List, Optional

# models


class SqlQueryRequest:
    def __init__(self, tables: List[str], sql: str): ...


class SqlQueryResponse:
    def num_rows(self) -> int: ...
    def row_by_idx(self, idx: int) -> Optional[Row]: ...
    def iter_rows(self) -> RowIter: ...
    @property
    def affected_rows(self) -> int: ...


class DataType(enum.IntEnum):
    Null = 0
    Timestamp = 1
    Double = 2
    Float = 3
    Varbinary = 4
    String = 5
    UInt64 = 6
    UInt32 = 7
    UInt16 = 8
    UInt8 = 9
    Int64 = 10
    Int32 = 11
    Int16 = 12
    Int8 = 13
    Boolean = 14


class Column:
    def name(self) -> str: ...
    def value(self) -> Any: ...
    def data_type(self) -> DataType: ...


class Row:
    def column(self, name: str) -> Optional[Column]: ...
    def column_by_idx(self, idx: int) -> Optional[Column]: ...
    def num_cols(self) -> int: ...
    def iter_columns(self) -> ColumnIter: ...


class ColumnIter:
    def __iter__(self) -> Column: ...


class RowIter:
    def __iter__(self) -> Row: ...


class Value:
    pass


class ValueBuilder:
    def __init__(self): ...
    def null(self) -> Value: ...
    def timestamp(self, val: int) -> Value: ...
    def varbinary(self, val: bytes) -> Value: ...
    def string(self, val: str) -> Value: ...
    def double(self, val: float) -> Value: ...
    def float(self, val: float) -> Value: ...
    def uint64(self, val: int) -> Value: ...
    def uint32(self, val: int) -> Value: ...
    def uint16(self, val: int) -> Value: ...
    def int64(self, val: int) -> Value: ...
    def int32(self, val: int) -> Value: ...
    def int16(self, val: int) -> Value: ...
    def uint8(self, val: int) -> Value: ...
    def bool(self, val: bool) -> Value: ...


class Point:
    pass


class PointBuilder:
    def __init__(self, table: str) -> PointBuilder: ...
    def set_table(self, table: str): ...
    def set_timestamp(self, timestamp_ms: int): ...
    def set_tag(self, name: str, val: Value): ...
    def set_field(self, name: str, val: Value): ...
    def build(self) -> Point: ...


class WriteRequest:
    def __init__(self): ...
    def add_point(self, point: Point): ...
    def add_points(self, point: List[Point]): ...


class WriteResponse:
    def get_success(self) -> int: ...
    def get_failed(self) -> int: ...

# client


class Client:
    def __init__(self, endpoint: str): ...

    async def write(self, ctx: RpcContext,
                    req: WriteRequest) -> WriteResponse: ...
    async def sql_query(self, ctx: RpcContext,
                        req: SqlQueryRequest) -> SqlQueryResponse: ...


class RpcConfig:
    def __init__(self): ...
    thread_num: int
    max_send_msg_len: int
    max_recv_msg_len: int
    keepalive_time_ms: int
    keepalive_timeout_ms: int
    default_write_timeout_ms: int
    default_sql_query_timeout_ms: int
    connect_timeout_ms: int


class RpcContext:
    def __init__(self): ...
    timeout_ms: int
    database: str

class Authorization:
    def __init__(self): ...
    username: str
    password: str

class Builder:
    def __init__(self, endpoint: str): ...
    def set_rpc_config(self, conf: RpcConfig): ...
    def set_default_database(self, db: str): ...
    def set_authorization(self, auth: Authorization): ...
    def build(self) -> Client: ...
