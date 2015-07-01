#!/usr/bin/python

import os, sys
sys.path.append(os.path.abspath('../pylib/src'))
import gorpc.server
import hotel_tag_pb2 as pb_test
import hotel_service_imply

"""
needed coz PB dont initialize default values !
"""
def ActuallyInit(obj):
    err = []
    obj.IsInitialized(err)
    for field in err:
        attr = obj.__getattribute__(field)
        try:
            obj.__setattr__(field, attr)
        except:
            ActuallyInit(attr)

# create and fill test message
pb=pb_test.hotel()
pb.hn = "The Royal Marigold Hotel"
#print pb.hotel_url
ActuallyInit(pb)


#server = gorpc.server.SocketRpcServer(8090)
server = gorpc.server.GreenStreamServer(8090)
server.registerService(hotel_service_imply.hotel_service_impl())
server.run()



