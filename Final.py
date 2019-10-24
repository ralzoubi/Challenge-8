import schedule, time, requests, json, datetime, timedelta
#importing libraries that we will be using here

url = "https://booking.cisco.com/scheduler/Web/Services/Authentication/Authenticate"
#url for booking site authentication
payload = "{\"username\":\"\",\"password\":\"\"}"
#payload for booking site authentication
headers = {
        'Content-Type': "text/plain",
        }
#headers for booking site authentication
response = requests.request("POST", url, verify=False, data=payload, headers=headers)
#output from API call to booking site stored here
extraTokenData = response.text
#changing format to text and storing it in this variable
bookedSessionToken = (extraTokenData.strip('{"sessionToken": '))
#deleting unnecessary part and storing it in bookedSessionToken
bookedSessionToken = (bookedSessionToken.split('"')[0])
#saving only token in bookedSessionToken
#print("This is the session token for the booking website: " + bookedSessionToken)

urlRes = "https://booking.cisco.com/scheduler/Web/Services/Reservations/"
#url used in API call to booking.cisco.com
payloadRes = " "
#payload for reservation
headersRes = {
        'X-Booked-SessionToken': "f3b809aca27ccb657af2748aa28172b9ebd71723e54eaab0dc",
        'X-Booked-UserId': "121",
}
#header contains the session token we made a variable for to access the booking website
responseRes = requests.request("GET", urlRes, verify=False, data=payloadRes, headers=headersRes)
#stores "GET" API call to booking website response in responseRes; responseRes stores all of the reservations on the site
dataRes = responseRes.json()
#converts responseRes to json format and stores it in dataRes

urlBD = "http://ixc-dashboard.cisco.com/api/card/131/query/json"
#url used in API call to ixc-dashboard.cisco.com
headersBD = {
        'Content-Type': "application/json",
        'X-Metabase-Session': "5a8aa7b6-e4d8-4a71-82a0-0e4eadccb632",
}
#headers for API call to dashboard
responseBD = requests.request("POST", urlBD, headers=headersBD)
#stores "POST" API call to dashboard website response in responseBD; responseBD stores all of the briefing documents on the site
dataBD = responseBD.json()
#converts responseBD to json format and stores it in dataBD

