# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import PTSL_pb2 as PTSL__pb2


class PTSLStub(object):
    """*
    Service for handling different types of ProTools commands using PTSL Client.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendGrpcRequest = channel.unary_unary(
                '/ptsl.PTSL/SendGrpcRequest',
                request_serializer=PTSL__pb2.Request.SerializeToString,
                response_deserializer=PTSL__pb2.Response.FromString,
                )
        self.SendGrpcStreamingRequest = channel.unary_stream(
                '/ptsl.PTSL/SendGrpcStreamingRequest',
                request_serializer=PTSL__pb2.Request.SerializeToString,
                response_deserializer=PTSL__pb2.Response.FromString,
                )


class PTSLServicer(object):
    """*
    Service for handling different types of ProTools commands using PTSL Client.
    """

    def SendGrpcRequest(self, request, context):
        """*
        Send generic gRPC request and receive generic response.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendGrpcStreamingRequest(self, request, context):
        """*
        Send generic gRPC request and receive generic streaming responses.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PTSLServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendGrpcRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.SendGrpcRequest,
                    request_deserializer=PTSL__pb2.Request.FromString,
                    response_serializer=PTSL__pb2.Response.SerializeToString,
            ),
            'SendGrpcStreamingRequest': grpc.unary_stream_rpc_method_handler(
                    servicer.SendGrpcStreamingRequest,
                    request_deserializer=PTSL__pb2.Request.FromString,
                    response_serializer=PTSL__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ptsl.PTSL', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PTSL(object):
    """*
    Service for handling different types of ProTools commands using PTSL Client.
    """

    @staticmethod
    def SendGrpcRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ptsl.PTSL/SendGrpcRequest',
            PTSL__pb2.Request.SerializeToString,
            PTSL__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendGrpcStreamingRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ptsl.PTSL/SendGrpcStreamingRequest',
            PTSL__pb2.Request.SerializeToString,
            PTSL__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
