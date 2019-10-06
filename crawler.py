#!/usr/bin/python3

### user config

csvFilename='umsatz4.csv'
csvEncoding='ISO-8859-1'

### functions

def getMonth(row):
    # syntax is dd.mm.yy
    date=row['Buchungstag']
    return int(date[3:5])

def getYear(row):
    # syntax is dd.mm.yy
    date=row['Buchungstag']
    return int(date[6:])

def getTransactionPerson(row):
    return row['Beguenstigter/Zahlungspflichtiger']

def getTransactionValue(row):
    #turn decimal , into decimal .
    transaction=row['Betrag'].replace(',','.')
    return float(transaction)

def updateSums(row,sum,sumPlus,sumMinus):
    value=getTransactionValue(row)
    sum[0]=sum[0]+value
    if value<0:
        sumMinus[0]=sumMinus[0]+value
    else:
        sumPlus[0]=sumPlus[0]+value

def updateMonthly(row,sum,sumPlus,sumMinus,m,mp,mm):
    value=getTransactionValue(row)
    m.append(sum[0])
    mp.append(sumPlus[0])
    mm.append(sumMinus[0])

def resetSums(sum,sumPlus,sumMinus):
    sum[0]=0
    sumPlus[0]=0
    sumMinus[0]=0

### variable initialisations

sum=[]
sum.append(0)
sumPlus=[]
sumPlus.append(0)
sumMinus=[]
sumMinus.append(0)
monthlySum=[]
monthlyPlus=[]
monthlyMinus=[]
i=0

### main

#set up csv reader
import csv, codecs
with open(csvFilename, encoding=csvEncoding) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    checkMonth=True
    # read through the whole csv file
    for row in reader:
        if checkMonth == True:
            currentMonth=getMonth(row)
            checkMonth = False
        #still in current month, get the transaction value
        if getMonth(row)==currentMonth:
            updateSums(row,sum,sumPlus,sumMinus)
            #sum = sum+getTransactionValue(row)
        #not in current month any more, write away last sum and start sum for the new month. check new month
        else:
            #monthlySum.append(sum)
            updateMonthly(row,sum,sumPlus,sumMinus,monthlySum,monthlyPlus,monthlyMinus)
            print(str(monthlySum[-1]) + " - " + str(currentMonth))
            print(str(monthlyPlus[-1]) + " <--> " + str(monthlyMinus[-1]) + '\n')
            updateSums(row,sum,sumPlus,sumMinus)
            resetSums(sum,sumPlus,sumMinus)
            #sum=getTransactionValue(row)
            checkMonth=True
updateMonthly(row,sum,sumPlus,sumMinus,monthlySum,monthlyPlus,monthlyMinus)
#monthlySum.append(sum)
print(str(monthlySum[-1]) + " - " + str(currentMonth))
print(str(monthlyPlus[-1]) + " <--> " + str(monthlyMinus[-1]) + '\n')
            
for entry in monthlySum:
    i=i+entry
print("total: ")
print(i)
