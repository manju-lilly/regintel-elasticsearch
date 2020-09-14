#!/usr/bin/env python3

import json
import boto3
import logging

import datetime

from elasticsearch import Elasticsearch, RequestsHttpConnection

from utils import load_log_config


class RegIntelElasticSearchAPI(object):
    FORMAT = "pdf"

    def __init__(self, *args, **kwargs):
        es_host = kwargs.get("endpoint")
        awsauth = kwargs.get("awsauth")

        if es_host is None:
            raise Exception("ES host is not configured")

        self.es_host = es_host

        self.es = Elasticsearch(
            hosts=[{'host': self.es_host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

        # ES settings
        self.number_of_replicas = 0
        self.number_of_shards = 1

        # logger
        self.logger = load_log_config()

    def create_es_index_template(self):
        template = {
       
            "index_patterns": [
                "reg_intel_*",
                "regint*"
            ],
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "index": {
                    "analysis": {
                        "filter": {
                            "synonym_filter": {
                                "type": "synonym",
                                "synonyms": [
                                    "negative, negation, negated",
                                    "oncology, cancer, tumor",
                                    "study, studies, study:there, trial, trials",
                                    "drug, drugs",
                                    "approve, approved, approval",
                                    "single arm, single-arm",
                                    "priority review, priority reviews",
                                    "prime designated => priority medicines",
                                    "review, reviews"
                                ]
                            }
                        },
                        "analyzer": {
                            "synonym_analyzer": {
                                "filter": [
                                    "synonym_filter"
                                ],
                                "type": "custom",
                                "tokenizer": "standard"
                            }
                        }
                    }
                }
            },
            "mappings": {
                "_source": {
                    "enabled": false
                },
                "properties": {
                    "id": {
                        "type": "text"
                    },
                    "format": {
                        "type": "text"
                    },
                    "name": {
                        "type": "text"
                    },
                    "title": {
                        "type": "text"
                    },
                    "drug_name": {
                        "type": "text"
                    },
                    "s3_raw_url": {
                        "type": "text"
                    },
                    "body_text": {
                        "type": "text",
                        "term_vector": "with_positions_offsets",
                        "analyzer": "synonym_analyzer"
                    },
                    "meta_nested": {
                        "type": "nested"
                    },
                    "source_url": {
                        "type": "text"
                    },
                    "date _created": {
                        "type": "date"
                    },
                    "date_updated": {
                        "type": "date"
                    }
                }
            }
        }

        try:
            url = f"{self.es_host}/_template/reg_intel_template"
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "PUT", url, headers=headers, data=template)
            logging.info(response.text.encode('utf8'))
        except Exception as ex:
            logging.error("error occurred while inserting index template")

    def create_index(self, index_name):
        """Create elastic search indexes utilizing
        """

        index_settings = {
            
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "analysis": {
                        "filter": {
                            "autocomplete_filter": {
                                "type": "edge_ngram",
                                "min_gram": 1,
                                "max_gram": 20
                            },
                            "synonym_filter": {
                                "type": "synonym",
                                "synonyms": [
                                    "negative, negation, negated",
                                    "oncology, cancer, tumor",
                                    "study, studies, study:there, trial, trials",
                                    "drug, drugs",
                                    "approve, approved, approval",
                                    "single arm, single-arm",
                                    "priority review, priority reviews",
                                    "prime designated => priority medicines",
                                    "review, reviews"
                                ]
                            }
                        },
                        "analyzer": {
                            "autocomplete": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": [
                                    "lowercase",
                                    "autocomplete_filter"
                                ]
                            },
                            "synonym_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": [
                                    "synonym_filter"
                                ]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "id": {
                            "type": "text"
                        },
                        "format": {
                            "type": "keyword",
                            "index": "true"
                        },
                        "name": {
                            "type": "keyword",
                            "index": "true"
                        },
                        "title": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "drug_name": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "active_substance": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "strength": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "data_source": {
                            "type": "keyword",
                            "index": "true"
                        },
                        "license_holder": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "year_of_authorization": {
                            "type": "date"
                        },
                        "route_of_administration": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "submission_date_for_initial_approval": {
                            "type": "date"
                        },
                        "approval_type": {
                            "type": "keyword",
                            "index": "true"
                        },
                        "document_type": {
                            "type": "keyword",
                            "index": "true"
                        },
                        "approval_status": {
                            "type": "keyword",
                            "index": "true"
                        },
                        "body_text": {
                            "type": "text",
                            "term_vector": "with_positions_offsets",
                            "analyzer": "synonym_analyzer"
                        },
                        "body_nested": {
                            "type": "nested"
                        },
                        "meta_nested": {
                            "type": "nested"
                        },
                        "source_url": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "date_created": {
                            "type": "date"
                        },
                        "date_updated": {
                            "type": "date"
                        },
                        "attachment.content": {
                            "type": "text",
                            "analyzer": "english",
                            "term_vector": "with_positions_offsets",
                            "store": "true"
                        }
                    }
                }
            }
        

        # create index
        try:
            response = self.es.indices.create(index=index_name, ignore=[
                                          400], body=index_settings)

        except:
            self.logger.fatal("Error creating index %s", index_name)
            raise

    def add_document(self, index_name, document, metadata, format="default"):
        ## check if index exists
        if self.es.indices.exists(index_name):
            self.logger.info('Index %s already exists, skipping creation.', index_name)
        else:
            self.create_index(index_name)

        try:
            # Creating payload for ingesting into Elasticsearch
            time = self.get_current_timestamp()
            doc = {
                'id': document['id'], 
                'name': document['name'],
                'title': document['title'],
                'drug_name': document['drug_name'],
                "source_url": document["source_url"],
                "format": document["format"] if "format" in document else self.FORMAT,
                "date_created": time,
                "date_updated":metadata["last_updated"],
                "active_substance": metadata['active_substance'],
                "strength": metadata["strength"],
                "data_source": metadata["data_source"],
                "year_of_authorization":metadata["year_of_authorization"],
                "license_holder": metadata["license_holder"],
                "route_of_administration": metadata["route_of_administration"],
                "submission_date_for_initial_approval": metadata["submission_date_for_initial_approval"],
                "approval_status": metadata["approval_type"],
                "document_type": metadata["document_type"],
                "meta_nested": metadata,
                "body_text": document["body_text"],
                "body_nested":document["body_nested"]

            }
            # add to index
            self.es.index(index=index_name, doc_type="doc", id=document['id'],body = doc)
        except:
            self.logger.error("Failed to add document to index: %s", index_name)
            raise

    # search
    def search_with_template(self, search_template):
        pass

    def search(self, search_query):
        pass

    # Helpers
    def get_current_timestamp(self):
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
