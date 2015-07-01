#!/usr/bin/python
# Standard library imports
#import SocketServer
from gevent import monkey
monkey.patch_all()
import logging
import gevent
import gevent.server
import gevent.socket
# Third-party imports


# Module imports
from gorpc import rpc_pb2 as rpc_pb
from gorpc.controller import SocketRpcController
from gorpc import error



class NullHandler(logging.Handler):
    '''A null logging handler to prevent clients that don't require the
    logging package from reporting no handlers found.'''
    def emit(self, record):
        pass

class Callback():
    '''Class to allow execution of client-supplied callbacks.'''

    def __init__(self):
        self.invoked = False
        self.response = None

    def run(self, response):
        self.response = response
        self.invoked = True

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


class GreenStreamServer:

    def __init__(self, port, host='localhost'):
        '''port - Port this server is started on'''
        self.port = port
        self.host = host
        self.serviceMap = {}
        self._stream_server = gevent.server.StreamServer((host,port),
                                                         self._handle_connection)
    def registerService(self, service):
        '''Register an RPC service.'''
        self.serviceMap[service.GetDescriptor().full_name] = service


    def _handle_connection(self, socket, addr):
        socket.setsockopt(gevent.socket.SOL_TCP, gevent.socket.TCP_NODELAY, 1)
        socket.setsockopt(gevent.socket.IPPROTO_TCP, gevent.socket.TCP_NODELAY, 1)
        f = socket.makefile('r+b', bufsize=0)

        #rsp_queue = gevent.queue.Queue()
        #is_connection_closed = [False]

  
        def recv_req():
            content = ""
            while True:
                try:
                    recv_buf = f.read()
                    content += recv_buf
                    #print " got  data .." + str(len(recv_buf))
                    if not recv_buf :
                        break
                except Exception, e:
                    logging.warning('recv_req error: ' + str(e))
                    break



            # Evaluate and execute the request
            rpcResponse = self.validateAndExecuteRequest(content)
            log.debug("Response to return to client \n %s" % rpcResponse)

            f.write(rpcResponse.SerializeToString())
            f.flush()

        recv_req()
        #workers = [gevent.spawn(recv_req)]
        #gevent.joinall(workers)


    def validateAndExecuteRequest(self, input):
        '''Match a client request to the corresponding service and method on
        the server, and then call the service.'''

        # Parse and validate the client's request
        try:
            request = self.parseServiceRequest(input)
        except error.BadRequestDataError, e:
            return self.handleError(e)

        # Retrieve the requested service
        try:
            service = self.retrieveService(request.service_name)
        except error.ServiceNotFoundError, e:
            return self.handleError(e)

        # Retrieve the requested method
        try:
            method = self.retrieveMethod(service, request.method_name)
        except error.MethodNotFoundError, e:
            return self.handleError(e)

        # Retrieve the protocol message
        try:
            proto_request = self.retrieveProtoRequest(service, method, request)
        except error.BadRequestProtoError, e:
            return self.handleError(e)

        # Execute the specified method of the service with the requested params
        try:
            response = self.callMethod(service, method, proto_request)
        except error.RpcError, e:
            return self.handleError(e)

        return response


    def parseServiceRequest(self, bytestream_from_client):
        '''Validate the data stream received from the client.'''

        #print 'got request : ' + str(len(bytestream_from_client))

        # Convert the client request into a PB Request object
        request = rpc_pb.Request()

        # Catch anything which isn't a valid PB bytestream
        try:
            request.MergeFromString(bytestream_from_client)
        except Exception, e:
            raise error.BadRequestDataError("Invalid request from \
                                            client (decodeError): " + str(e))

        # Check the request is correctly initialized
        if not request.IsInitialized():
            raise error.BadRequestDataError("Client request is missing \
                                             mandatory fields")
        log.debug('Request = %s' % request)

        return request

    def retrieveService(self, service_name):
        '''Match the service request to a registered service.'''
        service = self.serviceMap.get(service_name)
        if service is None:
            msg = "Could not find service '%s'" % service_name
            raise error.ServiceNotFoundError(msg)

        return service

    def retrieveMethod(self, service, method_name):
        '''Match the method request to a method of a registered service.'''
        method = service.DESCRIPTOR.FindMethodByName(method_name)
        if method is None:
            msg = "Could not find method '%s' in service '%s'"\
                   % (method_name, service.DESCRIPTOR.name)
            raise error.MethodNotFoundError(msg)

        return method

    def retrieveProtoRequest(self, service, method, request):
        ''' Retrieve the users protocol message from the RPC message'''
        proto_request = service.GetRequestClass(method)()
        try:
            proto_request.ParseFromString(request.request_proto)
        except Exception, e:
            raise error.BadRequestProtoError(unicode(e))

        # Check the request parsed correctly
        if not proto_request.IsInitialized():
            raise error.BadRequestProtoError('Invalid protocol request \
                                              from client')

        return proto_request

    def callMethod(self, service, method, proto_request):
        '''Execute a service method request.'''
        log.debug('Calling service %s' % service)
        log.debug('Calling method %s' % method)

        # Create the controller (initialised to success) and callback
        controller = SocketRpcController()
        callback = Callback()
        try:
            service.CallMethod(method, controller, proto_request, callback)
        except Exception, e:
            raise error.RpcError(unicode(e))

        # Return an RPC response, with payload defined in the callback
        response = rpc_pb.Response()
        if callback.response:
            response.callback = True
            response.response_proto = callback.response.SerializeToString()
        else:
            response.callback = callback.invoked

        # Check to see if controller has been set to not success by user.
        if controller.failed():
            response.error = controller.error()
            response.error_reason = rpc_pb.RPC_FAILED

        return response

    def handleError(self, e):
        '''Produce an RPC response to convey a server error to the client.'''
        msg = "%d : %s" % (e.rpc_error_code, e.message)
        log.error(msg)

        # Create error reply
        response = rpc_pb.Response()
        response.error_reason = e.rpc_error_code
        response.error = e.message
        return response

    def run(self):
        '''Activate the server.'''
        log.info('Running server on port %d' % self.port)
        self._stream_server.serve_forever()






