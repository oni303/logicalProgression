from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import time
import datetime
import sets
import sqlite3

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
def dim(a):
    if not type(a) == list:
        return []
    return [len(a)] + dim(a[0])
def column(matrix, i):
    return [row[i] for row in matrix]

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('/home/vonzeng/.ssh/google/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/vonzeng/.ssh/google/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    allExersises = sets.Set() 

    dbConn = sqlite3.connect("logicalProgression.db")
    dbc = dbConn.cursor()

    # Call the Sheets API
    SPREADSHEET_ID = '116FnJwq2tXo2z5xSBwo9_Qr_puKiFg2vWh8bh3sXBTM'
    sp = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sp.get('sheets', '')
    for s in sheets:
        dbConn.commit()
        
        sTitle = s.get("properties", {}).get("title")
        if sTitle == 'active' or sTitle =="helper":
            continue
        print("Import: "+s.get("properties", {}).get("title"))

        try:
            sessionType = sTitle.split(' ')[0]
            sDate = sTitle.split(' ')[2]
        except IndexError as e:
            continue
        date = int(time.mktime(datetime.datetime.strptime(sDate, "%Y/%m/%d").timetuple()))

        print("++"+sessionType+"++")
        print(str(date))
        dbc.execute('select date from sessions where date=?', (str(date),))
        dbSessions = dbc.fetchall()
        print(dbSessions)
        cDate = (date,)
        if cDate in dbSessions:
            print("Session already logged, skipping")
            continue
        
        durationRange = sTitle+'!duration'
        durationResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=durationRange).execute()
        durationResult = int(float(durationResult.get('values', [])[0][0]) * 60)
        print(durationResult)

        trainingDurationRange = sTitle+'!H8'
        trainingDurationResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=trainingDurationRange).execute()
        try:
            trainingDurationResult = int(float(trainingDurationResult.get('values', [])[0][0]) * 60)
        except IndexError:
            trainingDurationResult = 0
        print(trainingDurationResult)

        densityRange = sTitle+'!H9'
        densityResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=densityRange).execute()
        densityResult = int(float(densityResult.get('values', [])[0][0]))
        print(densityResult)

        sumRange = sTitle+'!L9'
        sumResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=sumRange).execute()
        sumResult = int(float(sumResult.get('values', [])[0][0]))
        print(sumResult)

        avgGradeRange = sTitle+'!N9'
        avgGradeResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=avgGradeRange).execute()
        avgGradeResult = int(float(avgGradeResult.get('values', [])[0][0]))
        print(avgGradeResult)

        avgSentRange = sTitle+'!N10'
        avgSentResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=avgSentRange).execute()
        avgSentResult = int(float(avgSentResult.get('values', [])[0][0]))
        print(avgSentResult)

        dbc.execute("insert into sessions(date,type,climbDuration,density,sum,avgGrade,avgSent,trainingDuration) values (?,?,?,?,?,?,?,?)",(date,sessionType,durationResult,densityResult,sumResult,avgGradeResult,avgSentResult,trainingDurationResult))
        dbc.execute('select ID from sessions where date=?', (str(date),))
        dbSessions = dbc.fetchone()[0]
        print(dbSessions)
        



        boulderRange = sTitle+'!boulderLog'
        boulderResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=boulderRange).execute()
        values = boulderResult.get('values', [])
        if not values:
            print('No data found.')
        else:
            grade = []
            tries = []
            gradeHelper = []
            sent = []
            steepness = []
            holdType = []
            comment = []
            dbData = []

            for row in values:
                try:
                    grade.append(int(row[0]))
                    tries.append(int(row[1]))
                    gradeHelper.append(grade[-1] * tries[-1])
                    sent.append(bool(row[2]))
                except IndexError as e:
                    continue
                except ValueError as e:
                    continue
                if len(row) == 6: # New log
                    steepness.append(row[3])
                    #take only the first hold type
                    holdType.append(row[4][0].lower())
                    comment.append(row[5])
                if len(row) == 4: # Old log
                    if row[3] == 'wu':
                        steepness.append('\\')
                        holdType.append('h')
                        comment.append('wu')
                    else:
                        try:
                            steep = row[3].split(' ',2)[0]
                            steepness.append(steep)
                            #take only the first hold type
                            hold = row[3].split(' ',2)[1][0]
                            holdType.append(hold)
                            com = row[3].split(' ',2)[2]
                            comment.append(com)
                        except IndexError as e:
                            steepness.append('\\')
                            holdType.append('h')
                            comment.append(row[3])
                if len(row) < 4: # Old incomplete log
                            steepness.append('\\')
                            holdType.append('h')
                            comment.append("")
                            

                
                steep = 0
                steepCount = 0
                if '\\' in steepness[-1]:
                    steep += 1
                    steepCount += 1
                if '|' in steepness[-1]:
                    steep += 2
                    steepCount +=1
                if '/' in steepness[-1]:
                    steep += 3
                    steepCount +=1
                if '-' in steepness[-1]:
                    steep += 4
                    steepCount +=1
                steepness[-1] = float(steep) / float(steepCount)

                print("%u %u %s %f %s %s"%(grade[-1], tries[-1], str(sent[-1]), steepness[-1], holdType[-1], comment[-1]))
                dbData.append((str(dbSessions), grade[-1], tries[-1], sent[-1], steepness[-1], holdType[-1], comment[-1]))
            dbc.executemany("insert into boulder(sessionID,grade,tries,sent,steepness,holdType,comment) values (?,?,?,?,?,?,?)",dbData)

                


        #Training
        if sessionType != "Strength":
            print("--"+sessionType+"--"+"Strength"+"--")
            continue
        strengthRange = sTitle+'!A10:C30'
        strengthResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=strengthRange).execute()
        values = strengthResult.get('values', [])
        exersises = []
        eSets = []
        reps = []
        dbData = []
        ex = column(values,0)
        for e in ex:
            if e != "":
                allExersises.add(e)
            try:
                dbc.execute("insert into exersises(name) values (?)",(e,))
            except sqlite3.IntegrityError:
                continue

        for row in values:
            try:
                if row[0] != "":
                    exersises.append(row[0])
                    eSets.append(int(row[1]))
                    reps.append(int(row[2]))
                    print("%s %u %u"%(exersises[-1],eSets[-1],reps[-1]))
                    dbc.execute("select ID from exersises where name = ?",(exersises[-1],))
                    exId = dbc.fetchone()[0]
                    dbData.append((str(dbSessions),exId,eSets[-1],reps[-1]))
            except IndexError as e:
                continue
        dbc.executemany("insert into training(sessionID,exersiseID,sets,reps) values (?,?,?,?)",dbData)


            #for row in values:
            #    # Print columns A and E, which correspond to indices 0 and 4.
            #      
            #    if str(row[0]) !="":
            #        print('%s' % (row[0]))
    dbConn.commit()
    dbConn.close()

if __name__ == '__main__':
    main()
