# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: orders.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0corders.proto\x12\x06orders\"F\n\x0cOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\x03 \x01(\x05\"2\n\rOrderResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x10\n\x08order_id\x18\x02 \x01(\t2\x85\x01\n\x0cOrderService\x12\x39\n\nPlaceOrder\x12\x14.orders.OrderRequest\x1a\x15.orders.OrderResponse\x12:\n\x0bUpdateOrder\x12\x14.orders.OrderRequest\x1a\x15.orders.OrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'orders_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDERREQUEST']._serialized_start=24
  _globals['_ORDERREQUEST']._serialized_end=94
  _globals['_ORDERRESPONSE']._serialized_start=96
  _globals['_ORDERRESPONSE']._serialized_end=146
  _globals['_ORDERSERVICE']._serialized_start=149
  _globals['_ORDERSERVICE']._serialized_end=282
# @@protoc_insertion_point(module_scope)
