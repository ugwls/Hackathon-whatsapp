from urllib.request import Request, urlopen
import json


def get_data(pin, date):
    print(pin,date)
    try:
        req = Request('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' +
                      pin+"&date="+date, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        data = json.loads(webpage)
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
    except:
        return "invalid pincode"
