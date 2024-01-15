#!/usr/bin/env python
# coding: utf-8

import os
import sys
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def main():

    engine=create_engine('postgresql://root:root@localhost:5432/nba')
    engine.connect()

    folder = os.path.join(sys.path[0],'data','combined')

    for filename in os.listdir(folder):
        table_name = filename.split('.')[0]
        if filename.split('.')[0] != 'games':
            df = pd.read_json(os.path.join(folder,filename))
            if filename.split('.')[0] == 'players':
                df = df[['id','first_name','last_name','position']]
            df.to_sql(name=table_name, con=engine, index=False)

if __name__ == "__main__":
    main()