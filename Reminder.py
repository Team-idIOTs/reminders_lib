
class Reminder():
    '''

    Arguments
    task_name  = Name of the task this reminder is for
    days       = ['MON', 'TUES', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
    start_time = [hour, minute] (Military time)
    end_time   = [hour, minute] (Military time)
    interval   = [hour, minute] (Military time)

    '''
    def __init__(self, task_name, start_time, days, id, updated=True, end_time=None, interval=None):
        self.task_name = task_name
        self.start_time = start_time
        self.end_time = end_time
        self.interval = interval
        self.days = days
        self.id = id
        self.updated = updated

    def to_json(self):
        json_data = {
            'task_name' : self.task_name,
            'start_time': self.start_time,
            'end_time'  : self.end_time,
            'interval'  : self.interval,
            'days'      : self.days,
            'id'        : self.id,
            'updated'   : self.updated
        }
        return json_data

    @classmethod
    def from_dict(clss, data):
        return Reminder(data['task_name'], data['start_time'], data['days'], data['id'], data['updated'], data['end_time'], data['interval'])