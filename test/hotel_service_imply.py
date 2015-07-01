import hotel_tag_pb2 as pb_test

def ActuallyInit(obj):
    err = []
    obj.IsInitialized(err)
    for field in err:
        attr = obj.__getattribute__(field)
        try:
            obj.__setattr__(field, attr)
        except:
            ActuallyInit(attr)

class hotel_service_impl(pb_test.HotelService):
    def get_hotel_details(self, controller, request, done):
        ht = request.name
        #print "In get_hotel_details! " +  ht
        response = pb_test.hotel()
        ActuallyInit(response)

        # Sleeping to show asynchronous behavior on client end.
        # time.sleep(1)

        # We're done, call the run method of the done callback
        done.run(response)


