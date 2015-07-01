#!/usr/bin/python

'''
error.py - Exception classes for the protobuf package.

This package contains exception classes mapped to the rpc.proto file.

'''

# Module imports
from gorpc import rpc_pb2 as rpc_pb


class ProtobufError(Exception):
    '''Base exception class for RPC protocol buffer errors.'''

    def __init__(self, message, rpc_error_code):
        '''ProtobufError constructor.

        message - Message string detailing error.
        rpc_error_code - Error code from rpc.proto file.
        '''
        Exception.__init__(self, message)
        self.rpc_error_code = rpc_error_code


class BadRequestDataError(ProtobufError):
    '''Exception generated for a BadRequestDataError.'''

    def __init__(self, message):
        super(BadRequestDataError, self).__init__(
            message, rpc_pb.BAD_REQUEST_DATA)


class BadRequestProtoError(ProtobufError):
    '''Exception generated for a BadRequestProtoError.'''

    def __init__(self, message):
        super(BadRequestProtoError, self).__init__(
            message, rpc_pb.BAD_REQUEST_PROTO)


class ServiceNotFoundError(ProtobufError):
    '''Exception generated for a ServiceNotFoundError.'''

    def __init__(self, message):
        super(ServiceNotFoundError, self).__init__(
            message, rpc_pb.SERVICE_NOT_FOUND)


class MethodNotFoundError(ProtobufError):
    '''Exception generated for a MethodNotFoundError.'''

    def __init__(self, message):
        super(MethodNotFoundError, self).__init__(
            message, rpc_pb.METHOD_NOT_FOUND)


class RpcError(ProtobufError):
    '''Exception generated for an RpcError.'''

    def __init__(self, message):
        super(RpcError, self).__init__(message, rpc_pb.RPC_ERROR)


class RpcFailed(ProtobufError):
    '''Exception generated for an RpcFailed.'''

    def __init__(self, message):
        super(RpcFailed, self).__init__(message, rpc_pb.RPC_FAILED)


class InvalidRequestProtoError(ProtobufError):
    '''Exception generated for an InvalidRequestProtoError.'''

    def __init__(self, message):
        super(InvalidRequestProtoError, self).__init__(
            message, rpc_pb.INVALID_REQUEST_PROTO)


class BadResponseProtoError(ProtobufError):
    '''Exception generated for a BadResponseProtoError.'''

    def __init__(self, message):
        super(BadResponseProtoError, self).__init__(
            message, rpc_pb.BAD_RESPONSE_PROTO)


class UnknownHostError(ProtobufError):
    '''Exception generated for an UnknownHostError.'''

    def __init__(self, message):
        super(UnknownHostError, self).__init__(message, rpc_pb.UNKNOWN_HOST)


class IOError(ProtobufError):
    '''Exception generated for an IOError.'''

    def __init__(self, message):
        super(IOError, self).__init__(message, rpc_pb.IO_ERROR)
