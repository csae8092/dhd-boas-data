import os

# define some directories and file patterns and create them if they don't yet exist
CURRENT_YEAR = "dhd_2019"
PICS = 'Pictures'
CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.split(os.getcwd())[0]
YEAR_DIR = os.path.join(BASE_DIR, CURRENT_YEAR)
DHC_YEAR = os.path.join(BASE_DIR, CURRENT_YEAR, 'DHC')
TEI_DIR = os.path.join(BASE_DIR, CURRENT_YEAR, 'TEI')
IMG_DIR = os.path.join(BASE_DIR, CURRENT_YEAR, 'IMG')
TMP_DIR = os.path.join(BASE_DIR, CURRENT_YEAR, 'DHC', 'tmp')
XML_FILES = "{}/*.xml".format(TMP_DIR)
DHC_FILES = "{}/*.dhc".format(DHC_YEAR)
PATTERNS = [
    ('Goethe-UniversitÃ¤t Frankfurt am Main', 'Goethe-Universität Frankfurt am Main'),
    ('fÃ¼r Informatik und Mathematik', 'für Informatik und Mathematik'),
    ('Mayer-StraÃe 10', 'Mayer-Straße 10')
]
