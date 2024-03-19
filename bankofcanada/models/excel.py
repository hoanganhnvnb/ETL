import pandas as pd

from .base import BaseModelExtract, BaseModelLoad

class ExtractModelExcel(BaseModelExtract):
    def __init__(self):
        pass

    def __str__(self):
        return 'API ' + super().__str__()

    def request_data(self, config):
        result = []
        if not isinstance(config, dict):
            print("Not extract data from Excel file")
            return result
        path = config.get('path')
        sheet = config.get('sheet')
        list_sheet = None
        if sheet:
            list_sheet = [sheet_name.strip() for sheet_name in sheet.split(",")]
        dfs = pd.read_excel(path, sheet_name=list_sheet)
        if isinstance(dfs, dict) and list_sheet:
            for s in list_sheet:
                data = dfs[s]
                result += self.convert_dataframe_to_list(data)

        elif isinstance(dfs, pd.DataFrame):
            result = self.convert_dataframe_to_list(dfs)
        return result

    def convert_dataframe_to_list(self, dataframe:pd.DataFrame):
        result = []
        if dataframe.empty:
            return result
        for index, row in dataframe.iterrows():
            data_insert = {}
            for key in dataframe.keys():
                if key:
                    data_insert[str(key)] = row[str(key)]
            result.append(data_insert)
        return result

class LoadModelExcel(BaseModelLoad):
    def __init__(self):
        pass

    def __str__(self):
        return 'API ' + super().__str__()
