import os 
import pandas as pd
from datetime import datetime, timedelta
import yaml

def read_daily_data(folder, day):
    data_sources = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    full_df = pd.DataFrame(columns = ['href', 'title', 'description', 'date', 'data_source'])
    df_list = []
    for data_source in data_sources:
        try:
            df = pd.read_csv(os.path.join(folder, data_source,f"{day}.csv"),sep="|")
            df["data_source"] = data_source
            df_list.append(df)
        except Exception as e:
            pass
    if len(df_list)>0:
        full_df = pd.concat(df_list)
    return full_df

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_folder,'conf.yml'), 'r') as file:
        conf = yaml.safe_load(file)
    folder = conf["Health_data_path"]
    # day = datetime.today().strftime("%B %d, %Y")
    day = (datetime.today() - timedelta(days=1)).strftime("%B %d, %Y")
    read_daily_data(folder, day).to_csv(os.path.join("Data/Data_02/Health_Data",f"{day}.csv"),sep="|",index=False)



