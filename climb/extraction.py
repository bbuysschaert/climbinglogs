# Dependencies
import pandas as pd
import datetime as dt
from pandas.api.types import CategoricalDtype
import re

from typing import List, Optional, Literal

def create_ordinalcats_ascensions() -> CategoricalDtype:
    """
     Create a Pandas CategoricalDtype that defines the ordinal categeories of the climbing ascension types
    """
    ascensions = ['flash', 'redpoint', 'repeat', 'topped', 'not topped']
    return CategoricalDtype(categories=ascensions, ordered=True)

def clean_columnname(col: str, format :Literal['snake'] = 'snake') -> str:
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

def extract_climbinglogs(path: str, format: Literal['excel'] = 'excel', cols_ffill: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Extract the climbing logs and retuns them as a Pandas DataFrame with the necessary data preparation.  This results in a highly specialised function.
    """
    from .grades import convert_grade
    from .grades import create_ordinalcats_french, create_ordinalcats_usa

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

    # Fill mising values
    for cc in ['blocks', 'falls', 'sends']:
            df[cc] = pd.to_numeric(df[cc], downcast='integer')

    # Ensure certain columns are always in lower-case
    for cc in ['ascension_type', 'style', 'grade']:
        df[cc] = [val.lower() for val in df[cc]]

    # Convert the grades to known systems
    df['grade_usa'] = df['grade'].apply(convert_grade, desired='usa')
    df['grade_french'] = df['grade'].apply(convert_grade, desired='french')

    # Define certain attributes as categorical
    df['grade_usa'] = df['grade_usa'].astype(create_ordinalcats_usa())
    df['grade_french'] = df['grade_french'].astype(create_ordinalcats_french())
    df['ascension_type'] = df['ascension_type'].astype(create_ordinalcats_ascensions())
    
    return df

def extract_sessionlogs(path: str, format: Literal['excel'] = 'excel') -> pd.DataFrame:
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