import threading

class X(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.flag = 1 
    self.cond = threading.Condition()

  def run(self):
    self.cond.acquire()
    self.condition.wait(300)
    while self.flag == 1:
      ... 
      self.cond.release()
      self.cond.acquire()
      self.condition.wait(300)

...
x.flag = 0
x.cond.acquire()
x.cond.notify()
x.cond.release()