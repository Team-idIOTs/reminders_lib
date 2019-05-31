from Reminder import *
from gtts import gTTS
import os

class Task():


    def __init__(self, type, name, audio, updated=True, reminders={}):
        self.type = type
        self.name = name
        self.audio = audio
        self.reminders = reminders
        self.updated = updated


    def add_reminder(self, start_time,  days, end_time=None, interval=None):
        id = len(self.reminders)
        self.reminders[id] = Reminder(self.name, start_time, days, id, updated = True, end_time = end_time, interval = interval)

    def update_reminder(self, id, **kwargs):
        self.reminders[id].update(**kwargs)

    def to_json(self):
        json_str = {
            'type' : self.type,
            'name' : self.name,
            'audio': self.audio,
            'updated': self.updated
        }

        json_str['reminders'] = {}
        for key, value in self.reminders.items():
            json_str['reminders'][key] = value.to_json()
        return json_str

    def make_audio(self, storage):
        tts = gTTS(self.audio)
        file_name = self.name.replace(" ", "") + ".mp3"
        tts.save(file_name)
        storage.child(file_name).put(file_name)
        os.remove(file_name)

    def get_audio_name(self):
        return self.name.replace(" ", "") + ".mp3"


    @classmethod
    def from_dict(clss, data):
        reminders = {}

        # If it is coming from firebase
        if (type(data['reminders']) == list):
            for i in range(len(data['reminders'])):
                reminders[i] = Reminder.from_dict(data['reminders'][i])
        else:
            for key, val in data['reminders'].items():
                reminders[key] = Reminder.from_dict(val)
        return Task(data['type'], data['name'], data['audio'], data['updated'], reminders)


    def to_firebase(self, db):
        self.updated = True
        db.child(self.name).set(self.to_json())