import requests
from datetime import datetime
from fastapi import HTTPException

def calculate_profit(scheme_code, start_date, end_date, capital=1000000.0):
    try:
        # Format dates
        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')

        # Get data from API
        api_url = f'https://api.mfapi.in/mf/{scheme_code}'
        data = requests.get(api_url).json()

        # Find the available dates
        available_dates = [datetime.strptime(date, '%d-%m-%Y') for date in data['data']['date']]
        available_dates.sort()

        # Find the next available date if start_date or end_date not present in the data
        start_date = next((d for d in available_dates if d >= start_date), available_dates[-1])
        end_date = next((d for d in available_dates if d >= end_date), available_dates[-1])

        # Get NAV on start and end dates
        nav_start = data['data']['nav'][data['data']['date'].index(start_date.strftime('%d-%m-%Y'))]
        nav_end = data['data']['nav'][data['data']['date'].index(end_date.strftime('%d-%m-%Y'))]

        # Calculate units and profit
        units_allotted = capital / nav_start
        value_on_redemption = units_allotted * nav_end
        net_profit = value_on_redemption - capital

        return net_profit
    except (KeyError, IndexError, ZeroDivisionError) as e:
        raise HTTPException(status_code=500, detail=f"Error calculating profit: {str(e)}")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
