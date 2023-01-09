from .Validate import Validate
from .Convert import ConvertFiles
from typing import Union
import pandas as pd
import shutil
import os

class FileConv(Validate, ConvertFiles):
    
    def __init__(self,  file: bytes, output_type: str, type_compact: str, output_name: str, save_mode: str, rows: Union[str, int]):
        self.file = file
        self.file_binary = file
        self.content_type = file.name.split('.')[-1]
        self.output_type = self.check_output_type(output_type)
        self.type_compact = self.check_compact(type_compact)
        self.output_name = self.check_output_name(output_name)
        self.save_mode = self.check_save_mode(save_mode)
        self.rows = self.check_rows(rows)
        self.download_path = "./downloads"
        self.download_path_dataframe = f"{self.download_path}/sheets"
        self.zip_path = f"./downloads/{self.type_compact}"
        self.file_path = f"{self.download_path_dataframe}/{self.output_name}"

    def create_dataframe(self) -> pd.DataFrame:
        """
        ### Read file according to the content type.
        
        - if content type equals text/csv, read csv
        - if content type equals "application/vnd.ms-excel" or "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", read excel
        - else, an exception will be raised

        """
        print(f"checking {self.content_type}")
        if self.content_type == "text/csv":
            self.dataframe = pd.read_csv(self.file.name, sep=',', encoding='utf-8')
            if self.dataframe.shape[1]<2:
                print("using separator: ';'")
                self.dataframe = pd.read_csv(self.file.name, sep=';', encoding='utf-8')
            
        elif self.content_type in ["application/vnd.ms-excel", 'xlsx'] or self.content_type in ['csv', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            self.dataframe = pd.read_excel(self.file.name)

        else:
            print(f"Invalid content type: '{self.content_type}'")
            raise Exception(f"Invalid content type: '{self.content_type}'")

    def get_response(self) -> str:
        print("Trying to return file")
        try:
            return f"{self.zip_path}/{self.output_name}.{self.type_compact}"
        except Exception as exc:
            print(exc)
            raise Exception(f"{exc}")

    def divide_rows(self, dataframe: pd.DataFrame, row_num: int):      
        """
        ### Divide dataframe's rows and append to list

        """
        dataframe_list = []
        if row_num != 0:
            print('going to divide dataframe')
            initial_index = 0
            final_index = 0
            len_dataframe = len(dataframe)
            while final_index < len_dataframe:
                
                if initial_index == 0 and final_index == 0:
                    initial_index = final_index
                    final_index = final_index + row_num
                    dataframe_list.append(dataframe[initial_index:final_index])

                else:
                    initial_index = final_index
                    final_index = final_index + row_num
                    dataframe_list.append(dataframe[initial_index:final_index]) 

            return dataframe_list
        else:
            return dataframe_list

    def remove_zip_dir(self):
        """
        ### Delete the directory that contains compacted files.
        """
        if os.path.isdir(self.zip_path):
            try:
                os.rmdir(self.zip_path)
            except:
                for file in os.listdir(self.zip_path):
                    os.remove(os.path.join(self.zip_path, file))
                os.rmdir(self.zip_path)
        else:
            pass

    def generate_dir(self, dir: str):
        """
        create directory to save files
        """
        print(f"creating {dir}")
        if os.path.isdir(dir):
            try:
                os.rmdir(dir)
                os.makedirs(dir)
                print(f"{dir} created.")
            except:
                for file in os.listdir(dir):
                    os.remove(os.path.join(dir, file))
                os.rmdir(dir)
                os.makedirs(dir)
                print(f"{dir} created.")
        else:
            os.makedirs(dir)
            print(f"{dir} created.")

    def compact_file(self): 
        """
        ### Function to compact path with files to return them.
        """
        print(f"going to compact file")
        try:
            print(os.listdir(self.download_path_dataframe))
            shutil.make_archive(f'{self.zip_path}/{self.output_name}', self.type_compact, self.download_path_dataframe)

        except BaseException as e:
            print(e)
            raise Exception(f"Can't compact '{self.output_name}.{self.type_compact}'.")

        for f in os.listdir(self.download_path_dataframe):
            os.remove(os.path.join(self.download_path_dataframe, f))
        os.rmdir(self.download_path_dataframe)
        
    def generate_files(self):
        """
        ## Function to convert dataframes to files

        - Excel(xlsx) -> Many files, one page, many pages
        - CSV 
        """
        dataframe_list = self.divide_rows(self.dataframe, self.rows)
        self.generate_dir(self.download_path_dataframe)
        file = f'{self.file_path}.{self.output_type}'
        
        if self.output_type.lower() == "xlsx":    

            if type(dataframe_list) == list:
                print(file)

                self.convert_excel(dataframe_list, file)
                self.compact_file()
                return file
            else:
                return None

        elif self.output_type.lower() == "csv":
            #self.dataframe.to_csv(file,index=False)

            if type(dataframe_list) == list:
                print(file)

                self.convert_csv(dataframe_list, file)

                self.compact_file()
                return file





