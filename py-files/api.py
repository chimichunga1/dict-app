import falcon
import msgpack
import couchdb
from array import array
import json
import os
couch = couchdb.Server()

db = couch['dictionary_search']
dbSearch = couch['job_spec']
dbSearchLog = couch['searchlogs']





class JobSpecResource(object):
    def on_get(self, req, resp):
        SearchResults = []
        for JobSpecDoc in dbSearch.view('jobspecdoc/jobspecview'):
            SearchResults.append(JobSpecDoc)
        print(SearchResults)
        resp.body = json.dumps(SearchResults, ensure_ascii=False)
        resp.status = falcon.HTTP_200

# falcon.API instances are callable WSGI apps
app = falcon.API()
# Resources are represented by long-lived class instances
JobSpecResource = JobSpecResource()
# things will handle all requests to the '/things' URL path
app.add_route('/dictionary/JobSpecResource', JobSpecResource)