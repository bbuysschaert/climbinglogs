import json

with open('./grades.json') as ff:
    grades = json.load(ff)

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