import requests
from fake_useragent import UserAgent
import datetime as da

def count_weekend():
    all_weekday_list = []
    year = da.datetime.now().year
    start_time = da.datetime.strptime("{}-01-01".format(year),"%Y-%m-%d")
    while True:
        week = start_time.weekday()
        if week in (0,1,2,3,4):
            sat = (start_time + da.timedelta(days=(5-week))).strftime("%Y-%m-%d")
            sun = (start_time + da.timedelta(days=(6-week))).strftime("%Y-%m-%d")
            all_weekday_list.append(sat)
            all_weekday_list.append(sun)
        elif week == 5:
            sat = start_time.strftime("%Y-%m-%d")
            sun = (start_time + da.timedelta(days=1)).strftime("%Y-%m-%d")
            all_weekday_list.append(sat)
            all_weekday_list.append(sun)
        elif week == 6:
            sun = start_time.strftime("%Y-%m-%d")
            all_weekday_list.append(sun)
        date_sun = da.datetime.strptime(sun,"%Y-%m-%d")
        if start_time.strftime("%Y-%m-%d") == "{}-12-31".format(year):
            break
        print(start_time.strftime("%Y-%m-%d"))
        start_time = date_sun + da.timedelta(days=6)
        if start_time.year > year:
            break
    return all_weekday_list


def count_weekdays_holidays():
    ua = UserAgent()
    headers = {
        """Accept""": """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3""",
        """Accept-Encoding""": """gzip, deflate""",
        """Accept-Language""": """zh-CN,zh;q=0.9""",
        """Cache-Control""": """max-age=0""",
        """Connection""": """keep-alive""",
        """User-Agent""": ua.random, }
    year_list = []
    year = da.datetime.now().year
    for i in range(12):
        year_list.append("{}年{}月".format(year, i + 1))
    holiday_list = []
    for item in year_list:
        url = """https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={}&resource_id=6018&format=json""".format(
            item)
        res = requests.get(url=url, headers=headers).text
        res = eval(res)
        if "holiday" in res["data"][0]:
            if type(res["data"][0]["holiday"]) == list:
                for item in res["data"][0]["holiday"][0]["list"]:
                    print(item)
                    if str(item["date"][:4]) == str(year):
                        holiday_list.append(item["date"])
                for item in res["data"][0]["holiday"][1]["list"]:
                    print(item)
                    if str(item["date"][:4]) == str(year):
                        holiday_list.append(item["date"])

    holiday_list = sorted([da.datetime.strptime(item,"%Y-%m-%d") for item in set(holiday_list)])
    holiday_list = [da.datetime.strftime(item,"%Y-%m-%d") for item in holiday_list]

    all_weekday_list = count_weekend()
    for item in holiday_list:
        if item not in all_weekday_list:
            all_weekday_list.append(item)

    all_weekdays_holidays_list = sorted([da.datetime.strptime(item,"%Y-%m-%d") for item in set(all_weekday_list)])
    all_weekdays_holidays_list = [da.datetime.strftime(item,"%Y-%m-%d") for item in all_weekdays_holidays_list]
    return all_weekdays_holidays_list

if __name__ == '__main__':
    all_weekdays_holidays_list = count_weekdays_holidays()
    print(all_weekdays_holidays_list)
