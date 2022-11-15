# Dependencies
import os
import json
from pandas.api.types import CategoricalDtype

# Read in the grade conversion file using the relative path
# See https://stackoverflow.com/a/3718923/2931774
file_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(file_path, 'grades.json')) as ff:
    grades = json.load(ff)

def create_ordinalcats_french() -> CategoricalDtype:
    """
    Create a Pandas CategoricalDtype that defines the ordinal categeories of the climbing grades in the French system
    """
    grades_fr = list(grades['French2USA'].keys())
    grades_fr = sorted(grades_fr)
    return CategoricalDtype(categories=grades_fr, ordered=True)

def create_ordinalcats_usa() -> CategoricalDtype:
    """
    Create a Pandas CategoricalDtype that defines the ordinal categeories of the climbing grades in the USA system
    """
    grades_usa = list(grades['USA2French'].keys())
    grades_usa = sorted(grades_usa)
    return CategoricalDtype(categories=grades_usa, ordered=True)

def convert_usa2french(val: str) -> str:
    """
    Convert a climbing grade from the USA scale to French Font scale
    >>> convert_usa2french('5.12b')
    '7b'
    """
    return grades['USA2French'][val]

def convert_french2usa(val: str) -> str:
    """
    Convert a climbing grade from the French Font scale to the USA scale 
    >>> convert_usa2french('7b')
    '5.12b'
    """
    return grades['French2USA'][val]

if __name__ == '__main__':
    print(convert_usa2french('5.12b'))
    print(convert_french2usa('7b'))