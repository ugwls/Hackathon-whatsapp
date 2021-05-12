import requests
import json


def get_data(pin, date):
    r = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+pin+"&date="+date, headers={'User-Agent': 'Mozilla/5.0'})
    check = r.text
    print(check)
    # data = json.loads(check)
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
