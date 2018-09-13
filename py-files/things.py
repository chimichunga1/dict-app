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


############################################################
class Resource(object):
    def on_get(self, req, resp):

        doc=[]
        for item in db.view('searchdoc/searchview'):
            doc.append(item)
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
            # print(item)
############################################################
class getData(object):
    def on_post(self, req, resp):

        test_users = {}
        # print("Checking...")
        insert_data = req.media
        doc=[]
        doc_syn = []
        for item in dbSearch.view('jobspecdoc/jobspecview'):
            if insert_data['comment'].lower() in item.value['job_title'].lower():
                doc.append(item.value['job_title'])
        for item_dict in db.view('searchdoc/searchview'):
            if insert_data['comment'].lower() == item_dict.value['job_title'].lower():
                doc_syn=item_dict.value['synonymous']
        for item in dbSearch.view('jobspecdoc/jobspecview'):
            counter=0
            while(counter<len(doc_syn)):
                if doc_syn[counter].lower() == item.value['job_title'].lower():
                    doc.append(doc_syn[counter])
                counter=counter+1
        if not doc:
            doc.append('No Result Found')
        # print(doc)                
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
############################################################
class logSearch(object):
    def on_post(self, req, resp):

        insert_data = req.media
        dbSearchLog.save(insert_data)

        doc=[]
        doc.append(insert_data)
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
############################################################
class getDelete(object):
    def on_post(self, req, resp):

  
        insert_data = req.media
        # print(insert_data['value']['_id'])
        document=db.get(insert_data['value']['_id'])
        if 'status' in document:
 
            document['status'] = "deleted"
        db.save(document) #save database
 ############################################################
class UpdateJobTitle(object):
    def on_post(self, req, resp):

    
        insert_data = req.media
        document=db.get(insert_data['id'])
        # document=db.get(insert_data['id'])
        # print('========')
        # print(document['_id'])
        # print('====')
        # print(insert_data['_id'])
        if '_id' in document:
            document['_id'] = insert_data['_id']
        db.save(document) #save database 

############################################################
class UpdateSyno(object):
    def on_post(self, req, resp):

        insert_data = req.media
        counter_syno = 0
        for item_dict in db.view('searchdoc/searchview'):
            if insert_data['id'] == item_dict['value']['_id']:
                for test in item_dict['value']['synonymous']:
                    if insert_data['CurrentSyno'] == item_dict['value']['synonymous'][counter_syno]:
                        # print(item_dict['value']['synonymous'][counter_syno])
                        doc1=db.get(insert_data['id'])
                        doc1['synonymous'][counter_syno] = insert_data['NewSyno']
                        # print(doc1['synonymous'][counter_syno])
                        db.save(doc1)
                    counter_syno = counter_syno + 1 

############################################################
class UpdateKeywords(object):
    def on_post(self, req, resp):

        insert_data = req.media
        counter_keyword = 0
        for item_dict in db.view('searchdoc/searchview'):
            if insert_data['id'] == item_dict['value']['_id']:
                for test in item_dict['value']['misspell']:
                    if insert_data['CurrentKeyword'] == item_dict['value']['misspell'][counter_keyword]:
                        # print(item_dict['value']['keywords'][counter_keyword])
                        doc1=db.get(insert_data['id'])
                        doc1['misspell'][counter_keyword] = insert_data['NewKeyword']
                        # print(doc1['keywords'][counter_keyword])
                        db.save(doc1)
                    counter_keyword = counter_keyword + 1 

############################################################
class delSyno(object):
    def on_post(self, req, resp):

        insert_data = req.media
        counter_syno = 0
        # print(insert_data)
        for item_dict in db.view('searchdoc/searchview'):
            if insert_data['id'] == item_dict['value']['_id']:
                for test in item_dict['value']['synonymous']:
                    if insert_data['syno'] == item_dict['value']['synonymous'][counter_syno]:
                        # print(item_dict['value']['synonymous'][counter_syno])
                        doc1=db.get(insert_data['id'])
                        del doc1['synonymous'][counter_syno]
                        db.save(doc1)
                    counter_syno = counter_syno + 1 

############################################################
class delKeywords(object):
    def on_post(self, req, resp):
        
        insert_data = req.media
        counter_keywords = 0
        for item_dict in db.view('searchdoc/searchview'):
            if insert_data['id'] == item_dict['value']['_id']:
                for test in item_dict['value']['misspell']:
                    if insert_data['keywords'] == item_dict['value']['misspell'][counter_keywords]:
                        # print(item_dict['value']['misspell'][counter_keywords])
                        doc1=db.get(insert_data['id'])
                        del doc1['misspell'][counter_keywords]
                        db.save(doc1)
                    counter_keywords = counter_keywords + 1 


############################################################
class addSearch(object):
    def on_post(self, req, resp):
        doc = req.media
        get_name = (doc)
        counter_syno = 0
        counter_keyword = 0
        syno_list = []
        keyword_list=[]
        doc_data = {}
        for i in get_name[1]:
             get_syno = get_name[1][counter_syno]['name']
             syno_list.append(get_syno)
             counter_syno = counter_syno + 1
        for i in get_name[1]:
             get_keyword = get_name[0][counter_keyword]['name']
             keyword_list.append(get_keyword)

             counter_keyword = counter_keyword + 1
        doc_data.update({'_id':get_name[2].lower()}) 
        doc_data.update({'synonymous':syno_list}) 
        doc_data.update({'misspell':keyword_list}) 

        doc_data.update({'status':'active'})
        doc_data.update({'display':get_name[2]})
        db.save(doc_data)


