from .base import BaseModelExtract, BaseModelLoad

import mysql.connector

class ExtractModelMysql(BaseModelExtract):
    def __init__(self):
        pass

class LoadModelMysql(BaseModelLoad):
    def __init__(self):
        pass

    def post_data(self, config:dict, data:list):
        pass

    def connect_to_database(self, host, user, password):
        pass