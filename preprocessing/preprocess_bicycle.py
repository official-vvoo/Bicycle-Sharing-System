import os
import argparse
import numpy as np
import pandas as pd
from datetime import datetime

import warnings
warnings.filterwarnings(action='ignore')


CONST_STR_EXTENSION = ".csv"
CONST_STR_BICYCLE = "bicycle"
CONST_STR_DATE = "date"
CONST_STR_TIME = 'time'
CONST_STR_HOUR = "hour"
CONST_STR_MINUTE = "minute"
CONST_STR_STATION = "station_ID"
CONST_STR_RENTAL = "num_rental"
CONST_STR_RETURN = "num_return"
CONST_STR_TOTAL_USE_TIME = "total_time"
CONST_STR_TOTAL_DISTANCE = "total_distance"


CONST_LIST_COLUMNS = ['기준_날짜', '기준_집계', '기준_시간대', '시작_대여소_ID', '시작_대여소명', '종료_대여소_ID', '종료_대여소명', '전체_건수', '전체_이용_분', '전체_이용_거리']

# define column name
CONST_COL_DATE = CONST_LIST_COLUMNS[0]
CONST_COL_TIME = CONST_LIST_COLUMNS[2]
CONST_COL_STATUS = CONST_LIST_COLUMNS[1]
CONST_COL_START_STATION_ID = CONST_LIST_COLUMNS[3]
CONST_COL_FINISH_STATION_ID = CONST_LIST_COLUMNS[5]
CONST_COL_BIKES = CONST_LIST_COLUMNS[7]
CONST_COL_TOTAL_USE_TIME = CONST_LIST_COLUMNS[8]
CONST_COL_TOTAL_USE_DISTANCE = CONST_LIST_COLUMNS[9]

def printl(msg):
    print(f"[{datetime.now()}]", msg)

class Config():
    def __init__(self):
        self.PATH_INPUT = None
        self.PATH_OUTPUT = None
        self.ENCODING = None
        
        self.header = False
        self.col_list = None

def __get_arguments():
    parser = argparse.ArgumentParser()

    '''
    example code
    python preprocess_bicycle.py -i "./1.source_data/서울시따릉이대여소별대여반납승객수(22년1월~22년9월).csv" -o "./2.preprocessed_data" -e "cp949"
    '''

    parser.add_argument('-i', '--input', type=str, required=True, help='[string] csv file path')
    parser.add_argument('-o', '--output', type=str, required=True, help='[string] directory or csv file path for save transform input file')
    parser.add_argument('-e', '--encoding', type=str, choices=['utf-8', 'cp949'], required=False, default='utf-8', help='[choices] encoding of csv file that must in ["cp949", "utf-8"]')
    parser.add_argument('--header', action="store_true", default=False, help='[store_true] if csv file have column, check option')
    parser.add_argument('--columns', type=str, action='append', dest='col_list', required=False, default=None, help='[append string] set column of input csv file')
    
    args = parser.parse_args()

    return args

def __parse_arguments(args):
    config = Config()

    config.PATH_INPUT = args.input
    config.PATH_OUTPUT = args.output
    config.ENCODING = args.encoding
    config.header=args.header
    config.col_list = args.col_list if args.col_list != None else CONST_LIST_COLUMNS

    return config
    
def read_data(config):
    assert os.path.isfile(config.PATH_INPUT)
    assert os.path.splitext(config.PATH_INPUT)[-1] == CONST_STR_EXTENSION
    assert type(config.col_list) == list

    if config.header:
        return pd.read_csv(config.PATH_INPUT, encoding=config.ENCODING)
    else:
        return pd.read_csv(config.PATH_INPUT, encoding=config.ENCODING, header=None, names=config.col_list)

def save_data(df, config):
    assert os.path.exists(config.PATH_OUTPUT)

    path = config.PATH_OUTPUT
    if os.path.isdir(path):
        path = os.path.join(path, CONST_STR_BICYCLE+CONST_STR_EXTENSION)

    if os.path.exists(path):
        path.replace(CONST_STR_BICYCLE, CONST_STR_BICYCLE+"_"+str(datetime.now())+CONST_STR_EXTENSION)
    
    df.to_csv(path, encoding=config.ENCODING, index=False)
    printl(f"Success to save data: {path}")

def group_hour(df):
    printl("start to group dataframe by hour")
    num_df = len(df)
    df[CONST_COL_TIME] = df[CONST_COL_TIME].astype(int)
    df[CONST_STR_HOUR] = df[CONST_COL_TIME]//100
    
    df = df.groupby([CONST_COL_DATE, CONST_COL_STATUS, CONST_STR_HOUR, CONST_COL_START_STATION_ID, CONST_COL_FINISH_STATION_ID]).sum().reset_index(drop=False)
    df = df[[CONST_COL_DATE, CONST_COL_STATUS, CONST_STR_HOUR, CONST_COL_START_STATION_ID, CONST_COL_FINISH_STATION_ID, CONST_COL_BIKES, CONST_COL_TOTAL_USE_TIME, CONST_COL_TOTAL_USE_DISTANCE]]
    df.columns = [CONST_COL_DATE, CONST_COL_STATUS, CONST_COL_TIME, CONST_COL_START_STATION_ID, CONST_COL_FINISH_STATION_ID, CONST_COL_BIKES, CONST_COL_TOTAL_USE_TIME, CONST_COL_TOTAL_USE_DISTANCE]
    printl(f"done to group dataframe by hour. length of dataframe: {num_df} > {len(df)}")
    return df

