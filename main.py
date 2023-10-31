import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests
import datetime
from dateutil import parser
from src import transformation

cr7 = pd.read_csv('data/cr7.csv', encoding='latin1')

transformation.extraction_transformation_cleaning(cr7)

from src import visualisation

cr7_rm_transformed = pd.read_csv('data/cr7_rm_transformed.csv', encoding='latin1')

visualisation.visualisation(cr7_rm_transformed)
