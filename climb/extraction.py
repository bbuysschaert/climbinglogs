import pandas as pd
import datetime as dt
import re

from typing import List, Union

def clean_columnname(col: str, format='snake') -> str:
    """
    Clean the column name to the specified format.  Returns a string with the clean column name 
    """
    # Exclude not allowed characters
    col = col.replace('/', '')

    # Perform formatting
    if format == 'snake':
        col = col.lower()
        col = col.replace(' ', '_')
    else:
        raise NotImplementedError('No other column cleaning format supported')
    
    # Final bookkeeping of whitespaces
    col = re.sub(' +', ' ', col)
    col = col.strip()
    return col

def extract_climbinglogs(path: str, format: str ='excel', cols_ffill: Union[List[str], None] = None) -> pd.DataFrame:
    """
    Extract the climbing logs and retuns them as a Pandas DataFrame
    """
    # Perform extraction
    if format == 'excel':
        df = pd.read_excel(path, sheet_name='logs')

    else:
        raise NotImplementedError('Log format is not yet supported')
    
    # Bookkeeping of column names
    df = df.rename(columns={cc:clean_columnname(cc) for cc in df.columns})

    # Perform forward filling for specific columns
    if cols_ffill:
        df.loc[:, cols_ffill] = df.loc[:, cols_ffill].ffill()
    
    return df

def extract_sessionlogs(path: str, format: str ='excel') -> pd.DataFrame:
    """
    Extract the session logs and retuns them as a Pandas DataFrame
    """
    # Perform extraction
    if format == 'excel':
        df = pd.read_excel(path, sheet_name='sessions')

    else:
        raise NotImplementedError('Log format is not yet supported')
    
    # Bookkeeping of column names
    df = df.rename(columns={cc:clean_columnname(cc) for cc in df.columns})
    
    return df

if __name__ == "__main__":
    pathin = './Data/XXX.xlsx'