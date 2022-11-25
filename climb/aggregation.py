# Dependencies
import numpy as np
import pandas as pd

from typing import Literal

def get_mediangrade(ds: pd.Series) -> str:
    """
    Determine the median grade of the logged ascents.  Assumes that the pandas.Series if of CategoricalDtype and is ordered (i.e., an ordinal measurement)

    >>> df.groupby('week')['grade_french'].agg(get_mediangrade)
    <some-answer>
    >>> get_median_grade(df['grade_french'])
    '6b+'
    """
    # Explicit median computation
    grades = ds.sort_values().to_list()

    if len(grades) % 2 == 0:
        return grades[int(len(grades) / 2)]
    elif len(grades) % 2 == 1:
        return grades[int((len(grades) + 1) / 2)]
    else:
        return None

def get_maxgrade_flash(df: pd.DataFrame, gradesystem: Literal['french', 'usa'] = 'french') -> str:
    """
    Determine the maximum grade of logged flash ascents.
    """
    # Determine the grade column
    gradecol = 'grade_{}'.format(gradesystem)
    
    temp = df[df['ascension_type'] == 'flash']
    return temp[gradecol].max()

def compute_gradepyramid_basic(df: pd.DataFrame,
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

def compute_gradepyramid(df: pd.DataFrame,
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