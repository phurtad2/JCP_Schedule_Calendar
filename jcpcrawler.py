import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from pyvirtualdisplay import Display


def string_date(date):
    month = date.month if date.month >=10 else str("0") + str(date.month)
    day = date.day if date.day >=10 else str("0") + str(date.day)
    return "%s-%s-%s" %(date.year, month, day)

def twenty_four(t):
    if 'a' in t:
        if "12" in t:
            return t.replace("12", "00", 1).strip('a')
        else:
            return t.strip('a')
    else:
        if "12" in t:
            return t.replace("12", "12", 1).strip('p')
        elif "01" in t:
            return t.replace("01", "13", 1).strip('p')
        elif "02" in t:
            return t.replace("02", "14", 1).strip('p')
        elif "03" in t:
            return t.replace("03", "15", 1).strip('p')
        elif "04" in t:
            return t.replace("04", "16", 1).strip('p')
        elif "05" in t:
            return t.replace("05", "17", 1).strip('p')
        elif "06" in t:
            return t.replace("06", "18", 1).strip('p')
        elif "07" in t:
            return t.replace("07", "19", 1).strip('p')
        elif "08" in t:
            return t.replace("08", "20", 1).strip('p')
        elif "09" in t:
            return t.replace("09", "21", 1).strip('p')
        elif "10" in t:
            return t.replace("10", "22", 1).strip('p')
        elif "11" in t:
            return t.replace("11", "23", 1).strip('p')


def url_string(date):
        month = date.month if date.month >=10 else str("0") + str(date.month)
        day = date.day if date.day >=10 else str("0") + str(date.day)
        return "%s%s%s" %( date.year, month, day)

def next_week(date):
    return "https://wmwbwb200.jcpenney.com:7107/etm/time/timesheet/etmTnsWeek.jsp?NEW_START_DATE=%s&SELECTED_DATE=2016053" % url_string(date)

def week_schedules(n):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.get("https://wmwbwb200.jcpenney.com:7107")
    assert "ETM Login" in driver.title
    dayurl = "https://wmwbwb200.jcpenney.com:7107/etm/time/timesheet/etmTnsDay.jsp?date="

    d = datetime.datetime.now()
    weekurl = "https://wmwbwb200.jcpenney.com:7107/etm/time/timesheet/etmTnsWeek.jsp?NEW_START_DATE=%s&SELECTED_DATE=20160531" % url_string(d)

    #d = now + datetime.timedelta(days=14)

    #elem = driver.find_element_by_xpath('/html/body/div[4]/div[2]/table/tbody/tr/td/table/tbody/tr/td/div/div[4]/table/tbody/tr/td/div[3]/div/div/table/tbody/tr/td/div/div/div/div/form[1]/div[2]/table/tbody/tr/td/div/div/table/tbody/tr[2]/td[2]')
    username = ""
    password = ""
    elem = driver.find_element_by_name("login")
    elem.send_keys(username)
    elem = driver.find_element_by_name("password")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    time.sleep(2)

    weekly = {}
    for i in range(1,n + 1):
        driver.get(weekurl)
        soup = bs(driver.page_source, 'html.parser')
        shift = soup.find_all("td", {"height":"200px", "valign":"middle" })
        for s in shift:
            add = s.find("div",{"class":"calendarTextShiftTime"})
            if add == None:
                pass
            else:
                for t in add.find("span"):
                    weekly[string_date(d)] = (twenty_four(t.string), twenty_four(t.find_next("span").string))
            d += datetime.timedelta(days=1)
        weekurl = next_week(d)


    driver.quit()
    display.stop()
    return weekly
