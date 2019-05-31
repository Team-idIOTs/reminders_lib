from crontab import CronTab
from Reminder import *

class ReminderScheduler():

    def __init__(self, user="pi", ttsdir="/home/pi/Design_Competition/raspi_reminders/ttsscript.py"):
        self.cron = CronTab(user=user)
        self.ttsdir=ttsdir

    def schedule_task(self, task):
        for key, reminder in task.reminders.items():
            if (reminder.updated):
                self.schedule_reminder(reminder)

    def schedule_reminder(self, reminder):
            # Check if it already exists.
            comment = str(reminder.task_name + str(reminder.id))
            found = False
            for job in self.cron:
                if (job.comment == comment):
                    found = True

            if (found == False):
                # If it has an end time, then schedule a bunch of jobs
                if (reminder.end_time == None):
                    end_hour = 22
                    end_min  = 59
                else :
                    end_hour = reminder.end_time[0]
                    end_min  = reminder.end_time[1]

                hour = reminder.start_time[0]
                min  = reminder.start_time[1]

                # If it is not at the end yet, then keep scheduling
                while(end_hour > hour or ((end_hour == hour) and (end_min > min))):
                    job = self.cron.new(command='python3 ' + self.ttsdir + " /home/pi/sounds/" + reminder.task_name.replace(" ", "") \
                                              +  " " , comment=comment)
                    job.hour.on(hour)
                    job.minute.on(min)
                    job.dow.on(*reminder.days)

                    # Increment hour and min

                    # Add minutes
                    min = min + reminder.interval[1]
                    if (min > 59):
                        min = min - 60
                        hour = hour + 1
                    hour = hour + reminder.interval[0]
                    if (hour > 23):
                        break

            self.cron.write()
