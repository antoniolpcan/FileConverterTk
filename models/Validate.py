from datetime import datetime

class Validate:

    def check_output_name(self, output_name: str):
        dt = datetime.now()
        if len(output_name) > 0:
            return output_name + f"_{dt.day}_{dt.month}_{dt.year}_{dt.microsecond}"
        else:
            raise Exception(f"Invalid output name: {output_name}")
    
    def check_save_mode(self, save_mode: str) -> str:

        if save_mode.lower() in ['one page', 'uma página']:
            return 'one page'
        
        elif save_mode.lower() in ['many pages', 'várias páginas']:
            return 'many pages'
        
        elif save_mode.lower() in ['many files','vários arquivos']:
            return 'many files'
        
        else: 
            raise Exception(f'Invalid save mode: {save_mode}.')
    
    def check_output_type(self, output_type: str) -> str:

        if output_type.lower() == 'xlsx':
            return output_type
        
        elif output_type.lower() == 'csv':
            return output_type
        
        else: 
            raise Exception(f'Invalid output type: {output_type}.')

    def check_compact(self, output_compact: str) -> str:

        if output_compact.lower() in ['zip']:
            return output_compact
        
        else: 
            raise Exception(f'Invalid compact type: {output_compact}.')

    def check_rows(self, rows: str) -> int:

        if type(rows) == str:

            if '.' in rows or ',' in rows:
                raise Exception(f"rows '{rows}' can't be a float value")

            if not rows.isdigit():
                print('row number is not digit')
                if rows.lower() in ["all", "*"]:
                    return 0
                else:
                    raise Exception(f'Invalid rows per sheet: {rows}.')
            else:
                print('row number is string digit')
                return int(rows)

        elif type(rows) == int:
            print('row number: ', rows)
            return rows
        
        else:
            raise Exception(f'Invalid rows: {rows}.')
            
