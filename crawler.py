#!/usr/bin/python3

### user config

csvFilename='umsatz4.csv'
csvEncoding='ISO-8859-1'

### calculator class

class CsvCalculator:

    ### methods
    def __init__(self):
        self.monthlySum=[]
        self.monthlyPlus=[]
        self.monthlyMinus=[]
        self.sum=0
        self.sumPlus=0
        self.sumMinus=0

    def append_monthlySum(self,sumToAdd):
        self.monthlySum.append(sumToAdd)

    def append_monthlyPlus(self,sumToAdd):
        self.monthlyPlus.append(sumToAdd)
    
    def append_monthlyMinus(self,sumToAdd):
        self.monthlyMinus.append(sumToAdd)

    def getMonth(self,row):
        # syntax is dd.mm.yy
        date=row['Buchungstag']
        return int(date[3:5])

    def getYear(self,row):
        # syntax is dd.mm.yy
        date=row['Buchungstag']
        return int(date[6:])

    def getTransactionPerson(self,row):
        return row['Beguenstigter/Zahlungspflichtiger']

    def getTransactionValue(self,row):
        #turn decimal comma into decimal dot
        transaction=row['Betrag'].replace(',','.')
        return float(transaction)

    def updateSums(self,row):
        value=self.getTransactionValue(row)
        self.sum=self.sum+value
        if value<0:
            self.sumMinus=self.sumMinus+value
        else:
            self.sumPlus=self.sumPlus+value

    def updateMonthly(self, row):
        value=self.getTransactionValue(row)
        self.monthlySum.append(self.sum)
        self.monthlyPlus.append(self.sumPlus)
        self.monthlyMinus.append(self.sumMinus)

    def resetSums(self):
        self.sum=0
        self.sumPlus=0
        self.sumMinus=0

    ### variable initialisations



i=0

### main

calc = CsvCalculator()

#set up csv reader
import csv, codecs
with open(csvFilename, encoding=csvEncoding) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    checkMonth=True
    # read through the whole csv file
    for row in reader:
        if checkMonth == True:
            currentMonth=calc.getMonth(row)
            checkMonth = False
        #still in current month, get the transaction value
        if calc.getMonth(row)==currentMonth:
            calc.updateSums(row)
        #not in current month any more, write away last sum and start sum for the new month. check new month
        else:
            calc.updateMonthly(row)
            print(str(calc.monthlySum[-1]) + " - " + str(currentMonth))
            print(str(calc.monthlyPlus[-1]) + " <--> " + str(calc.monthlyMinus[-1]) + '\n')
            calc.updateSums(row)
            calc.resetSums()
            checkMonth=True
#update monthly afterwards, since it gets updated above only when a new month starts (not at end of file)
calc.updateMonthly(row)
print(str(calc.monthlySum[-1]) + " - " + str(currentMonth))
print(str(calc.monthlyPlus[-1]) + " <--> " + str(calc.monthlyMinus[-1]) + '\n')

for entry in calc.monthlySum:
    i=i+entry
print("total: ")
print(i)
