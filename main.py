import requests
import time
from datetime import datetime
import smtplib

import os

EMAIL = os.environ.get("EMAIL_ID")
PASSWORD = os.environ.get("EMAIL_PASS")


class CowinSlots:

    def __init__(self):
        self.smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.smtp.login(EMAIL, PASSWORD)

    def getSlotsDetails(self):
        # district id for Jammu, J&K
        # change this with your own district id
        district_id = "230"
        # today's date
        date = datetime.now().strftime("%d-%m-%Y")

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        # }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }

        # url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=" + district_id + "&date=" + date
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + district_id + "&date=" + date

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print("Got response")
                self.getDataFromJSON(response.json())
            elif response.status_code == 200:
                print("Auth Error")
        except:
            print("error")

    def getDataFromJSON(self, data):
        foundSlot = False
        for center in data['centers']:
            for session in center['sessions']:
                if session['min_age_limit'] == 18 & session['available_capacity_dose1'] > 0:
                    self.sendEmail(center['name'], center['pincode'])
                    print("slot found at " + center['name'] + " with PIN : " + center['pincode'])
                    foundSlot = True

        if not foundSlot:
            print("No slots available")

    def sendEmail(self, centerName, pinCode):
        subject = "Found Slot for DOSE-1"
        body = "Found slot at " + centerName + " with PIN : " + pinCode + "\nGoto : https://selfregistration.cowin.gov.in/"
        msg = f"Subject: {subject}\n\n{body}"
        self.smtp.sendmail(EMAIL, EMAIL, msg)
        print("Email Sent")


if __name__ == "__main__":
    slot = CowinSlots()
    while True:
        slot.getSlotsDetails()
        time.sleep(15)
