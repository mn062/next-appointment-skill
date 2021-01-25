from mycroft import MycroftSkill, intent_file_handler
from datetime import datetime
import caldav
from caldav.elements import dav
import pytz

class NextAppointment(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('appointment.next.intent')
    def handle_appointment_next(self, message):
        self.loadCalendar()
        self.speak_dialog(self.getAppointment())
    
    def loadCalendar(self):
        with open('/home/mn062/pw.txt','r') as file:
             self.data = file.read().splitlines()

        self.username = self.data[0]
        self.password = self.data[1]

        self.url = "https://" + self.username + ":" + self.password + "@next.social-robot.info/nc/remote.php/dav"

        # open connection to calendar
        self.client = caldav.DAVClient(self.url)
        self.principal = self.client.principal()

        # get all available calendars (for this user)
        self.calendars = self.principal.calendars()

        # get first calendar
        self.calendar = self.calendars[0]

        # get all appointments in a spefcific time period (here: now - 01.01.2024)
        self.events_fetched = self.calendar.date_search(
            start = datetime.now(), end = datetime(2024, 1, 1), expand=True)

        # get name and start time of first appointment if there is one
        if self.events_fetched:
           self.summary = self.events_fetched[0].vobject_instance.vevent.summary.value
           self.dtstart = self.events_fetched[0].vobject_instance.vevent.dtstart.value

    def getAppointment(self):
        if not self.events_fetched:
           return "There is no upcoming appointment"
        else:
           return self.dtstart.strftime("Your next appointment is on %B %d, %Y at " + str(self.dtstart.hour+1) + ":%M %p and is entitled " + self.summary)
def create_skill():
    return NextAppointment()