def split_status(df):
    printl("start to divide ")
    df[CONST_COL_STATUS] = df[CONST_COL_STATUS].astype(int)
    # 대여 데이터
    rental_df = df[df[CONST_COL_STATUS]==0].reset_index(drop=True)
    # 반납 데이터
    return_df = df[df[CONST_COL_STATUS]==1].reset_index(drop=True)
    if len(rental_df) + len(return_df) == len(df):
        printl("Success to divide dataframe")
        return rental_df, return_df
    else:
        raise ValueError(f"Fail to split all dataframe: df1({len(rental_df)}) + df2({len(return_df)}) = {len(rental_df) + len(return_df)}, not {len(df)}")

def generate_time_station_df(date_list, time_list, station_list):
    printl("start to generate dataframe of all cases")
    num_date = len(date_list)
    num_time = len(time_list)
    num_station = len(station_list)
    num_total = num_date*num_time*num_station
    
    date_df = pd.DataFrame(date_list*num_time*num_station, columns=[CONST_STR_DATE]).sort_values(CONST_STR_DATE).reset_index(drop=True)
    time_df = pd.DataFrame(time_list*num_date*num_station, columns=[CONST_STR_TIME])
    new_station_list = station_list*num_time
    new_station_list.sort()
    station_df = pd.DataFrame(new_station_list*num_date, columns=[CONST_STR_STATION])

    date_df = date_df
    date_time_df = pd.concat((date_df, time_df), axis=1)
    df = pd.concat((date_time_df, station_df), axis=1, join='outer')

    if df.duplicated().sum() == 0:
        printl("Success to generate dataframe of all cases")
        return df
    else:
        raise ValueError(f"Fail to generate dataframe of all cases: {df.duplicated().sum()} cases are duplicated")


def transform_rental_bicycle(rental_df):
    printl("start to transform rental bicycle data")
    rental_df = rental_df.groupby([CONST_COL_DATE, CONST_COL_STATUS, CONST_COL_TIME, CONST_COL_START_STATION_ID]).sum().reset_index(drop=False)

    date_list = list(rental_df[CONST_COL_DATE].unique())
    time_list = list(rental_df[CONST_COL_TIME].unique())
    station_list = list(rental_df[CONST_COL_START_STATION_ID].unique())

    df = generate_time_station_df(date_list, time_list, station_list)
    
    rental_df.columns = [CONST_STR_DATE, CONST_COL_STATUS, CONST_STR_TIME, CONST_STR_STATION, CONST_STR_RENTAL, CONST_STR_TOTAL_USE_TIME, CONST_STR_TOTAL_DISTANCE]
    df = pd.merge(df, rental_df, on=[CONST_STR_DATE, CONST_STR_TIME, CONST_STR_STATION], how='outer')

    num_null = df[CONST_STR_RENTAL].isnull().sum()
    if len(rental_df) + num_null == len(df):
        df = df[[CONST_STR_DATE, CONST_STR_TIME, CONST_STR_STATION, CONST_STR_RENTAL, CONST_STR_TOTAL_USE_TIME, CONST_STR_TOTAL_DISTANCE]]
        df.fillna(0, inplace=True)
        df[CONST_STR_RENTAL] = df[CONST_STR_RENTAL].astype(int)
        printl("Success to transform rental bicycle data")
        return df
    else:
        raise ValueError(f"Fail to merge dataframe: rental({len(rental_df)}) + null({num_null}) = {len(rental_df) + num_null}, not {len(df)}")

def transform_return_bicycle(return_df):
    printl("start to transform return bicycle data")
    return_df = return_df[[CONST_COL_DATE, CONST_COL_TIME, CONST_COL_FINISH_STATION_ID, CONST_COL_BIKES]].groupby([CONST_COL_DATE, CONST_COL_TIME, CONST_COL_FINISH_STATION_ID]).sum().reset_index(drop=False)
    return_df.columns = [CONST_STR_DATE, CONST_STR_TIME, CONST_STR_STATION, CONST_STR_RETURN]

    printl("done to transform return bicycle data")
    return return_df

def transform_bicycle(df):
    printl("start to transform dataframe")
    df = group_hour(df)
    
    rental_df, return_df = split_status(df)
    
    rental_df = transform_rental_bicycle(rental_df)
    return_df = transform_return_bicycle(return_df)

    df = pd.merge(rental_df, return_df, on=[CONST_STR_DATE, CONST_STR_TIME, CONST_STR_STATION], how='left')

    num_null = df[CONST_STR_RETURN].isnull().sum()
    df.fillna(0, inplace=True)
    df[CONST_STR_RETURN] = df[CONST_STR_RETURN].astype(int)
    printl(f"done to transform dataframe: {len(df)}")
    return df

def main(config):
    printl("start to load file")
    df = read_data(config)
    printl("done to load file")

    df = transform_bicycle(df)

    save_data(df, config)

if __name__ == "__main__":
    args = __get_arguments()
    config = __parse_arguments(args)
    main(config)