import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from twilio.rest.studio.v1 import flow


def gen_pdf(num, data_row):
    pdf = canvas.Canvas(num+".pdf")
    flow_obj = []
    pdf.translate(cm, cm)
    count = len(data_row)
    num = count/10
    a = int(count/num)
    count_new = [0]
    x = 0
    while(x+a < count):
        x = x+a
        count_new.append(x)
    frame1 = Frame(10, 40, 360, 280, showBoundary=1)
    styles = getSampleStyleSheet()
    text1 = """
<b>this is the vaccine slot tracking report:</b>,<br></br>"""
    t1 = Paragraph(text1, style=styles["Normal"])
    flow_obj.append(t1)
    flow_obj.append(Spacer(6, 6))
    text2 = """
<b>data generated at :</b>,<br></br>""" + str(datetime.datetime.now())
    t2 = Paragraph(text2, style=styles["Normal"])
    flow_obj.append(t2)
    frame1.addFromList(flow_obj, pdf)
    pdf.showPage()
    for j in range(len(count_new)):
        frame = Frame(10, 40, 600, 780, showBoundary=1)
        data1 = [["centre_name", "centre_address", "availability", "date"]]
        if(j == len(count_new)-1):
            for row in data_row[count_new[j]:]:
                data1.append(
                    [row["centre_name"], row["centre_address"], row["availability"], row["date"]])
            table = Table(data1, colWidths=[120, 300, 80, 60], rowHeights=[
                          25 for i in range(len(data1))])
            ts = TableStyle([("GRID", (0, 0), (-1, -1), 2, colors.red),
                             ("BACKGROUND", (0, 0), (-1, 0), colors.yellow),
                             ("BACKGROUND", (0, 1), (-1, -1), colors.lightblue),
                             ("SIZE", (0, 0), (-1, -1), 6, colors.yellow),
                             ("ALIGN", (0, 1), (-1, -1), "LEFT")])
            table.setStyle(ts)
            flow_obj.append(Spacer(8, 8))
            flow_obj.append(table)
            frame.addFromList(flow_obj, pdf)
            pdf.showPage()
        else:
            for row in data_row[count_new[j]:count_new[j+1]]:
                data1.append(
                    [row["centre_name"], row["centre_address"], row["availability"], row["date"]])
            table = Table(data1, colWidths=[120, 300, 80, 60], rowHeights=[
                          25 for i in range(len(data1))])
            ts = TableStyle([("GRID", (0, 0), (-1, -1), 2, colors.red),
                             ("BACKGROUND", (0, 0), (-1, 0), colors.yellow),
                             ("BACKGROUND", (0, 1), (-1, -1), colors.lightblue),
                             ("SIZE", (0, 0), (-1, -1), 6, colors.yellow),
                             ("ALIGN", (0, 1), (-1, -1), "LEFT")])
            table.setStyle(ts)
            flow_obj.append(Spacer(8, 8))
            flow_obj.append(table)
            frame.addFromList(flow_obj, pdf)
            pdf.showPage()
    pdf.save()

    return "ok"
