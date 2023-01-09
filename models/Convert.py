import pandas as pd

class ConvertFiles():

    def convert_excel(self, dataframe_list: list, filename: str):
        index = 0

        print(self.save_mode)

        if self.save_mode.lower() == 'many files':
            print("chosen: ", self.save_mode)        
            for each in dataframe_list:
                each.to_excel(f'{self.file_path}_{index+1}.{self.output_type}',index=False)
                index = index + 1 

        elif self.save_mode.lower() == 'one page':
            print("chosen: ", self.save_mode)
            print(filename)
            self.dataframe.to_excel(filename,index=False)
            
        elif self.save_mode.lower() == 'many pages':
            print("chosen: ", self.save_mode)
            with pd.ExcelWriter(filename) as writer:  
                for each in dataframe_list:
                    each.to_excel(writer, sheet_name=f'sheet_{index+1}',index=False)
                    index = index + 1   
                
    def convert_csv(self, dataframe_list: list, filename: str):
        index = 0
        if self.save_mode.lower() == 'many files':
            print("chosen: ", self.save_mode)        
            for each in dataframe_list:
                each.to_csv(f'{self.file_path}_{index+1}.{self.output_type}',index=False)
                index = index + 1 

        elif self.save_mode.lower() == 'one page':
            print("chosen: ", self.save_mode)
            print(filename)
            self.dataframe.to_csv(filename,index=False)
            
        elif self.save_mode.lower() == 'many pages':
            raise Exception("sorry, can't convert csv to many pages")
