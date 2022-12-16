# Dependencies
import os
import json
import re
from pandas.api.types import CategoricalDtype
import pandas as pd

from typing import List, Literal, Union
grades = Literal['french', 'usa', 'v-bouldering']

# Read in the grade conversion file using the relative path
# See https://stackoverflow.com/a/3718923/2931774
file_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(file_path, 'grades.json')) as ff:
    grades_dict = json.load(ff)

def import_gradestable(gradetable: str = 'grades.csv', sep: Literal[';', ','] = ';') -> pd.DataFrame:
    """Read in the grades table and return it as a dataframe"""

    # Read in the grade conversion file using the relative path
    # See https://stackoverflow.com/a/3718923/2931774
    file_path = os.path.dirname(os.path.realpath(__file__))

    grades = pd.read_csv(os.path.join(file_path, gradetable), sep=sep)
    return grades

def create_grademap(grade_source: grades, grade_dest: grades, agg_method: Literal['min', 'max']='min') -> dict:
    """
    Converts the grades table into a mapping dictionary to translate grade_source into grade_dest.
    Method determines what to do when grade_source matches multiple grade_dest:
    - method='min' -> take the lowest grade_dest
    - method='max' -> take the highest grade_dest

    ASSUMPTION: assumess that grade_source and grade_dest are correctly sorted in the grades table!
    """
    grades = import_gradestable()

    # Extract the information from the grade table
    temp = [(ss, dd) for ss, dd in zip(grades[grade_source], grades[grade_dest])]
    
    # Convert the list of tuples to a dict
    grademap = {}
    for kk, vv in temp:
        if kk not in grademap:
            grademap[kk] = vv
        elif agg_method == 'min':
            pass
        elif agg_method == 'max':
            grademap[kk] = vv
        else:
            raise LookupError('Something went wrong when creating the grademap')

    return grademap

def create_ordinalcats_french() -> CategoricalDtype:
    """
    Create a Pandas CategoricalDtype that defines the ordinal categeories of the climbing grades in the French system
    """
    grades_fr = list(grades_dict['french2usa'].keys())
    grades_fr = sorted(grades_fr)
    return CategoricalDtype(categories=grades_fr, ordered=True)

def create_ordinalcats_usa() -> CategoricalDtype:
    """
    Create a Pandas CategoricalDtype that defines the ordinal categeories of the climbing grades in the USA system
    """
    grades_usa = list(grades_dict['usa2french'].keys())

    # Hack into the list to have leading zeros to allow correct sorting
    grades_usa = [val.split('.') for val in grades_usa]
    grades_usa = ['.'.join([val[0], val[1].zfill(2)]) for val in grades_usa]
    grades_usa = sorted(grades_usa)

    # Hack into the list to remove leading zeros
    grades_usa = [val.split('.') for val in grades_usa]
    grades_usa = ['.'.join([val[0], val[1].lstrip('0')]) for val in grades_usa]

    return CategoricalDtype(categories=grades_usa, ordered=True)

# Deprecated, should not be used
def convert_usa2french(val: str) -> str:
    """
    Convert a climbing grade from the USA scale to French Font scale
    >>> convert_usa2french('5.12b')
    '7b'
    """
    return grades_dict['usa2french'][val]

# Deprecated, should not be used
def convert_french2usa(val: str) -> str:
    """
    Convert a climbing grade from the French Font scale to the USA scale 
    >>> convert_usa2french('7b')
    '5.12b'
    """
    return grades_dict['french2usa'][val]

def get_gradesystem(val: str) -> str:
    """
    Determine the grade system according to specified regular expressions.

    >>> get_gradesystem('7b')
    'french'
    >>> get_gradesystem('5.12b')
    'usa'
    >>> get_gradesystem('test')
    None
    """
    if re.search('^5.\d{1,2}[abcd]{0,1}$', val):
        return 'usa'
    elif re.search('^\d{1}[abc]{0,1}\+{0,1}$', val):
        return 'french'
    else:
        return None

def convert_grade(grade: str, desired: grades = 'french') -> Union[str, None]:
    """
    Convert the climbing grade from one system to another.
    - No conversion will take place when the grade is already in the desired system.
    - In case the grade is in an unknown system, None will be returned
    
    The function should be applied as a pandas.Series.map operation
    """
    # Check whether desired system is known
    assert desired in ['french', 'usa'], 'Desired grade system not known'

    # Get the grade system
    source = get_gradesystem(grade)
    
    # Determine whether it is known and whether different from desired
    if (source != None) & (source != desired):
        return grades_dict['{}2{}'.format(source, desired)][grade]

    elif (source != None) & (source == desired):
        return grade

    else:
        return None
    
if __name__ == '__main__':
    print(convert_usa2french('5.12b'))
    print(convert_french2usa('7b'))

    import pandas as pd
    print(pd.Series(['5a', '5.10d', 'test']).apply(convert_grade, desired='french'))
    print(pd.Series(['5a', '5.10d']).apply(convert_grade, desired='usa'))