############################################################
class addSynoKey(object):
    def on_post(self, req, resp):
        doc = req.media
        document=db.get(doc[2])
        LoopKeyword = doc
        counter_num = 0
        counter_keyword = 0
        if '_id' in document:
            for i in LoopKeyword[1]:
                get_keyword = doc[1][counter_num]['KeywordArray']
                document['misspell'].append(get_keyword)
                counter_num = counter_num + 1
            # print(document['misspell'])
            for i in LoopKeyword[0]:
                get_synonymous = doc[0][counter_keyword]['SynonymArray']
                document['synonymous'].append(get_synonymous)
                counter_keyword = counter_keyword + 1
            # print(document['synonymous'])


        db.save(document) #save database 



 


############################################################
class AddNewDict(object):
    def on_post(self, req, resp):
        doc = req.media
        doc_insert_data = {}

        doc_insert_data.update({'_id':doc[0].lower()})
        doc_insert_data.update({'display':doc[0]})
        doc_insert_data.update({'synonymous':doc[1]}) 
        doc_insert_data.update({'misspell':doc[2]}) 
        doc_insert_data.update({'status':'active'})
        doc_insert_data.update({'history':[]})



        db.save(doc_insert_data) #save database 



 

############################################################


class displaySearch(object):
    def on_get(self, req, resp):
        
        SearchResults = []
        for item in db.view('searchdoc/searchview'):
            SearchResults.append(item)
        # print(SearchResults)
        resp.body = json.dumps(SearchResults, ensure_ascii=False)
        resp.status = falcon.HTTP_200


############################################################
###############################WILFRED WILFRED WILFRED WILFRED WILFRED WILFRED WILFRED WILFRED ##############################


class UpdateAll(object):
    def on_post(self, req, resp):
        import datetime
        date = datetime.datetime.now()
        date_now=[date.year,date.month,date.day,date.hour,date.minute,date.second,date.microsecond]
        data = req.media
        document=db.get(data["_id"])
        # print document,data
        # db.save(document)
        hist_syno = DeepDiff(document["synonymous"], data["synonymous"], ignore_order=True, report_repetition=True)
        hist_miss = DeepDiff(document["misspell"], data["misspell"], ignore_order=True, report_repetition=True)
        # print hist_syno
        ############### Synonymous
        for item in hist_miss:
            if item == "iterable_item_removed":
                removed_syno=[]
                for item in hist_miss["iterable_item_removed"]:
                    removed_syno.append(hist_miss["iterable_item_removed"][item])
                log={
                    "note":"-misspell:"+json.dumps(removed_syno),
                    "admin":"RemoteStaff",
                    "date":date_now
                }

                document["history"].insert(0,log)
            elif item == "iterable_item_added":
                added_syno=[]
                for item in hist_miss["iterable_item_added"]:
                    added_syno.append(hist_miss["iterable_item_added"][item])
                log={
                    "note":"+misspell:"+json.dumps(added_syno),
                    "admin":"RemoteStaff",
                    "date":date_now
                }
                document["history"].insert(0,log)
        ############### Misspell
        for item in hist_syno:
            if item == "iterable_item_removed":
                removed_syno=[]
                for item in hist_syno["iterable_item_removed"]:
                    removed_syno.append(hist_syno["iterable_item_removed"][item])
                log={
                    "note":"-synonymous:"+json.dumps(removed_syno),
                    "admin":"RemoteStaff",
                    "date":date_now
                }

                document["history"].insert(0,log)
            elif item == "iterable_item_added":
                added_syno=[]
                for item in hist_syno["iterable_item_added"]:
                    added_syno.append(hist_syno["iterable_item_added"][item])
                log={
                    "note":"+synonymous:"+json.dumps(added_syno),
                    "admin":"RemoteStaff",
                    "date":date_now
                }
                document["history"].insert(0,log)
        ############### Display
        if document["display"]!=data["display"]:
            log={
                    "note":"-display:'"+document["display"]+"'",
                    "admin":"RemoteStaff",
                    "date":date_now
                }
            document["history"].insert(0,log)
            log={
                    "note":"+display:'"+data["display"]+"'",
                    "admin":"RemoteStaff",
                    "date":date_now
                }
            document["history"].insert(0,log)

        document.update({'display':data["display"]})
        document.update({'synonymous':data["synonymous"]})
        document.update({'misspell':data["misspell"]})
        db.save(document)

############################################################################################################################
app = falcon.API()

 ############################################################

things = Resource()
catchData = getData()
logSearch = logSearch()
addSearch = addSearch()
getDelete = getDelete()
delSyno = delSyno()
UpdateSyno = UpdateSyno()
UpdateJobTitle = UpdateJobTitle()
delKeywords = delKeywords()
UpdateKeywords = UpdateKeywords()
displaySearch = displaySearch()
addSynoKey = addSynoKey()
AddNewDict = AddNewDict()
 ############################################################

app.add_route('/falcon/AddNewDict', AddNewDict)
app.add_route('/falcon/addSynoKey', addSynoKey)
app.add_route('/falcon/displaySearch', displaySearch)
app.add_route('/falcon/UpdateKeywords', UpdateKeywords)
app.add_route('/falcon/delKeywords', delKeywords)
app.add_route('/falcon/UpdateJobTitle', UpdateJobTitle)
app.add_route('/falcon/UpdateSyno', UpdateSyno)
app.add_route('/falcon/delSyno', delSyno)
app.add_route('/falcon/getDelete', getDelete)
app.add_route('/falcon/addSearch', addSearch)
app.add_route('/falcon/logSearch', logSearch)
app.add_route('/falcon/catchData', catchData)
app.add_route('/falcon/things', things)
app.add_route('/falcon/UpdateAll', UpdateAll())
 ############################################################