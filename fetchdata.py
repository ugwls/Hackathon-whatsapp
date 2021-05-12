import json
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=110001&date=31-03-2021"


def get_data(pin, date):
    r = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" +
                     pin+"&date="+date, headers=headers)
    data = r.json()
    check = r.text
    if 'Invalid Pincode' in check:
        return "invalid pincode"
    else:
        centers = data["centers"]
        if (len(centers) > 0):
            data_all = []
            for centre in centers:
                sessions = centre["sessions"]
                for session in sessions:
                    data_all.append({"centre_name": centre["name"], "centre_address": centre["address"],
                                     "availability": session["available_capacity"], "date": session["date"]})
            return (data_all)
        else:
            return ("no centre")
