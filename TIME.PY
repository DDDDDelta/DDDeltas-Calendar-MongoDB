# This code is create by DDDelta for his own use
# do not copy or use any code without author's permission


class timeUtil:
    def __init__(self):
        self.minute = 60
        self.hour = 24
        self.day = 60*24

    def checkTimeValidation(self,time):
        if isinstance(time,str):
            try:
                hour, minute = time.split(":")
                hour = int(hour)
                minute = int(minute)
            except:
                return False
            if hour >= 24 or hour < 0 or minute >= 60 or minute < 0:
                return False
            else:
                return True
        elif isinstance(time,int):
            if time >= self.day or time < 0:
                return False
            else:
                return True
        else:
            return False

    def checkDurationValidation(self,duration):
        h = False
        min = False
        if "h" in duration:
            h = True
        if "min" in duration:
            min = True
        if not (h or min):
            return False
        elif h and not min:
            if duration.replace("h","").isnumeric() and duration.count("h") == 1 and duration[-1] == "h":
                return True
            else:
                return False
        elif not h and min:
            if duration.replace("min","").isnumeric() and len(duration)-len(duration.replace("min","")) == 3 and duration[-1] == "n":
                return True
            else:
                return False
        elif h and min:
            aDuration = duration.replace("min","").replace("h","")
            if aDuration.isnumeric() and len(duration) - len(aDuration) == 4 and duration[-1] == "n":
                h,m = duration.strip("min").split("h")
                if h is not None and m is not None and int(m) < 60:
                    return True
                else:
                    return False
            else:
                return False

    def getIntTime(self,strTime):
        hour,minute = strTime.split(":")
        return int(hour)*60 + int(minute)

    def getStrTime(self,intTime):
        minute = intTime % 60
        hour = int((intTime - minute)/60)
        if minute < 10:
            minute = "0" + str(minute)
        if hour < 10:
            hour = "0" + str(hour)
        return str(hour) + ":" + str(minute)

    def getHour(self,time,typ):
        if not isinstance(time,int):
            intTime = self.getIntTime(time)
        else:
            intTime = time
        hour = int(intTime/60)
        if typ == "int":
            return hour
        else:
            if hour < 10:
                return "0" + str(hour)
            else:
                return str(hour)

    def getMinute(self,time,typ):
        if not isinstance(time,int):
            intTime = self.getIntTime(time)
        else:
            intTime = time
        minute = int(intTime%60)
        if typ == "int":
            return minute
        else:
            if minute < 10:
                return "0" + str(minute)
            else:
                return str(minute)

    def convertDurationToMinutes(self,duration):
        h = False
        min = False
        if "h" in duration:
            h = True
        if "min" in duration:
            min = True
        d = duration.strip("min")
        if h and min:
            hour,minute = d.split("h")
            return int(minute) + int(hour)*60
        elif h and not min:
            return int(d.strip("h"))*60
        else:
            return int(d)

    def convertMinutesToDuration(self,minutes):
        hour = self.getHour(minutes,"int")
        minute = self.getMinute(minutes,"int")
        if minute == 0:
            return str(hour) + "min"
        elif hour == 0:
            return str(minute) + "min"
        else:
            return str(hour) + "h" + str(minute) + "min"

    def getDuration(self,time1,time2):
        if isinstance(time1,str):
            intTime1 = self.getIntTime(time1)
        else:
            intTime1 = time1
        if isinstance(time2,str):
            intTime2 = self.getIntTime(time2)
        else:
            intTime2 = time2
        mins = abs(intTime2-intTime1)
        ret = self.convertMinutesToDuration(mins)
        return ret



if __name__ == '__main__':
    t = timeUtil()
