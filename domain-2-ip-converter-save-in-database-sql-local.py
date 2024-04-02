import pandas as pd
from sqlalchemy import create_engine
import socket

def domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "Resolution Error"

def process_txt_file(input_file):
    # Read domains from TXT file into DataFrame
    df_txt = pd.read_csv(input_file, header=None, names=['Domain'])
    # Convert domain to IP
    df_txt['IP Address'] = df_txt['Domain'].apply(domain_to_ip)
    return df_txt

def process_csv_file(input_file):
    # Read domains from CSV file into DataFrame
    df_csv = pd.read_csv(input_file)
    # Assuming the domain is in the first column
    df_csv['IP Address'] = df_csv.iloc[:, 0].apply(domain_to_ip)
    return df_csv

def to_sql(database_file, df_txt, df_csv):
    engine = create_engine(f'sqlite:///{database_file}')
    # Write DataFrames to SQL
    df_txt.to_sql('txt_domains', con=engine, if_exists='replace', index=False)
    df_csv.to_sql('csv_domains', con=engine, if_exists='replace', index=False)

# Example usage
df_txt = process_txt_file('domains.txt')
df_csv = process_csv_file('domains.csv')
to_sql('domains.db', df_txt, df_csv)