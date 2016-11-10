#!/usr/bin/python

import web
import json
from imageRequest import imageRequest
import random
import clustering_engine

# URL to expose
urls = ('/', 'clusteringService')
ce = clustering_engine("ce")

# Class to expose
class clusteringService:
    """made for EARIA2016 hackthon by the team 'bon appetit' """

    
    
    # Constructor
    def __init__(self):
        self.defaultSubjects = ["jaguar","football","astronomy","president","python","cinema","ecology","Europe","Mars","Music","Apple","Computer","Java","France","Orange"]
        self.defaultDocuments = list()
        self.defaultDocuments.append({"title":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce massa.","link":"http://lpsum/?docID=1234","abstract":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse nec quam mollis, laoreet dui et, pretium tortor. Aliquam tristique rutrum euismod. Ut bibendum diam ultrices malesuada varius. Fusce efficitur eget ipsum ac luctus. Aenean et justo ac augue vestibulum condimentum at sit amet ex. In malesuada nec augue vel pulvinar. Suspendisse hendrerit mi magna, feugiat fringilla sem lobortis nec. Duis consectetur est maximus finibus congue. In ac sagittis turpis. Cras porttitor sed ipsum eu condimentum. Praesent sit amet commodo lacus, nec bibendum nisl. Proin sodales tempus purus, sit amet iaculis tellus sagittis sed."})
        self.defaultDocuments.append({"title":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent tincidunt.","link":"http://lpsum/?docID=4564","abstract":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse nec quam mollis, laoreet dui et, pretium tortor. Aliquam tristique rutrum euismod. Ut bibendum diam ultrices malesuada varius. Fusce efficitur eget ipsum ac luctus. Aenean et justo ac augue vestibulum condimentum at sit amet ex. In malesuada nec augue vel pulvinar. Suspendisse hendrerit mi magna, feugiat fringilla sem lobortis nec. Duis consectetur est maximus finibus congue. In ac sagittis turpis. Cras porttitor sed ipsum eu condimentum. Praesent sit amet commodo lacus, nec bibendum nisl. Proin sodales tempus purus, sit amet iaculis tellus sagittis sed."})
        self.defaultDocuments.append({"title":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consequat.","link":"http://lpsum/?docID=6553","abstract":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse nec quam mollis, laoreet dui et, pretium tortor. Aliquam tristique rutrum euismod. Ut bibendum diam ultrices malesuada varius. Fusce efficitur eget ipsum ac luctus. Aenean et justo ac augue vestibulum condimentum at sit amet ex. In malesuada nec augue vel pulvinar. Suspendisse hendrerit mi magna, feugiat fringilla sem lobortis nec. Duis consectetur est maximus finibus congue. In ac sagittis turpis. Cras porttitor sed ipsum eu condimentum. Praesent sit amet commodo lacus, nec bibendum nisl. Proin sodales tempus purus, sit amet iaculis tellus sagittis sed."})
        self.defaultDocuments.append({"title":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dictum.","link":"http://lpsum/?docID=23456","abstract":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse nec quam mollis, laoreet dui et, pretium tortor. Aliquam tristique rutrum euismod. Ut bibendum diam ultrices malesuada varius. Fusce efficitur eget ipsum ac luctus. Aenean et justo ac augue vestibulum condimentum at sit amet ex. In malesuada nec augue vel pulvinar. Suspendisse hendrerit mi magna, feugiat fringilla sem lobortis nec. Duis consectetur est maximus finibus congue. In ac sagittis turpis. Cras porttitor sed ipsum eu condimentum. Praesent sit amet commodo lacus, nec bibendum nisl. Proin sodales tempus purus, sit amet iaculis tellus sagittis sed."})
        self.defaultDocuments.append({"title":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut lacinia.","link":"http://lpsum/?docID=23245","abstract":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse nec quam mollis, laoreet dui et, pretium tortor. Aliquam tristique rutrum euismod. Ut bibendum diam ultrices malesuada varius. Fusce efficitur eget ipsum ac luctus. Aenean et justo ac augue vestibulum condimentum at sit amet ex. In malesuada nec augue vel pulvinar. Suspendisse hendrerit mi magna, feugiat fringilla sem lobortis nec. Duis consectetur est maximus finibus congue. In ac sagittis turpis. Cras porttitor sed ipsum eu condimentum. Praesent sit amet commodo lacus, nec bibendum nisl. Proin sodales tempus purus, sit amet iaculis tellus sagittis sed."})

    def getClusters(self, query):
        return []
    #end getClusters

    # Get random subjects and images
    def getRandomSubject(self):
        clusters = list()
        image_request = imageRequest()
        subjects = random.sample(self.defaultSubjects,3)
        for subject in subjects:
            img_url = image_request.getImage(subject)
            clusters.append({"words":subject,"image":img_url})
        return clusters
    #end getRandomSubject

    # Get clusters subjects
    def getSubjects(self, query):
        clusters = list()
        image_request = imageRequest()
        subjects = ce.start(query)

        for subject in subjects:
            img_url = image_request.getImage(subject)
            clusters.append({"words":subject,"image":img_url})
        return clusters
    # end getSubjects
    
    # GET request
    def GET(self):

        # Header
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        # Service parameter
        query_params = web.input(query="")

        # Standard header
        data = {}
        data['status'] = "ok"

        # Query
        data['query'] = query_params.query;

        if query_params.query == "documents":
            data['count'] = len(self.defaultDocuments)
            data['documents'] = self.defaultDocuments
        else:
            # Image
            if query_params.query != "":
                if(len(query_params.query.split(' ')) > 3):
                    docs = ce.getDocuments(query_params.query)
                    data['documents'] = docs
                    data['count'] = len(docs)
                else :
                    clusters = self.getSubjects(query_params.query)
                    data['clusters'] = clusters
                    data['count'] = len(clusters)

            # Empty query, we get a list of random subject
            if query_params.query == "":
                subjects = self.getRandomSubject()
                data['count'] = len(subjects)
                data['clusters'] = self.getRandomSubject()

        # Return JSON
        return json.dumps(data)
    #end GET

#end clusteringService

# Main
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()