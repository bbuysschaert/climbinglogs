# Dependencies
import numpy as np
import pandas as pd

from typing import Literal
grades = Literal['french', 'usa', 'v-bouldering']
styles = Literal['route', 'boulder', 'lead', 'toprope']

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

    if len(grades) == 1:
        return grades[0]
    elif len(grades) % 2 == 0:
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

def compute_weeklysummary(df: pd.DataFrame, gradesystem: grades = 'french', style: styles = 'route') -> pd.DataFrame:
    """
    Aggregate the climbing logs per week for high-level metrics.

    The following metrics are computed:
    - max grade topped
    - min grade topped
    - max grade climbed per ascension type (flash, redpoint, repeat)
    - median grade climbed per ascension type (flas, redpoint, repeat)
    """
    assert style in ['route', 'boulder', 'lead', 'toprope'], 'specified climbing style not understood'
    assert gradesystem in ['french', 'usa']
    
    # Determine the grade column
    gradecol = 'grade_{}'.format(gradesystem)
    
    # Subset the data to only account for the specified styles
    if style == 'route':
        data = df[(df['style'] == 'lead') | (df['style'] == 'toprope')]
    else:
        data = df[df['style'] == style]
    
    # Ignore routes that were not topped
    data = data[data['ascension_type'] != 'not topped']
    
    # Add week information, by getting the first monday of that week
    # https://stackoverflow.com/a/35613515/2931774
    data['week'] = data['date'].dt.to_period('W-MON').apply(lambda r: r.start_time)
    
    # Repeat records to account for repeated routes
    data = pd.DataFrame(data.values.repeat(data.sends, axis=0),
                        columns = data.columns
                       )
    
    
    # Reset the grade to categorical data!
    if gradesystem == 'french':
        from .grade import create_ordinalcats_french
        data[gradecol] = data[gradecol].astype(create_ordinalcats_french())
    elif gradesystem == 'usa':
        from .grade import create_ordinalcats_usa
        data[gradecol] = data[gradecol].astype(create_ordinalcats_usa())
    
    
    # Only account for needed information
    data = data.loc[:, ['date', 'week', 'grade', gradecol, 'route', 'style', 'ascension_type']]
    
    # Determine max / min grade per week
    data_weekly = (data
                   .groupby('week', as_index=False)
                   .agg(maxgrade = (gradecol, 'max'),
                        mingrade = (gradecol, 'min')
                       )
                  )
    
    # Determine max and median grade per ascenion type
    temp = (data
            .groupby(['week', 'ascension_type'], as_index=False)
            .agg(maxgrade = (gradecol, 'max'),
                 mediangrade = (gradecol, get_mediangrade)
                )
            .pivot(index='week',
                  columns='ascension_type',
                  values=['maxgrade', 'mediangrade'])
           )
    temp.columns = [f'{ii}_{jj}'for ii, jj in temp.columns]
    
    # Combine the tables
    data_weekly = data_weekly.merge(temp,
                                    on = 'week',
                                    how = 'left' # Should always match, because it uses the same base table
                                   )
    
    return data_weekly