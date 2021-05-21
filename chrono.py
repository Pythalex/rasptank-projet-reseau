import threading
import time

class Chrono(threading.Thread):
    
    def start():

        self.start = time.time()

        while time.time() - self.start() > 0.001:
