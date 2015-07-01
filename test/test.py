#!/usr/bin/python

import os, sys, json
from pprint import pprint

import protobuf_json

import hotel_tag_pb2 as pb_test

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

# convert it to JSON and back
#pprint(pb.SerializeToString())
json_obj=protobuf_json.pb2json(pb)
with  open("tab.json","w+") as j_file:
	j_file.write(json.dumps(json_obj))
print "size of json : " + str(sys.getsizeof(json_obj))
pb2=protobuf_json.json2pb(pb_test.hotel(), json_obj)
with  open("tab.pb","w+") as p_file:
	p_file.write(pb2.SerializeToString())
print "size of pb : " + str(sys.getsizeof(pb2))


