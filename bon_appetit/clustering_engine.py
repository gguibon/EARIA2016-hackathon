#!/usr/bin/python

from websocket import create_connection
import json
import toolbox
# import sklearn 
from sklearn.cluster import KMeans
# import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from operator import itemgetter
import os.path

# initialisation of the toolbox for easy common usages
tb = toolbox.Commons("tb1")

server = "www.earia2016.org"
port = 9002
ws = create_connection("ws://%s:%d/" % (server, port))
team_name = "bonappetit"
# the password for the server, if needed
team_pwd = "PUT YOUR PWD HERE IF NEEDED"
# number of docs to download in order to do the clusterisation
n_docs2download = 15
# number of docs to show at the end
n_docs2show = 10
# number of words to get per docs in order to do the clusterisation
n_words_per_docs = 50


class clusteringService:
    """made for EARIA2016 hackthon by the team 'bon appetit' """

    name = ""
    def __init__(self, name):
        self.name = name

    def start(self, query):
        """access filter for the two methods above. Currently not used."""
        if len(query.split(' ')) > 3 :
            return self.getDocuments(query)
        else :
            return self.compute_word_clusters(query)
    
    def compute_word_clusters(self, query):
        """clusterisation using k-means. Then return the most representative words for each clusters and the query."""
        # Evaluate run
        directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        with open(os.path.join(directory, "run.txt")) as f:
            run = f.read()
            ws.send(json.dumps({ "command": "submit", "name": "bonappetit", "password": "ba978.!",
                                 "run": run }))
            print(json.loads(ws.recv()))
        
        # Query
        queries = [{ "text": "#combine("+ query +")", "number": "1" }]
        command = {"command": "query", "query": queries, "count": n_docs2download}
        ws.send(json.dumps(command))
        result = json.loads(ws.recv())
        
        cN = 0
    
        listdocbow = []
        for c in result['1'] :
            idDoc = c['id']
            cN = cN+1
            ws.send(json.dumps({ "command": "document", "type": "bow", "docid": idDoc}))
            docbow = json.loads(ws.recv())
    
            maprank = {}
            for d in docbow['occurrences']:
                if d[0] in maprank :
                    maprank[d[0]].append(d[1])
                else :
                    maprank[d[0]] = [d[1]]
            sorted_x = sorted(maprank.items(), key=itemgetter(0), reverse=True)
            listtmp = [x[1] for x in sorted_x]
            listfinal = []
            for el in listtmp :
                listfinal.append( ' '.join(el) )
            listdocbow.append( ' '.join(listfinal) )
            print cN, " / ", 100
        
        
        print 'listdocbow : ', listdocbow
        
        print 'count vectorizer'
        cv = CountVectorizer( stop_words="english")
        print 'cv intialized\n starting fit'
        tf = cv.fit_transform(listdocbow[1:n_words_per_docs])
        
        
        ws.close()
        
        
        kmeans = KMeans(n_clusters=5, random_state=0).fit(tf)
        print 'labels : ', kmeans.labels_
        print 'clusters : ', kmeans.cluster_centers_
        
        order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = cv.get_feature_names()
        
        chosen_words = []
        w_in_query = queries[0]['text'].replace('#combine(','').replace(')','').split(' ')
        print 'w_in_query = ', w_in_query
        for i in range(5):
            print "Cluster: ", i
            numberMax = 0
            for ind in order_centroids[i, :10]:
                if numberMax == 0:
                    if terms[ind] in ['oov']:
                        continue
                    if terms[ind] in w_in_query:
                        continue
                    if (' '.join(w_in_query) + ' ' + terms[ind]) in chosen_words:
                        continue
                    chosen_words.append(' '.join(w_in_query) + ' ' + terms[ind])
                    numberMax = 1
                print terms[ind]
        w_in_query += chosen_words
    
        print chosen_words
        return chosen_words
    
    
    def getDocuments(self, query):
        """method to launch the clustering based on the query. return a list of json objects with doc id and list of words with the most occurrences"""   
        # Evaluate run
        directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        with open(os.path.join(directory, "run.txt")) as f:
            run = f.read()
            ws.send(json.dumps({ "command": "submit", "name": team_name, "password": team_pwd,
                                 "run": run }))
            print(json.loads(ws.recv()))
        
        
        # Query
        queries = [{ "text": "#combine("+ query +")", "number": "1" }]
        command = {"command": "query", "query": queries, "count": n_docs2show}
        ws.send(json.dumps(command))
        result = json.loads(ws.recv())
        
        cN = 0
    
        listdocbow = []
    
        doc2return = []
        for c in result['1'] :
            idDoc = c['id']
            cN = cN+1
            ws.send(json.dumps({ "command": "document", "type": "bow", "docid": idDoc}))
            docbow = json.loads(ws.recv())
    
            maprank = {}
            for d in docbow['occurrences']:
                if d[0] in maprank :
                    maprank[d[0]].append(d[1])
                else :
                    maprank[d[0]] = [d[1]]
    
            sorted_x = sorted(maprank.items(), key=itemgetter(0), reverse=True)
    
            listtmp = [x[1] for x in sorted_x]
            listfinal = []
            for el in listtmp :
    
                listfinal.append( ' '.join(el) )
            listdocbow.append( ' '.join(listfinal) )
            print cN, " / ", 100
            
            #creation map json object to send
            objectDoc = {'idDoc':idDoc, 'words': sorted_x[1:10]}
            doc2return.append(objectDoc)
        
        return doc2return 
    
    
# kept here in order to test the engine directly
# start("animal nature")