import os 
import pandas as pd
from datetime import datetime, timedelta
import yaml

def read_daily_data(folder, day):
    """
    Reads data from multiple data sources for a specific day and 
    concatenates them into a single dataframe
    :param folder: path of the folder where the data sources are located
    :param day: date for which data is to be read in the format of 'Month Day, Year'
    :return: a single dataframe containing data from all data sources
    """
    data_sources = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    full_df = pd.DataFrame(columns = ['href', 'title', 'description', 'date', 'data_source'])
    df_list = []
    for data_source in data_sources:
        try:
            #reading the data from csv file
            df = pd.read_csv(os.path.join(folder, data_source,f"{day}.csv"),sep="|")
            #adding the data_source column
            df["data_source"] = data_source
            df_list.append(df)
        except Exception as e:
            #catching the exception if any occurs while reading the csv
            pass
    # concatenating all the dataframe
    if len(df_list)>0:
        full_df = pd.concat(df_list)
    return full_df

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    # loading the configuration from conf.yml file
    with open(os.path.join(current_folder,'conf.yml'), 'r') as file:
        conf = yaml.safe_load(file)
    #path to the data sources
    folder = conf["Health_data_path"]
    # day = datetime.today().strftime("%B %d, %Y")
    # getting the previous day data
    day = (datetime.today() - timedelta(days=1)).strftime("%B %d, %Y")
    #saving the concatenated dataframe to csv
    read_daily_data(folder, day).to_csv(os.path.join("Data/Data_02/Health_Data",f"{day}.csv"),sep="|",index=False)
