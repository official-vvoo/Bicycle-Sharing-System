import os
import pandas as pd
import unicodedata

def merge_df_from_storage(path, encoding="cp949", index_col=None, reset_index=False):
    '''
    경로 내 하위 파일(.csv)들을 읽어와서 데이터 프레임 형태로 추출
    '''
    file_list = [x for x in os.listdir(path) if ("._" not in x) and (".csv" in x)]
    file_list.sort()

    for i in range(len(file_list)):
        file_path = os.path.join(path, file_list[i])
        df = pd.read_csv(file_path, encoding=encoding, index_col=index_col)
        if reset_index:
            df.reset_index(drop=True,inplace=True)

        total_df = df if i == 0 else pd.concat((total_df, df))
        
        del file_path
        del df
    
    return total_df.reset_index(drop=True)

def csv_preprocessing(root, file):
    # 분리된 자음모음 결합하기
    ## weather_df 내 행정동('location') 한글 문자열은 자음모음이 분리된 형태로 구성되어 있음.
    ## https://jonsyou.tistory.com/26 참고
    dong=unicodedata.normalize('NFC', file.split('_')[0]) # 행정동명 추출 
    weather_type=file.split('_')[1] # 날씨 정보 종류 
    # 데이터 로드 
    file_path = os.path.join(root, file)
    weather=pd.read_csv(file_path,encoding='cp949')
    # 전처리 
    weather.columns=['날짜','시간',weather_type] # 변수명 변경 
    weather.dropna(axis=0,inplace=True) # 설명 텍스트 행 제거 
    weather['행정동']=[dong]*len(weather) # 행정동명 추가 
    weather['시간']=weather['시간'].astype(int)
    weather['날짜']=weather['날짜'].astype(int)
    weather.reset_index(drop=True,inplace=True)
    # '날짜'열 : datetime에 맞는 형식으로 변경
    day=30
    month=0
    for i in range(len(weather)):
        if weather['날짜'][i] < day :
            month+=1
        day=weather['날짜'][i]
        weather['날짜'][i] = '2022' +str(month).zfill(2) + str(weather['날짜'][i]).zfill(2)
    # '시간'열 : datetime에 맞는 형식으로 변경
    weather['시간']=weather['시간'].apply(lambda x: str(x).zfill(4))
    # '날짜','시간'열 합쳐서 datetime형으로 변경 
    day_time=weather['날짜'].astype(str)+weather['시간']

    weather['날짜시간']=pd.to_datetime(day_time,format="%Y%m%d%H%M")
    weather.drop(['날짜','시간'],axis=1,inplace=True)
    # 데이터 프레임 순서 변경 
    weather=weather[['날짜시간','행정동', weather_type]]
    
    return weather

def makingWeatherDF(path):
    weather_dfs = []
    # 날씨 정보 합치기 
    for (root, directories, files) in os.walk(path):
        for file in files:
            if '.csv' in file:
                weather_df = csv_preprocessing(root, file)
                weather_dfs.append(weather_df)
                
    weather= pd.concat(weather_dfs, axis=0, ignore_index=True)
    return weather