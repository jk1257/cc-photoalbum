import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
import logging

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def sendtoLex(query):
    lex = boto3.client('lexv2-runtime')
    response = lex.recognize_text(
        botId='JAMC4UCTTX',
        botAliasId='TMIOHYFSNW',
        localeId='en_US',
        sessionId='22',
        text=query)
    return response
    
    
def keywordsForSearch(lex_response):
    try:
        search_list = []
        hits = lex_response["interpretations"][0]["intent"]["slots"]["SeachWords"]["values"]
        for i in hits: 
            if i["value"]["resolvedValues"] == []:
                return search_list
            else:
                keyword = i["value"]["resolvedValues"][0]
                search_list.append(keyword)
        return search_list
    except:
        search_list = []
        return search_list
    
def searchOpenSearch(search_list):
    photos = []
    for i in search_list:
        host = 'https://search-photos-lmba365w3ql2icszjbdevd7pdy.us-east-1.es.amazonaws.com'
        index = 'photos'
        url = host + '/' + index + '/_search?q=' + i
        service = 'es'
        region = 'us-east-1'
        headers = { "Content-Type": "application/json" }
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
        response = requests.get(url, auth=awsauth, headers=headers)
        data = json.loads(response.content.decode('utf-8'))
        for i in data["hits"]["hits"]:
            bucket = i["_source"]["bucket"]
            key = i["_source"]["objectKey"]
            photoURL = "https://{0}.s3.amazonaws.com/{1}".format(bucket,key)
            photos.append(photoURL)
    return photos
        
        
def lambda_handler(event, context):  
    temp = event['params']['querystring']
    query = temp["q"]
    
    lex_response = sendtoLex(query)
    search_list = keywordsForSearch(lex_response)
    photos = searchOpenSearch(search_list)
    
    return photos
 