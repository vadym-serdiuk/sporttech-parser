import json
import logging
from sched import scheduler

import parsers

log = logging.getLogger('schedule')


class Schedule:
    def __init__(self, config):
        self.s = scheduler()
        self.config = config
        self.schedule_config = config.get('schedule', {})
        self.add_task()
        log.info('Scheduler started with interval')
        self.s.run()

    def add_task(self, interval=0):
        self.s.enter(interval, 1, self.task)

    def task(self):
        data = parsers.parse(self.config)

        with open(self.schedule_config.get('filename', 'output.json'), 'w') as fp:
            json.dump(data, fp)
        self.add_task(self.schedule_config.get('interval', 5) * 60)

