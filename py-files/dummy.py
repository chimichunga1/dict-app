import falcon
import msgpack
import couchdb
from array import array
import json
import os
from faker import Faker
from deepdiff import DeepDiff  # For Deep Difference of 2 objects
from deepdiff import DeepSearch  # For finding if item exists in an object
import json


couch = couchdb.Server()

db = couch['dictionary_search']
dbSearch = couch['job_spec']
dbSearchLog = couch['searchlogs']


doc_insert_data = {}

id_keyword = faker.name()
display = faker.name()


doc_insert_data.update({'_id':id_keyword.lower()})



doc_insert_data.update({'display':doc[0]})
doc_insert_data.update({'synonymous':doc[1]}) 
doc_insert_data.update({'misspell':doc[2]}) 
doc_insert_data.update({'suggestion':doc[3]})       
doc_insert_data.update({'status':'active'})
doc_insert_data.update({'history':[]})
db.save(doc_insert_data) #save database 

