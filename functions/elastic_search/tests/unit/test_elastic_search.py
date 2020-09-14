#!/usr/bin/env python3
# pylint: disable=redefined-outer-name,missing-docstring

import json
import os 
import pytest
import boto3
import imp

from botocore.exceptions import ClientError
from contextlib import contextmanager

from moto import mock_s3, mock_stepfunctions
from regintel_elastic_search_api import RegIntelElasticSearchAPI
from load_elasticsearch import lambda_handler

### Test:
## 1. load delta file
## 2. break .csv into chunks
## 3. load chunk, create step function
## 4. test creating step function

EVENT_FILE = os.path.join(
    os.path.dirname(__file__),
    'events',
    'event.json'
)

ES_HOST = 'https://vpc-rq-es-dev-pc2wpl6zau3okwa43wyvky223i.us-east-2.es.amazonaws.com/'
@pytest.fixture()
def event(event_file=EVENT_FILE):
    """
    Trigger event
    
    """
    with open(event_file) as f:
        return json.load(f)

@contextmanager
def s3_setup(s3_client, event):
    """
    Create s3 bucket

    Args:
        s3_client ([type]): [description]
        event ([type]): [description]
    """
    s3_client.create_bucket(Bucket = event['bucket'])
    yield


def test_elastic_search_api(event):
    os.environ = {
        "ES_HOST": ES_HOST,
        "BUCKET_NAME": "Test"}
    
    regintel_api = RegIntelElasticSearchAPI(
        endpoint=ES_HOST)

    # create index
    regintel_api.create_index("unit_testing")

    assert regintel_api.es.indices!=None

def test_elastic_search_handler(event):
    os.environ = {
        "ES_HOST": ES_HOST,
        "BUCKET_NAME": "Test"}
    response = lambda_handler(event=event)

    
    

    
    
    
    

    
    




