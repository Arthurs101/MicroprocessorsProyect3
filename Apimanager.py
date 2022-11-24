import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
sa = gspread.service_account(filename="service_account.json")
sh = sa.open("ProyuectData")
wks = sh.worksheet("RawData")
def sendElements(raw_data):
    df = pd.DataFrame(raw_data)
    #upload data
    set_with_dataframe(wks, df)
    
    
   