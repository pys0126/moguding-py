import requests
import json
import time
import pendulum
from hashlib import md5
from fake_useragent import UserAgent

session = requests.session()
ua = UserAgent()


def get_proxy():
    url = "http://127.0.0.1:5010/get"
    res_json = session.get(url=url).json()
    if res_json["https"]:
        return {
            "https": "https://" + res_json["proxy"]
        }
    else:
        return {
            "http": "http://" + res_json["proxy"]
        }


def getToken(username: str, password: str, login_type: str = "android"):
    url = "https://api.moguding.net:9000/session/user/v1/login"
    data = {
        "password": password,
        "phone": username,
        "loginType": login_type,
        "uuid": ""
    }
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "user-agent": ua.chrome
    }
    res = session.post(url=url, data=json.dumps(data), headers=headers)
    if res.json()["code"] == 500:
        print(res.json()["msg"])
        exit()
    else:
        sign = get_sign(text=res.json()["data"]["userId"] + res.json()["data"]["userType"])
        return res.json()["data"]["token"], sign, res.json()["data"]["userId"]


def get_sign(text: str):
    s = text + "3478cbbc33f84bd00d75d7dfa69e0daa"
    return md5(s.encode("utf-8")).hexdigest()


def get_plan_id(token: str, sign: str):
    url = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
    data = {
        "state": ""
    }
    headers = {
        'roleKey': 'student',
        "authorization": token,
        "sign": sign,
        "content-type": "application/json; charset=UTF-8",
        "user-agent": ua.chrome
    }
    res = session.post(url=url, data=json.dumps(data), headers=headers)
    return res.json()["data"][0]["planId"]


def save(user_id: str, authorization: str, plan_id: str, country: str, province: str,
         address: str, save_type: str = "START", description: str = "",
         device: str = "Android", latitude: str = None, longitude: str = None):
    text = device + save_type + plan_id + user_id + f"{country}{province}{address}"
    headers = {
        'roleKey': 'student',
        "user-agent": ua.chrome,
        "sign": get_sign(text=text),
        "authorization": authorization,
        "content-type": "application/json; charset=UTF-8"
    }
    data = {
        "country": country,
        "address": f"{country}{province}{address}",
        "province": province,
        "city": province,
        "latitude": latitude,
        "description": description,
        "planId": plan_id,
        "type": save_type,
        "device": device,
        "longitude": longitude
    }
    url = "https://api.moguding.net:9000/attendence/clock/v2/save"
    res = session.post(url=url, headers=headers, data=json.dumps(data))
    if res.json()["code"] == 200:
        print("打卡成功！\n")
    else:
        print("出错了：\n" + res.json() + "\n")


def main(phone = "",
    pwd = "",
    logintype = "android",
    country = "中国",
    province = "",
    address = "",
    description = "",
    latitude = "",
    longitude = ""):
    print(pendulum.now().to_datetime_string() + " 账号：" + phone + " 开始打卡...\n")
    if int(pendulum.now().to_time_string()[:2]) <= 9:
        save_type = "START"
    else:
        save_type = "END"
    try:
        session.proxies.update(get_proxy())
        auth_token, sign_value, user_id = getToken(username=phone, password=pwd, login_type=logintype)
        plan_id = get_plan_id(token=auth_token, sign=sign_value)
        save(user_id=user_id, authorization=auth_token, plan_id=plan_id, country=country, province=province,
            address=address, save_type=save_type, description=description,
            device=logintype.capitalize(), latitude=latitude, longitude=longitude)
    except:
        auth_token, sign_value, user_id = getToken(username=phone, password=pwd, login_type=logintype)
        plan_id = get_plan_id(token=auth_token, sign=sign_value)
        save(user_id=user_id, authorization=auth_token, plan_id=plan_id, country=country, province=province,
            address=address, save_type=save_type, description=description,
            device=logintype.capitalize(), latitude=latitude, longitude=longitude)


if __name__ == "__main__":
    time.sleep(1)
    main(
        phone = "",  # 账号/手机号
        pwd = "",  # 密码
        logintype = "android",  # 打卡设备类型
        country = "中国",  # 国家
        province = "",  # 省市
        address = "",  # 详细地址，没有市
        description = "",  # 打卡描述
        latitude = "",  # 纬度
        longitude = ""  # 经度
    )

