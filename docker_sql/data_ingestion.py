import os
import sys
import argparse
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import sessionmaker

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db

    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    meta_data = MetaData()
    Session = sessionmaker(bind=engine)
    session = Session()
    

    folder_split = sys.path[0].split('\\')[0:-1]
    base_folder = '\\'.join(folder_split)
    data_folder = os.path.join(base_folder,'data')

    # Dropping Old Tables
    for item in ['games','players','season_averages','teams']:
        try:
            table = Table(item, meta_data, autoload_with=engine)
            table.drop(engine)
            print(f'Dropped: {item}')
        except NoSuchTableError:
            print(f'{item} - Table Does Not Exist')

    # Ingesting New Tables From Scratch
    for filename in os.listdir(data_folder):
        print(f'Ingesting: {filename}')
        table_name = filename.split('.')[0]
        df = pd.read_json(os.path.join(data_folder,filename))
        if filename.split('.')[0] == 'players':
            df = df[['id','first_name','last_name','position']]
        df.to_sql(name=table_name, con=engine, index=False)

    # Renaming Columns in Season Averages Table
    ddl_statement = """ALTER TABLE public.season_averages RENAME COLUMN min TO minutes_played;
         ALTER TABLE public.season_averages RENAME COLUMN fgm TO fg_made;
         ALTER TABLE public.season_averages RENAME COLUMN fga TO fg_attempted;
         ALTER TABLE public.season_averages RENAME COLUMN fg3m TO fg_3pt_made;
         ALTER TABLE public.season_averages RENAME COLUMN fg3a TO fg_3pt_attempted;
         ALTER TABLE public.season_averages RENAME COLUMN ftm TO free_throws_made;
         ALTER TABLE public.season_averages RENAME COLUMN fta TO free_throws_attempted;
         ALTER TABLE public.season_averages RENAME COLUMN oreb TO offensive_rebounds;
         ALTER TABLE public.season_averages RENAME COLUMN dreb TO defensive_rebounds;
         ALTER TABLE public.season_averages RENAME COLUMN reb TO rebounds;
         ALTER TABLE public.season_averages RENAME COLUMN ast TO assists;
         ALTER TABLE public.season_averages RENAME COLUMN turnover TO turnovers;
         ALTER TABLE public.season_averages RENAME COLUMN stl TO steals;
         ALTER TABLE public.season_averages RENAME COLUMN blk TO blocks;
         ALTER TABLE public.season_averages RENAME COLUMN pf TO personal_fouls;
         ALTER TABLE public.season_averages RENAME COLUMN pts TO points;
         ALTER TABLE public.season_averages RENAME COLUMN fg_pct TO field_goal_percentage;
         ALTER TABLE public.season_averages RENAME COLUMN fg3_pct TO fg_3pt_percentage;
         ALTER TABLE public.season_averages RENAME COLUMN ft_pct TO free_throw_percentage;
    """
    pd.read_sql(ddl_statement, con=engine)

    # with engine.connect() as connection:
    #     connection.execute(ddl_statement)
    # print("Altered season_averages")

    season_average_table = Table('season_averages', meta_data, autoload_with=engine)
    season_average_table.c.min.alter(name='minutes_played')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest JSON data into Postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db for postgres')
    
    args = parser.parse_args()
    main(args)