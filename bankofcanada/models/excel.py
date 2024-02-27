import pandas as pd

from base import BaseModelExtract, BaseModelLoad

class ExtractModelExcel(BaseModelExtract):
    def __init__(self):
        pass

    def __str__(self):
        return 'API ' + super().__str__()

    def request_data(self, config):
        if not isinstance(config, dict):
            print("Not extract data from Excel file")
            return None
        path = config.get('path')
        sheet = config.get('sheet')
        list_sheet = None
        if not sheet:
            list_sheet = [sheet_name.strip() for sheet_name in sheet.split(",")]
        data = []
        return data

class LoadModelExcel(BaseModelLoad):
    def __init__(self):
        pass

    def __str__(self):
        return 'API ' + super().__str__()
