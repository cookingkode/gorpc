__author__ = 'jyothi'

from gevent import monkey
monkey.patch_all()

import os, sys, time
from gevent.pool import Pool

sys.path.append(os.path.abspath('../pylib/src'))
from  gorpc import RpcService
import hotel_tag_pb2 as pb_test
import cProfile, pstats, StringIO
profile = cProfile.Profile()

# Server details
hostname = 'localhost'
port = 8090

#import pdb; pdb.set_trace()


def client(hotel):
    # Create a request
    request = pb_test.hotel_request()
    request.name = 'Hotel XYZ'

    profile.enable()
    t1 = time.time()
    # Create a new service instance
    hotel_service = RpcService(pb_test.HotelService_Stub,
                         port,
                         hostname)


    try:
    	t2 = time.time()
        response = hotel_service.get_hotel_details(request)
    	t3 = time.time()

    except Exception, ex:
        print 'Exception :' + str(ex)

    print str(time.time() -t1) +  " , " +  str(t3-t2)

    profile.disable()

    return response
    #time.sleep(5)


if __name__ == '__main__':
    hotels = ['goo'] * 100
    pool = Pool(20)
    while True :
    	pool.map(client,hotels)
