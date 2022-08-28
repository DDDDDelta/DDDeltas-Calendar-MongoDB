# This code is create by DDDelta for his own use
# do not copy or use any code without author's permission

import DATE
import TIME
import json
import texttable

timeUtil = TIME.timeUtil()
dateUtil = DATE.dateUtil()


class mainCalendar:

    def __init__(self):
        self.username = "DDDelta"
        self.password = "040806"

    def checkInputType(self,inp,typ):
        if typ == "str":
            try:
                str(inp)
                return True
            except:
                return False
        elif typ == "int":
            try:
                int(inp)
                return True
            except:
                return False
        elif typ == "float":
            try:
                float(inp)
                return True
            except:
                return False
        elif typ == "isoDate":
            try:
                dateUtil.convertIsoToDate(inp)
            except:
                return False
        elif typ == "bool":
            return inp.lower() in ["true","false","t","f"]
        elif typ == "strTime":
            return timeUtil.checkTimeValidation(inp)
        return False

    def convertInputType(self,inp,typ):
        if typ == "str":
            return str(inp)
        elif typ == "int":
            return int(inp)
        elif typ == "float":
            return float(inp)
        elif typ == "bool":
            if inp.lower() == "true" or inp.lower() == "t":
                return True
            if inp.lower() == "false" or inp.lower() == "f":
                return False
        else:
            return None

    def getInputFromCommandLine(self,typ,quote,para=None):
        inp = input(quote)
        if inp == "back":
            return "back"
        if self.checkInputType(inp,typ):
            if typ == "isoDate" or typ == "strTime":
                typ = "str"
            conv_input = self.convertInputType(inp,typ)
            if conv_input is True or conv_input is False:
                return conv_input
            if conv_input and (para is None or conv_input in para):
                return conv_input
            else:
                return "error"
        else:
            return "error"

    def operationSelection(self):
        parameter = ["add", "delete", "print","terminate"]
        print("select operation type")
        print("parameter: add, delete, print, terminate")
        inp = self.getInputFromCommandLine("str", "please select operation type:\n", parameter)
        while inp == "error":
            print("invalid input, please try again")
            print("parameter: add, delete, print, terminate")
            inp = self.getInputFromCommandLine("str", "please select operation type:\n", parameter)
        if inp == "add":
            print("====================================Operation Starts====================================")
            print("adding events")
            self.addingEvent()
        elif inp == "delete":
            print("====================================Operation Starts====================================")
            print("deleting event")
            self.deletingEvent()
        elif inp == "print":
            print("====================================Operation Starts====================================")
            print("printing calendar")
            self.printCalendar()
        elif inp == "terminate":
            raise SystemExit
        print("====================================Operation Ends====================================")
        return

    def datePreproccess(self,dates):
        para3 = ["this" + x.lower() for x in dateUtil.daysOWeek]
        if isinstance(dates,str):
            dates = [dates]
        for i in range(len(dates)):
            if dates[i] == "today":
                dates[i] = dateUtil.todayDate
            elif dates[i].lower() in para3:
                dates[i] = dateUtil.thisWeek[para3.index(dates[i])]
            else:
                try:
                    dateUtil.convertIsoToDate(dates[i])
                except:
                    return "error"
        return dates

    def repeatEventParameterPreproccess(self,inp):
        arr = inp.split(" ")
        # para1
        para1 = ["daily","weekly","monthly","yearly"]
        if arr[0] not in para1:
            print("parameter 1 is invalid")
            return "error"
        # para2
        try:
            arr[1] = int(arr[1])
        except:
            print("parameter 2 is invalid")
            return "error"
        # para3
        if "&" in arr[2]:
            dates = arr[2].split("&")
        else:
            dates = [arr[2]]
        dates = self.datePreproccess(dates)
        if dates == "error":
            print("parameter 3 is invalid")
            return "error"
        arr[2] = dates
        # para4
        time = True
        date = True
        try:
            dateUtil.convertIsoToDate(arr[3])
        except:
            date = False
        try:
            arr[3] = int(arr[3])
        except:
            time = False
        if not (time or date):
            print("parameter 4 is invalid")
            return "error"
        return arr

    def endTimePreprocess(self,inp,start):
        if inp.isnumeric() and start is not None:
            return start + int(inp)
        elif inp.lower() == "no" or inp.lower() == "n/a" or inp.lower() == "n":
            return start
        elif timeUtil.checkTimeValidation(inp) and timeUtil.getIntTime(inp) > start:
            return timeUtil.getIntTime(inp)
        elif timeUtil.checkDurationValidation(inp):
            return timeUtil.convertDurationToMinutes(inp) + start
        else:
            return "error"

    def getDictFromJson(self):
        file = open("event.json","r")
        try:
            ret = json.load(file)
        except:
            ret = {}
        finally:
            file.close()
        return ret

    def dumpDictToJson(self,dic):
        file = open("event.json", "w")
        try:
            json.dump(dic, file)
        except:
            print("unable to save")
        finally:
            file.close()
        return

    def register(self,eventDict):
        originalDict = self.getDictFromJson()
        if originalDict != {}:
            new = originalDict.copy()
            for key in eventDict:
                if key in new:
                    new[key].append(eventDict[key])
                else:
                    new[key] = [eventDict[key]]
        else:
            new = {}
            for key in eventDict:
                new[key] = [eventDict[key]]
        """
        for key in new:
            new[key].sort(key=lambda startTime: startTime[1])
        """
        self.dumpDictToJson(new)
        return

    def addingEvent(self):
        print("parameter: any string")
        inp1 = self.getInputFromCommandLine("str", "enter event name:\n")
        while inp1 == "error":
            print("invalid input, please try again")
            print("parameter: any string")
            inp1 = self.getInputFromCommandLine("str", "enter event name:\n")
        if inp1 == "back":
            return
        else:
            name = inp1
        print("parameter: bool")
        inp2 = self.getInputFromCommandLine("bool", "if the event repeats:\n")
        while inp2 == "error":
            print("invalid input, please try again")
            print("parameter: bool")
            inp2 = self.getInputFromCommandLine("bool", "if the event repeats:\n")
        if inp2 == "back":
            return
        else:
            repeat = inp2
        allDates = []
        if repeat == True:
            print("parameter:mode(daily/weekly/monthly/yearly) frequency(any integer)")
            print("start_date(XXXX-XX-XX/today/this[weekday] end_date(XXXX-XX-XX) OR repeat_time(any int)")
            inp3 = self.getInputFromCommandLine("str", "enter values following parameters:\n")
            if inp3 == "back":
                return
            procInp3 = self.repeatEventParameterPreproccess(inp3)
            while procInp3 == "error":
                print("invalid input")
                print("parameter:mode(daily/weekly/monthly/yearly) frequency(any integer)")
                print("start_date(XXXX-XX-XX/today/this[weekday] end_date(XXXX-XX-XX) OR repeat_time(any int)")
                inp3 = self.getInputFromCommandLine("str", "enter values following parameters:\n")
                if inp3 == "back":
                    return
                procInp3 = self.repeatEventParameterPreproccess(inp3)
            for date in procInp3[2]:
                if isinstance(procInp3[-1],int):
                    dates = dateUtil.getRepeatedDates(procInp3[0],procInp3[1],date,time=procInp3[-1])
                else:
                    dates = dateUtil.getRepeatedDates(procInp3[0],procInp3[1],date,end=procInp3[-1])
                for date in dates:
                    allDates.append(date)
        else:
            print("parameter: XXXX-XX-XX/today/this[weekday]")
            inp3 = self.getInputFromCommandLine("str", "enter date:\n")
            if inp3 == "back":
                return
            inp3 = self.datePreproccess([inp3])
            while inp3 == "error":
                print("invalid input")
                print("parameter: XXXX-XX-XX/today/this[weekday]")
                inp3 = self.getInputFromCommandLine("str", "enter date:\n")
                if inp3 == "back":
                    return
                inp3 = self.datePreproccess([inp3])
            allDates.append(inp3[0])
        allDates = list(set(allDates))
        eventDict = {}
        print("parameter: XX:XX(time)")
        inp4 = self.getInputFromCommandLine("strTime", "start time:\n")
        while inp4 == "error":
            print("invalid input")
            print("parameter: XX:XX(time)")
            inp4 = self.getInputFromCommandLine("strTime", "start time:\n")
        if inp4 == "back":
            return
        else:
            startTime = timeUtil.getIntTime(inp4)
        print("parameter: XX:XX(time), XhXmin(duration), anyInt(mins)")
        inp5 = self.getInputFromCommandLine("str", "end time:\n")
        if inp5 == "back":
            return
        inp5 = self.endTimePreprocess(inp5,startTime)
        while inp5 == "error":
            print("invalid input")
            print("parameter: XX:XX(time), XhXmin(duration), anyInt(mins)")
            inp5 = self.getInputFromCommandLine("str", "end time:\n")
            if inp5 == "back":
                return
            inp5 = self.endTimePreprocess(inp5,startTime)
        endTime = inp5
        for date in allDates:
            eventDict[date] = [name,startTime,endTime]
        print("you are adding " + str(len(eventDict)) + " events")
        print("event name: " + name)
        for date in allDates:
            print("dates: " + date)
        print("time: From " + timeUtil.getStrTime(startTime) + " to " + timeUtil.getStrTime(endTime))
        print(eventDict)
        self.register(eventDict)

    def modifiedGetInputFromCommandLine(self,typ,quote,para=None):
        ret = self.getInputFromCommandLine(typ,quote,para=para)
        if ret == "error":
            raise ValueError()
        else:
            return ret

    def loopedModifiedGetInputFromCommandLine(self,typ,quote,paraStr,para=None):
        inp = None
        while inp is None:
            try:
                print("parameter: " + paraStr)
                inp = self.modifiedGetInputFromCommandLine(typ, quote, para)
            except ValueError:
                print("invalid input, please try again")
        return inp

    def deleteWithDate(self):
        eventDict = self.getDictFromJson()
        dates = self.loopedModifiedGetInputFromCommandLine("str","enter date: \n","any date",para=None)
        for date in dates:
            if date in eventDict:
                eventDict.pop(date)
                print("all events in " + date + " are removed")
            else:
                print("there is event registered under specified dates or invalid input")
        self.dumpDictToJson(eventDict)
        return

    def setKeyDateToEventName(self,eventDict):
        transformed = {}
        for date in eventDict:
            for event in eventDict[date]:
                eventName,eventStart,eventEnd = event
                if eventName in transformed:
                    transformed[eventName].append([date,eventStart,eventEnd])
                else:
                    transformed[eventName] = [[date,eventStart,eventEnd]]
        return transformed

    def setKeyEventNameToDate(self,transEventDict):
        new = {}
        for eventName in transEventDict:
            for timeInfo in transEventDict[eventName]:
                date,eventStart,eventEnd = timeInfo
                if date in new:
                    new[date].append([eventName,eventStart,eventEnd])
                else:
                    new[date] = [eventName,eventStart,eventEnd]
        return new

    def deleteWithEventName(self):
        transEventDict = self.setKeyDateToEventName(self.getDictFromJson())
        allEvents = [x for x in transEventDict]
        table1 = texttable.Texttable()
        table1.set_cols_align(["c","c"])
        table1.set_cols_valign(["m","m"])
        table1.header(["number","event names"])
        for i in range(len(allEvents)):
            table1.add_row([i,allEvents[i]])
        print(table1.draw())
        num = None
        while num is None:
            try:
                print("parameter: any integer")
                num = input("select event name\n")
                if num == "back":
                    return
                num = int(num)
                if num > len(allEvents)-1 or num < -1:
                    num = None
                    raise ValueError
            except Exception:
                print("invalid input, please try again")
        selectedEvent = allEvents[num]
        allTime = {}
        for timeInfo in transEventDict[selectedEvent]:
            date, eventStart, eventEnd = timeInfo
            eventStart = timeUtil.getStrTime(eventStart)
            eventEnd = timeUtil.getStrTime(eventEnd)
            timeDuration = eventStart + "-" + eventEnd
            if timeDuration not in allTime:
                allTime[timeDuration] = 1
        allTime = [x for x in allTime]
        table2 = texttable.Texttable()
        table2.set_cols_align(["c", "c", "c"])
        table2.set_cols_valign(["m", "m", "m"])
        table2.header(["number", "start time", "end time"])
        counter = 0
        for time in allTime:
            time1, time2 = time.split("-")
            table2.add_row([counter, time1, time2])
            counter += 1
        print("all time info for " + selectedEvent)
        print(table2.draw())
        num = None
        while num is None:
            try:
                print("parameter: any integer")
                num = input("select time\n")
                if num == "back":
                    return
                num = int(num)
                if num > len(allTime)-1 or num < -1:
                    num = None
                    raise ValueError
            except Exception:
                print("invalid input, please try again")
        startTime, endTime = allTime[num].split("-")
        startTime, endTime = timeUtil.getIntTime(startTime), timeUtil.getIntTime(endTime)
        selectedTime = [startTime, endTime]
        newTime = []
        for time in transEventDict[selectedEvent]:
            if not (time[1] == selectedTime[0] and time[2] == selectedTime[1]):
                newTime.append(time)
        transEventDict[selectedEvent] = newTime
        finalEventDict = self.setKeyEventNameToDate(transEventDict)
        self.dumpDictToJson(finalEventDict)
        return

    def deleteEventsInOneDay(self):
        print("deleting stuff")
        return

    def deletingEvent(self):
        parameter = ["date", "eventName","cleanUp","eventsInOneDay"]
        inp1 = None
        while inp1 is None:
            try:
                print("parameter: date, eventName, cleanUp, eventsInOneDay")
                inp1 = self.modifiedGetInputFromCommandLine("str","select operation type: \n",parameter)
            except ValueError:
                print("invalid input, please try again")
        if inp1 == "back":
            return
        elif inp1 == "date":
            self.deleteWithDate()
        elif inp1 == "eventName":
            self.deleteWithEventName()
        elif inp1 == "cleanUp":
            self.cleanUp()
        elif inp1 == "eventsInOneDay":
            self.deleteEventsInOneDay()
        return

    def printCalendar(self):
        calendarDict = self.getDictFromJson()
        inp = None
        while inp is None:
            try:
                print("parameter: any date")
                inp = input("enter a date:\n")
                if inp == "back":
                    return
                dateUtil.convertIsoToDate(inp)
                if inp not in calendarDict:
                    print("no event registered under specified date")
                    raise ValueError()
            except (ValueError, KeyError):
                inp = None
                print("invalid input, please try again")
        day = calendarDict[inp]
        table = texttable.Texttable()
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["start time", "end time", "event name"])
        for event in day:
            table.add_row([timeUtil.getStrTime(event[1]), timeUtil.getStrTime(event[2]), event[0]])
        print("========================================Calendar Starts========================================")
        print(table.draw())
        print("=========================================Calendar Ends=========================================")
        return


    def cleanUp(self):
        today = dateUtil.convertIsoToDate(dateUtil.todayDate)
        eventDict = self.getDictFromJson()
        newDict = eventDict.copy()
        for key in eventDict:
            if dateUtil.convertIsoToDate(key) < today:
                newDict.pop(key)
                print("removed events from past: " + key)
        confirm = input("confirm clearing past events?\nenter no to cancel operation\n")
        if confirm == "no":
            return
        self.dumpDictToJson(newDict)

    def run(self):
        while True:
            try:
                self.operationSelection()
            except SystemExit:
                input("press any key to end")
                break
            except Exception:
                print("============================================warning============================================")
                print("program ran into an error")
                print("============================================warning============================================")

if __name__ == '__main__':
    calendar = mainCalendar()
    calendar.run()