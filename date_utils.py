# This code is create by DDDelta for his own use
# do not copy or use any code without author's permission

import datetime


class DateUtil:
    def __init__(self):
        self.todayDate = self.getTodayDate()
        self.todayYear, self.todayMonth, self.todayDay = self.todayDate.split("-")
        self.daysOWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.intToWeekdayDict = {}
        self.weekdayToIntDict = {}
        for i in range(len(self.daysOWeek)):
            self.intToWeekdayDict[i+1] = self.daysOWeek[i].lower()
            self.weekdayToIntDict[self.daysOWeek[i].lower()] = i+1
        self.thisWeek = self.getWeekFromDate(self.todayDate)

    def getTodayDate(self):
        return datetime.date.today().isoformat()

    def convertIsoToArray(self,isoDate):
        return isoDate.split("-")

    def convertIsoToDate(self,isoDate):
        year, month, day = isoDate.split("-")
        return datetime.date(int(year), int(month), int(day))

    def getDayOWeek(self,isoDate,typ):
        if typ == "int":
            return self.convertIsoToDate(isoDate).isoweekday()
        if typ ==  "str":
            return self.intToWeekdayDict[self.convertIsoToDate(isoDate).isoweekday()]

    def getDateOWeekFromAnotherDate(self,isoDate,target):
        if isinstance(target, str):
            intTarget = self.weekdayToIntDict[target.lower()]
        else:
            intTarget = target
        intInit = self.getDayOWeek(isoDate,"int")
        initDate = self.convertIsoToDate(isoDate)
        delta = self.getTimeDelta("daily",intTarget-intInit)
        targetDate = initDate + delta
        return targetDate.isoformat()

    def getWeekFromDate(self,isoDate):
        week = []
        for day in self.daysOWeek:
            week.append(self.getDateOWeekFromAnotherDate(isoDate,day))
        return week

    def getTimeDelta(self,mode,freq):
        mode = mode.lower()
        tDelta = datetime.timedelta()
        if mode == "daily":
            tDelta = datetime.timedelta(days=freq)
        elif mode == "weekly":
            tDelta = datetime.timedelta(weeks=freq)
        return tDelta

    def increaseByMonths(self,date,freq):
        year,month,day=date.year,date.month,date.day
        if month+freq <= 12:
            return datetime.date(year,month+freq,day)
        else:
            return datetime.date(year+1,month+freq-12,day)

    def getRepeatedDates(self,mode,freq,start,end=None,time=0):
        mode = mode.lower()
        ret = []
        startDate = self.convertIsoToDate(start)
        delta = self.getTimeDelta(mode,freq)
        currDate = startDate
        if mode != "monthly" and mode != "yearly":
            if end == None and time != 0:
                for i in range(time):
                    currDate = startDate + delta*i
                    ret.append(currDate.isoformat())
            elif end != None and time == 0:
                endDate = self.convertIsoToDate(end)
                while currDate < endDate:
                    ret.append(currDate.isoformat())
                    currDate = currDate + delta
                if currDate == endDate:
                    ret.append(currDate.isoformat())
                else:
                    print("end date provided is not exact, dates later than the specified are removed")
        elif mode == "monthly":
            if end == None and time != 0:
                for i in range(time):
                    ret.append(currDate.isoformat())
                    currDate = self.increaseByMonths(currDate,freq)
            elif end != None and time == 0:
                endDate = self.convertIsoToDate(end)
                while currDate < endDate:
                    ret.append(currDate.isoformat())
                    currDate = self.increaseByMonths(currDate,freq)
                if currDate == endDate:
                    ret.append(currDate.isoformat())
                else:
                    print("end date provided is not exact, dates later than the specified are removed")
        elif mode == "yearly":
            if end == None and time != 0:
                for i in range(time):
                    ret.append(currDate.isoformat())
                    currDate = currDate.replace(year=currDate.year+freq)
            elif end != None and time == 0:
                endDate = self.convertIsoToDate(end)
                while currDate < endDate:
                    ret.append(currDate.isoformat())
                    currDate = currDate.replace(year=currDate.year+freq)
                if currDate == endDate:
                    ret.append(currDate.isoformat())
                else:
                    print("end date provided is not exact, dates later than the specified are removed")
        return ret



if __name__ == '__main__':
    d = dateUtil()