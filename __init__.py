from mycroft import MycroftSkill, intent_file_handler


class NextAppointment(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('appointment.next.intent')
    def handle_appointment_next(self, message):
        self.speak_dialog('appointment.next')


def create_skill():
    return NextAppointment()

