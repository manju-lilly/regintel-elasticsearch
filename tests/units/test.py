#!/usr/bin/env python3

import json
import requests

import elasticsearch

config = {
    'host': 'https://search-nlp-es-5wanb4pg34re6bstmpflsjwc3i.us-east-2.es.amazonaws.com'
}

es = elasticsearch.Elasticsearch([config,], timeout=300)
#reg_intel_dev_sp4

