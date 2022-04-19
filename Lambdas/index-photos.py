import json
import urllib.parse
import boto3
from datetime import datetime
import requests
from requests_aws4auth import AWS4Auth
import re

#DEMO ADDITION 

def detectLabelsRekognition(bucket, key):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={'S3Object':{
            'Bucket':bucket,
            'Name':key
            }
        },
        MinConfidence=95
        )
    labels = []
    for i in response['Labels']:
        labels.append(i['Name'])
    return labels

def fetchCustomLabels(bucket, key, labels):
    s3 = boto3.client('s3')
    metadata = s3.head_object(Bucket=bucket, Key=key)
    if metadata["Metadata"] == {}:
        return labels 
    else: 
        customlabels = metadata["Metadata"]["customlabels"]
        nospace = customlabels.replace(",", "")
        customlabel_list = [x.strip() for x in nospace.split(' ')]
        labels.extend(customlabel_list)
        return labels
    
def createDocument(bucket, key, labels):
    document = {
            "objectKey":key,
            "bucket":bucket,
            "createdTimestamp": datetime.now().strftime("%y-%m-%d %H:%M:%S"),
            "labels":labels
        }
    return document
    
def indexOpenSearch(document):
    host = 'https://search-photos-lmba365w3ql2icszjbdevd7pdy.us-east-1.es.amazonaws.com'
    index = 'photos'
    url = host + '/' + index + '/_doc'
    service = 'es'
    region = 'us-east-1'
    headers = { "Content-Type": "application/json" }
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    response = requests.post(url, auth=awsauth, json=document, headers=headers)
    return response


def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    rekLabels = detectLabelsRekognition(bucket, key)
    all_labels = fetchCustomLabels(bucket, key, rekLabels)
    document = createDocument(bucket, key, all_labels)    
    response = indexOpenSearch(document)
    
    # data = json.loads(response.content.decode('utf-8'))
    
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
    }
