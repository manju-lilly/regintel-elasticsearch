import json
import boto3
import logging
import requests
import datetime
from datetime import datetime
import json
import os



from utils import load_osenv, load_log_config
from regintel_elastic_search_api import RegIntelElasticSearchAPI


# Initialize logging
logger = load_log_config()

s3 = boto3.client('s3')

es_endpoint = os.environ['ES_HOST']


def lambda_handler(event, context):
    

    logger.info("--------------- PROCESSING NEW EVENT ---------------")

    ## if this is a test
    is_test = True if 'test' in event['metadata'] else False

    try:
        logger.info(
            "Extracting data_source, s3 file path information from the event")
        type_of_data = event['detail']['metadata'][0]['data_source']
        enrich_in_file_path = event['detail']['metadata'][0]['enrich_in_filename']
        enrich_in_file_s3_bucket_name = enrich_in_file_path.split('/')[2]
        enrich_in_file_s3_objectKey = enrich_in_file_path.split('/', 3)[3]

        logger.info("Successfully extracted data_source, s3 file path from the event")
        logger.info("S3 Path: " + enrich_in_file_path)

        ## Getting file extension of the enrich_in file
        enrich_in_filename = enrich_in_file_path.split('/')[-1].split('.')[-1]
        enrich_in_file_extension = enrich_in_filename.split(".")[-1]

        ## Getting metadata from event
        metadata = event['detail']['metadata'][0]
        
        ## Calling s3 download object to get enrich_in file content
        if not is_test:
            enrich_in_file_response = s3.get_object(
                Bucket=enrich_in_file_s3_bucket_name, Key=enrich_in_file_s3_objectKey)
            enrich_in_file_content = enrich_in_file_response['Body'].read()
        else:
            enrich_in_file_content = open()


        try:
            ## Assigning the content of enrich_in_file_content with
            ## respective key depending upon the extension type of the enrich_in file
            if (enrich_in_file_extension == 'txt'):
                enrich_in_txt = str(enrich_in_file_content, 'utf-8')
                enrich_in_json = []

            elif (enrich_in_file_extension == 'json'):
                enrich_in_txt = ""
                enrich_in_json = enrich_in_file_content.decode('utf-8')
                #enrich_in_json = json.dumps(enrich_in_json)
                enrich_in_json = json.loads(enrich_in_json)
                logger.info(enrich_in_json)

            else:
                logger.error(
                    "Unidentified file extension found when trying to get data")
                logger.error("File Name: "+ text_file_name)

            logger.info("Processing data completed")

        except Exception as e:
            logger.error('Exception occured while getting data '+str(e))

        index_name = 'reg_intel_'+type_of_data.lower()+'_' + \
            str(datetime.now().strftime('%Y_%m')) if 'index_name' not in event['metadata'][0] else event['metadata'][0]['index_name']
        
        id = event['id']

        ## Creating payload for ingesting into Elasticsearch
        regintel_es_api = RegIntelElasticSearchAPI(endpoint=es_endpoint)
        response = regintel_es_api.add_document(index_name, {
            "id": id, "name": metadata["filename"], "title": metadata["filename"],
            "drug_name": metadata["drug_name"],
             "source_url": metadata["source_url"],
             "body_text": enrich_in_txt,
             "body_nested": enrich_in_json
        }, metadata)

        logger.info("logging: {}".format(json.dumps(response, indent=2)))


    except Exception as e:
        logger.error(e)
