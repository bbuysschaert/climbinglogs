# Dependencies
import numpy as np
import pandas as pd

from typing import Literal

def create_pyramid_basic(df: pd.DataFrame,
                        aggtype: Literal['sum', 'count'] = 'sum',
                        gradesystem: Literal['french', 'usa'] = 'french') -> pd.DataFrame:
    """
    Aggregate the climbing logs to create a route pyramid per grade
    """
    assert aggtype in ['count', 'sum']
    assert gradesystem in ['french', 'usa']
    
    # Determine the grade column
    gradecol = 'grade_{}'.format(gradesystem)
    
    # Aggregate to the basic pyramid
    pyrm = (df
            .groupby(gradecol)
            .agg(sends=('sends', aggtype),
                )
           )
    return pyrm.reset_index()

def create_pyramid(df: pd.DataFrame,
                   aggtype: Literal['sum', 'count'] = 'sum',
                   gradesystem: Literal['french', 'usa'] = 'french') -> pd.DataFrame:
    """
    Aggregate the climbing logs to create a route pyramid per grade and ascension type
    """
    assert aggtype in ['count', 'sum']
    assert gradesystem in ['french', 'usa']
    
    # Determine the grade column
    gradecol = 'grade_{}'.format(gradesystem)
    
    # Aggregate to the actual pyramid
    pyrm = (df
            .groupby([gradecol, 'ascension_type'])
            .agg(sends=('sends', aggtype),
                )
           )
    
    # Additional cumulative sum, needed to display the pyramid
    temp = pyrm.groupby(level=0).cumsum()
    temp = temp.rename(columns={'sends': 'sends_cumsum'})
    
    # Join the two dataframes
    pyrm = pyrm.reset_index()
    temp = temp.reset_index()
    
    return pyrm.merge(temp, on=[gradecol, 'ascension_type'], how='left')  