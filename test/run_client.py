import os, sys, time
sys.path.append(os.path.abspath('../pylib/src'))
from  gorpc import RpcService
import hotel_tag_pb2 as pb_test
import cProfile, pstats, StringIO
pr = cProfile.Profile()

# Server details
hostname = 'localhost'
port = 8090

#import pdb; pdb.set_trace()

# Create a request
request = pb_test.hotel_request()
request.name = 'Hotel XYZ'


# Create a new service instance
hotel_service = RpcService(pb_test.HotelService_Stub,
                     port,
                     hostname)

#time.sleep(5)


try:
    print 'Making synchronous call'

    t1 = time.time()
    #response = hotel_service.get_hotel_details(request, timeout=10000)
    response = hotel_service.get_hotel_details(request)
    print time.time() - t1
except Exception, ex:
    print 'Exception :' + str(ex)
    print ex.message
