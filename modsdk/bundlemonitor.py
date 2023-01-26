# -*- coding: utf-8 -*-

import os
from tornado import ioloop
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from modsdk.settings import LV2_DIR

class EventHandler(FileSystemEventHandler):

    def __init__(self, monitor):
        super(EventHandler, self).__init__()
        self.monitor = monitor

    def on_created(self, event):
        if event.is_directory:
            self.monitor.add_watch(event.src_path)
        self.monitor.notify(event.src_path, event.event_type)

    def on_deleted(self, event):
        self.monitor.notify(event.src_path, event.event_type)

    def on_modified(self, event):
        self.monitor.notify(event.src_path, event.event_type)

class BundleMonitor:

    def __init__(self, callback):
        self.callback = callback
        self.observer = Observer()

    def monitor(self, bundle):
        self.clear()
        path = os.path.join(LV2_DIR, bundle)
        self.add_watch(path)
        self.observer.start()

    def add_watch(self, path):
        self.observer.schedule(EventHandler(self), path, recursive=True)

    def notify(self, pathname, event_type):
        self.callback()

    def clear(self):
        self.observer.stop()
        self.observer.join()
