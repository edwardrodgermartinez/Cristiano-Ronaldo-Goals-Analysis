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

def extraction_transformation_cleaning(cr7):

    def web_scraping_astrology():

        html = requests.get("https://en.wikipedia.org/wiki/Astrological_sign")
        soup = BeautifulSoup(html.content, "html.parser")
        signs = soup.find_all("th", {"scope": "row", "class":""})
        signs_simple = [i.getText().replace("\n", "") for i in signs]
        dates = soup.find_all('span', {"class": "nowrap"})
        pattern = re.compile(r'\d{1,2} [A-Za-z]+')
        filtered_dates = [span for span in dates if pattern.match(span.get_text())]
        dates_simple = [i.getText().replace("\n", "") for i in filtered_dates]
        date_ranges = []
        for i in range(0, len(dates_simple), 2):
            if i + 1 < len(dates_simple):
                pair = f"{dates_simple[i]} - {dates_simple[i + 1]}"
                date_ranges.append(pair)
        star_signs = {key: value for key, value in zip(signs_simple, date_ranges)}
        
        date_ranges = {}
        for sign, date_range in star_signs.items():
            start_date, end_date = map(str.strip, date_range.split(' - '))
            start_date = parser.parse(start_date).strftime('%d-%m')
            end_date = parser.parse(end_date).strftime('%d-%m')
            date_ranges[sign] = (start_date, end_date)
   
        return date_ranges

    date_ranges = web_scraping_astrology()

    def cleaning_cristiano_dataset(cr7):
        
        condition_madrid = cr7['Club'] == 'Real Madrid'
        cr7_rm = cr7[condition_madrid]
        desired_columns = ['Season', 'Competition', 'Matchday', 'Date', 'Venue', 'Club', 'Opponent']
        cr7_rm = cr7_rm[desired_columns]
        cr7_rm = cr7_rm.reset_index(drop=True)
        cr7_rm['Date'] = pd.to_datetime(cr7_rm['Date']).dt.strftime('%d-%m')
        cr7_rm['Season'] = cr7_rm['Season'].replace(['Dec-13'], '12/13')
        
        return cr7_rm
    
    cr7_rm = cleaning_cristiano_dataset(cr7)
    
    def transformation(cr7_rm):
        
        def determine_star_sign(date):
            year = 2022
            date = datetime.date(year, int(str(date).split('-')[1]), int(str(date).split('-')[0]))
            for sign, (start_date, end_date) in date_ranges.items():
                if (int(str(start_date).split('-')[1]) == 12) and (int(str(end_date).split('-')[1]) == 1):
                    start_date = datetime.date(2022, int(str(start_date).split('-')[1]), int(str(start_date).split('-')[0]))
                    end_date = datetime.date(2023, int(str(end_date).split('-')[1]), int(str(end_date).split('-')[0]))
                else:
                    start_date = datetime.date(year, int(str(start_date).split('-')[1]), int(str(start_date).split('-')[0]))
                    end_date = datetime.date(year, int(str(end_date).split('-')[1]), int(str(end_date).split('-')[0]))
                if start_date <= date <= end_date:
                    return sign
            return 'Unknown'
        
        cr7_rm['Star Sign'] = cr7_rm['Date'].apply(determine_star_sign)
        cr7_rm['Star Sign'] = cr7_rm['Star Sign'].replace(['Unknown'], 'Capricorn')
        
        distance_from_aquarius = {
        'Aquarius': '0', 
        'Pisces': '1', 
        'Aries': '2', 
        'Taurus': '3', 
        'Gemini': '4', 
        'Cancer': '5', 
        'Leo': '6', 
        'Virgo': '5', 
        'Libra': '4', 
        'Scorpio': '3', 
        'Sagittarius': '2', 
        'Capricorn': '1'}
        
        cr7_rm['Distance from Aquarius'] = cr7_rm['Star Sign'].apply(lambda x: distance_from_aquarius.get(x, 'Unknown'))
        
        return cr7_rm

    cr7_rm_transformed = transformation(cr7_rm)

    cr7_rm_transformed.to_csv('data/cr7_rm_transformed.csv', index=False)
        