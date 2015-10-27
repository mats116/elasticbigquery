# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
from googleapiclient.errors import Error, HttpError
from oauth2client.client import GoogleCredentials
import uuid

def generate_insert_body(row):
    body = {
        u"ignoreUnknownValues": False,
        u"insertId": unicode(uuid.uuid4()),
        u"rows": [{u"json": row}]
    }
    return body


class BigQuery():

    def __init__(self, project_id):
        self.credentials = GoogleCredentials.get_application_default()
        self.bigquery = build("bigquery", "v2", credentials=self.credentials)
        self.project_id = project_id

    def stream_row(self, dataset_id, table_id, body, num_retries=5):
        req = self.bigquery.tabledata().insertAll(projectId=self.project_id, datasetId=dataset_id, tableId=table_id, body=body)
        res = req.execute(num_retries=num_retries)
        return res

    def create_dataset(self, dataset_id):
        body = {
            u"datasetReference": {
                u"projectId": self.project_id,
                u"datasetId": dataset_id
            }
        }
        req = self.bigquery.datasets().insert(projectId=self.project_id, body=body)
        res = req.execute()
        return res

    def create_table(self, dataset_id, table_id, schema):
        body = {
            u"tableReference": {
                u"projectId": self.project_id,
                u"datasetId": dataset_id,
                u"tableId": table_id
            },
            u"schema": {
                u"fields": schema
            }
        }
        req = self.bigquery.tables().insert(projectId=self.project_id, datasetId=dataset_id, body=body)
        res = req.execute()
        return res

    def update_table(self, dataset_id, table_id, schema):
        body = {
            u"tableReference": {
                u"projectId": self.project_id,
                u"datasetId": dataset_id,
                u"tableId": table_id
            },
            u"schema": {
                u"fields": schema
            }
        }
        req = self.bigquery.tables().update(projectId=self.project_id, datasetId=dataset_id, tableId=table_id, body=body)
        res = req.execute()
        return res
