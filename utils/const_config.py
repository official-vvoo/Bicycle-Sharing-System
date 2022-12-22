import os

# define string
## define folder name
CONST_STR_SOURCEDATA = "1.source_data"
CONST_STR_PREPROCESSDATA = "2.preprocessed_data"
CONST_STR_TEMP = "temp"

CONST_STR_ENCODING = "cp949"
CONST_STR_EXTENSION = ".csv"
CONST_STR_BICYCLE = "bicycle"
CONST_STR_BUS = "bus"
CONST_STR_SUBWAY = "subway"

## define column name
CONST_STR_DATE = "date"
CONST_STR_MONTH = "month"
CONST_STR_WEEKDAY = "weekday"
CONST_STR_TIME = 'time'
CONST_STR_HOUR = "hour"
CONST_STR_MINUTE = "minute"
CONST_STR_STATION = "station_ID"
CONST_STR_RENTAL = "num_rental"
CONST_STR_RETURN = "num_return"
CONST_STR_TOTAL_USE_TIME = "total_time"
CONST_STR_TOTAL_DISTANCE = "total_distance"
CONST_STR_DEM = 'dem'
CONST_STR_BUS_USER = 'bus_user'
CONST_STR_SUBWAY_USER = 'subway_user'

# define float
CONST_FLOAT_SIGNIFICANCE_LEVEL = 0.05

# define path
## git path
CONST_PATH_GIT = os.path.dirname(os.path.abspath(os.getcwd()))
CONST_PATH_WORKSPACE = os.path.dirname(CONST_PATH_GIT)

## 기본 폴더 설정
CONST_PATH_SOURCEDATA = os.path.join(CONST_PATH_WORKSPACE, CONST_STR_SOURCEDATA)
CONST_PATH_PREPROCESSEDDATA = os.path.join(CONST_PATH_WORKSPACE, CONST_STR_PREPROCESSDATA)
CONST_PATH_TEMP = os.path.join(CONST_PATH_WORKSPACE, CONST_STR_TEMP)

## source data
CONST_PATH_BUS_META = os.path.join(CONST_PATH_SOURCEDATA, "서울시 버스정류소 위치정보/서울시 버스정류소 위치정보(2022.08.24).csv")
CONST_PATH_BUS_DAILY = os.path.join(CONST_PATH_SOURCEDATA, "서울시 버스노선별 정류장별 승하차 인원 정보")
CONST_PATH_BUS_TIME = os.path.join(CONST_PATH_SOURCEDATA, "서울시 버스노선별 정류장별 시간대별 승하차 인원 정보")
CONST_PATH_SUBWAY_DAILY = os.path.join(CONST_PATH_SOURCEDATA, "서울시 지하철호선별 역별 승하차 인원 정보")
CONST_PATH_SUBWAY_TIME = os.path.join(CONST_PATH_SOURCEDATA, "서울시 지하철 호선별 역별 시간대별 승하차 인원 정보")
CONST_PATH_SOURCE_BICYCLE = os.path.join(CONST_PATH_SOURCEDATA, "서울시따릉이대여소별대여반납승객수(22년1월~22년9월).csv")
CONST_PATH_WEATHER_RAIN = os.path.join(CONST_PATH_SOURCEDATA, "서울시 동별 강수 기온 풍속 정보(22.01~22.09)", "weather_rain")
CONST_PATH_WEATHER_TEMPERATURE = os.path.join(CONST_PATH_SOURCEDATA, "서울시 동별 강수 기온 풍속 정보(22.01~22.09)", "weather_temp")
CONST_PATH_WEATHER_WIND = os.path.join(CONST_PATH_SOURCEDATA, "서울시 동별 강수 기온 풍속 정보(22.01~22.09)", "weather_wind")

## preprocesed data
CONST_PATH_MAPPING = os.path.join(CONST_PATH_PREPROCESSEDDATA, "서울시_따릉이대여소별_고도_지하철역_정거장매핑.csv")
CONST_PATH_BICYCLE = os.path.join(CONST_PATH_PREPROCESSEDDATA, CONST_STR_BICYCLE+CONST_STR_EXTENSION)


# source data
## bicycle
### column list
CONST_LIST_COLUMNS = ['기준_날짜', '기준_집계', '기준_시간대', '시작_대여소_ID', '시작_대여소명', '종료_대여소_ID', '종료_대여소명', '전체_건수', '전체_이용_분', '전체_이용_거리']

### column name
CONST_COL_DATE = CONST_LIST_COLUMNS[0]
CONST_COL_TIME = CONST_LIST_COLUMNS[2]
CONST_COL_STATUS = CONST_LIST_COLUMNS[1]
CONST_COL_START_STATION_ID = CONST_LIST_COLUMNS[3]
CONST_COL_FINISH_STATION_ID = CONST_LIST_COLUMNS[5]
CONST_COL_BIKES = CONST_LIST_COLUMNS[7]
CONST_COL_TOTAL_USE_TIME = CONST_LIST_COLUMNS[8]
CONST_COL_TOTAL_USE_DISTANCE = CONST_LIST_COLUMNS[9]