def getRes():
#function for getting reservation two days from now
    refNum = ""
    #variable to store the reference number of the reservation two days from now
    futureDate = datetime.datetime.now() + datetime.timedelta(days=10)
    #saving the date two days from now in variable futureDate
    formatDate = (datetime.datetime.strptime(str(futureDate), "%Y-%m-%d %H:%M:%S.%f").strftime('%Y-%m-%d'))
    #formatting the date to allow for comparison with start date from reservation

    for item in dataRes['reservations']:
    #looping through each item inside each reservation
        fullStartDate = item['startDate']
        #variable storing the full start date and time
        splitStartDate = fullStartDate.split('T')
        #variable storing the split date and time
        startDate, startTime = splitStartDate[0], splitStartDate[1]
        #variables storing start date and time separately
        formatStartDate = (datetime.datetime.strptime(str(startDate), "%Y-%m-%d").strftime('%m/%d/%Y'))
        #formatting date to match date format required in createV()
        formatStartTime = (datetime.datetime.strptime(str(startTime), "%H:%M:%S+%f").strftime('%H:%M:%S %p'))
        #formatting time to match time format required in createV()
        startDateTime = formatStartDate + " " + formatStartTime
        #variable storing concatenated date and time to match format required in createV()
        #print(startDateTime)

        fullEndDate = item['endDate']
        #variable storing the full end date and time
        splitEndDate = fullEndDate.split('T')
        #variable storing the split date and time
        endDate, endTime = splitEndDate[0], splitEndDate[1]
        #variables storing end date and time separately
        formatEndDate = (datetime.datetime.strptime(str(endDate), "%Y-%m-%d").strftime('%m/%d/%Y'))
        #formatting date to match date format required in createV()
        formatEndTime = (datetime.datetime.strptime(str(endTime), "%H:%M:%S+%f").strftime('%H:%M:%S %p'))
        #formatting time to match format required in createV()
        endDateTime = formatEndDate + " " + formatEndTime
        #variable storing concatenated date and time to match format required in createV()
        #print(endDateTime)

        formatDateRes = (str(item).split("T")[0])
        #storing the date of the reservation in variable formatDateRes

        if formatDate in formatDateRes:
        #checking that the date in the reservation is two days from now
            refNum = item['referenceNumber']
            #storing reference number of this reservation in refNum
            #print("\n\nThe date of this reservation matches the date two days from now.")
            #print("\n\nThis is the information about the reservation: \nStart Date: " + str(item))
            #print("\n\nThis is the reference number of this reservation: " + refNum)
            urlSFDC = "https://booking.cisco.com/scheduler/Web/Services/Reservations/{}".format(refNum)
            #because we want to get the sfdc deal id for this reservation we added refNum as a variable in the url that gets the custom attributes of this reservation
            #print("\n\nThis is the URL we are using to get all the specific information about this reservation: " + urlSFDC)
            payloadSFDC = ""
            #payload for API call to booking site
            headersSFDC = {
                'X-Booked-SessionToken': "f3b809aca27ccb657af2748aa28172b9ebd71723e54eaab0dc",
                'X-Booked-UserId': "121"
                }
            #headers for API call to booking site
            responseSFDC = requests.request("GET", urlSFDC, verify=False, data=payloadSFDC, headers=headersSFDC)
            #stores "GET" API call to booking website response in responseSFDC; responseSFDC stores all of the information about this reservation
            dataSFDC = responseSFDC.json()
            #converts responseSFDC to json format and stores it in dataSFDC

            def getSFDCId():
            #function for getting the SFDC ID for the selected reservations


                for item in dataSFDC['customAttributes']:
                #looping through each item within the custom attributes inside of the dataSFDC

                    if item['label'] == 'SFDC Deal ID':
                    #checking if we've reached the sfdc deal id
                        sfdcRes = item['value']
                        #storing sfdc deal id in variable sfdcRes
                        #print("This is the SFDC Deal ID of the reservation: " + sfdcRes)
                        def getBD():
                            sid = ""
                            #variable to store sid of selected reservation
                            visitBuilding = "DBICXC"
                            #static variable storing visit building
                            visitorName = ""
                            #variable storing the full name of the attendee
                            visitorCompany = ""
                            #variable storing visitor's company name
                            visitorEmail = ""
                            #variable storing visitor's email
                            visitorFirstName = ""
                            #variable storing visitor's first name
                            visitorLastName = ""
                            #variable storing visitor's last name
                            listOfFirstNames = []
                            listOfLastNames = []
                            listOfEmails = []
                            for item in dataBD:
                            #looping through each item within dataBD
                                if item['name'] == 'sfdc_deal_id':
                                    sfdcBD = item['value']
                                    #inside of briefing document we are gettting all the sfdc deal ids for the comparison
                                    #print("These are the SFDC Deal IDs in the Briefing Document: " + sfdcBD)
                                    if sfdcBD == sfdcRes:
                                    #finding match between sfdcBD and sfdcRes
                                        sid = item['sid']
                                        #when we get the match between the sfdc deal ids in the reservation and doc, we need the sid
                                        #print("The SID: " + str(sid))
                                if item['sid'] == sid:
                                #checking that the sid of each field is the same to ensure that we are working with the same BD
                                    #print(item['name'])


                                    if item['name'] == "please_provide_the_names_of_attendees":
                                    #finding item within document that provides visitors' names
                                        visitorName = str(item['value'])
                                        #print(visitorName)
                                        #storing the visitor's full name inside of variable visitorName
                                        a = visitorName.split()
                                        #splitting between visitor's first and last name
                                        visitorFirstName,visitorLastName = a[0],a[1]
                                        #print("This is the first name: " + visitorFirstName)
                                        #print("This is the last name: " + visitorLastName)
                                        listOfFirstNames.append(visitorFirstName)
                                        listOfLastNames.append(visitorLastName)
                                        #storing visitor's first name in visitorFirstName and visitor's last name in visitorLastName
                                        #print("This is the list of first names: " + str(listOfFirstNames))
                                        #print("This is the list of last names: " + str(listOfLastNames))
                                    if item['name'] == "customer_name" and item['value'] != "NA":
                                    #finding item within document that provides visitors' company name
                                        visitorCompany = item['value']
                                        #print(visitorCompany)
                                        #here we get the company name
                                    if 'email' in str(item['name']):
                                        visitorEmail = item['value']
                                        listOfEmails.append(visitorEmail)
                                        #print("This is the list of emails: " + str(listOfEmails))
                                        #here we get the visitors' emails

                                        #here we get the visitors' emails
                            def createV():

                                        #function for creating visit on vms
                                urlCV = "https://visit.cisco.com/rest/api/createvisit"
                                        #url used for API call to vms
                                headersCV = {
                                        'Authorization': "Basic d3Bydm1zYXBpLmdlbiAgIDpXcHJ2bXNAMTIzNA==",
                                        'Content-Type': "text/plain",
                                        }
                                        #headers for API call to vms
                                payloadCV = "{\r\n  \"visitBuilding\": \"%s\",\r\n  \"visitorList\": [\r\n    {\r\n      \"visitorCompany\": \"%s\",\r\n      \"visitorEmail\": \"%s\",\r\n      \"visitorFirstName\": \"%s\",\r\n      \"visitorLastName\": \"%s\",\r\n      \"visitComments\": \"\",\r\n      \"visitorMobile\": \"000111\"\r\n    }\r\n  ],\r\n  \"hostEmail\": \"mea-dit\",\r\n  \"visitStartDate\": \"%s\",\r\n  \"visitEndDate\": \"%s\",\r\n \"checkInVisitor\": false,\r\n  \"notifyVisitor\": true,\r\n  \"notifyHost\": true\r\n}\r\n" % (visitBuilding, visitorCompany, listOfEmails[i], listOfFirstNames[i], listOfLastNames[i], startDateTime, endDateTime)
                                        #payload for API call to vms
                                print(payloadCV)
                                responseCV = requests.request("POST", urlCV, verify=False, data=payloadCV, headers=headersCV)
                                        #storing response to API call in responseCV
                                dataCV = responseCV.json()
                                    #converting to json and storing in dataCV
                                print(dataCV)

                            i=0
                            while i < len(listOfEmails)-1:
                                createV()
                                i+=1
                        getBD()
            getSFDCId()

getRes()


"""schedule.every().sunday.at("22:00").do(job)
schedule.every().monday.at("22:00").do(job)
schedule.every().tuesday.at("22:00").do(job)
schedule.every().wednesday.at("22:00").do(job)
schedule.every().thursday.at("22:00").do(job)
schedule.every().friday.at("22:00").do(job)
schedule.every().saturday.at("22:00").do(job)

while True:
schedule.run_pending()
time.sleep(1)"""
