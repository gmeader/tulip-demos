# cal.py
# wrap the lv calendar in a UIElement so it can live in a UIScreen
# by bwhitman, enhanced by gmeader
import tulip
from ui import UIElement, lv, lv_depad

class CalendarView(UIElement):
    def __init__(self, year, month, day, **kwargs):
        super().__init__(**kwargs)
        self.calendar = lv.calendar(self.group)
        self.calendar.set_today_date(year,month,day)
        self.calendar.set_showed_date(year,month)
        self.calendar.set_size(185,230)
        lv.calendar_header_dropdown(self.calendar) # enable month and year dropdown boxes
        lv.calendar_header_arrow(self.calendar) # enable next and previous buttons
        self.calendar.add_event_cb(calendar_cb,lv.EVENT.ALL, None)
        
        dates = [] # list for the extra highlighted dates
        adate = lv.calendar_date_t() # create a date struct
        adate.day = 10
        adate.month = 1
        adate.year = 2025
        dates.append(adate)
        
        bdate = lv.calendar_date_t()
        bdate.day = 30
        bdate.month = 1
        bdate.year = 2025
        dates.append(bdate)
        
        self.calendar.set_highlighted_dates(dates,len(dates))
        
                                                     
# callback when a date is clicked on the calendar
def calendar_cb(e):
    code = e.get_code() # what type of event
    if code == lv.EVENT.VALUE_CHANGED:
        obj = e.get_target_obj() # obj that fired the event - probably a button (date) on the calendar
        date = lv.calendar_date_t() # var to store date
        parent = obj.get_parent() # get calendar, not buttonmatrix
        if parent.get_pressed_date(date):
            event_label.set_text('Clicked: %04d-%02d-%02d'%(date.year, date.month, date.day))
            print('Clicked: %04d-%02d-%02d'%(date.year, date.month, date.day))
        
# label to display events - clicks on calendar dates        
class EventLabel(UIElement):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.label_obj = lv.label(self.group)
        self.set_text(text)
        
    def set_text(self, text):
        self.text = text
        self.label_obj.set_text(text)

# create the label as a global so we can change it from the callback                
event_label= EventLabel(text='EVENTS')

# start the app
def run(screen):
    year = 2025
    month = 10
    day = 20
    today = str(month)+ '/'+str(day)+'/'+str(year)
    screen.add(tulip.UILabel(text = today, fg_color=tulip.color(255,255,0),font=tulip.lv.font_montserrat_24),x=90,y=35)
    screen.add(CalendarView(year,month,day), pad_x=100, x=20, y=60)
    screen.add(event_label, x=50, y=310, pad_x=100)
    screen.present()







































































































































