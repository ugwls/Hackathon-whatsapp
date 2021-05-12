import csv
from pymongo import MongoClient
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json
from pymongo.mongo_client import MongoClient
from fetchdata import get_data
from report_pdf import gen_pdf


client = MongoClient(
    "mongodb+srv://ujjwal:Ujjwal.16@cluster0.hnhs0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['whatsapp']
collection = db['cowin_center']

app = Flask(__name__)


@app.route("/sms", methods=["GET", "POST"])
def reply():
    num = request.form.get("From")
    num = num.replace("whatsapp:", "")
    print(num)
    msg_text = request.form.get("Body")
    if "," in msg_text:
        pin = msg_text.split(",")[0]
        date = msg_text.split(",")[1]
        x = collection.find_one({"NUMBER": num})
        try:
            status = x["status"]
        except:
            pass
        if(bool(x) == False):
            collection.insert_one({"NUMBER": num, "status": "first"})
            msg = MessagingResponse()
            resp = msg.message("""Hello this is Cowin-bot,developed by Ujjwal Sharma, to get covid vaccine availability related informaion please follow the below
enter your pincode and date separated by comma, for example if your pincode is 110045 and date you want for 15 th may 2021, then your input should be 
110045,15-05-2021""")
            return (str(msg))
        else:
            if (status == "first"):
                data = get_data(pin, date)
                msg = MessagingResponse()

                if (data == "invalid pincode"):
                    resp = msg.message("please entre valid pincode")
                    return (str(msg))
                elif (data == "no centre"):
                    resp = msg.message(
                        "no centre found for your given input ,please try again later or else try with find with nearest pincode")
                    return (str(msg))
                else:
                    if(len(data) < 15):
                        parse_data = json.dumps(data)
                        parse_data = parse_data.replace("{", "")
                        parse_data = parse_data.replace("}", "\n\n")
                        parse_data = parse_data.replace("[", "")
                        parse_data = parse_data.replace("]", "")
                        parse_data = parse_data.replace(",", "\n")
                        resp = msg.message(parse_data)
                        # print(parse_data)
                        return (str(msg))
                    else:
                        print("abc")
                        resp1 = msg.message(
                            "please find the pdf for more information")
                        gen_pdf(num, data)
                        resp1.media(
                            "https://b9d59c792d84.ngrok.io/cowin_center/"+num+".pdf")
                        return(str(msg))

    else:
        msg = MessagingResponse()
        resp = msg.message("""Hello this is Cowin-bot,developed by Ujjwal Sharma, to get covid vaccine availability related informaion please follow the below
enter your pincode and date separated by comma, for example if your pincode is 110045 and date you want for 15 th may 2021, then your input should be 
110045,15-05-2021""")
        return (str(msg))

        print(num)

# https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=110001&date=31-03-2021


#headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
if __name__ == "__main__":
    app.run(port=5000)
