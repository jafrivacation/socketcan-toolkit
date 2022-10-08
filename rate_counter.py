import time
class RateCounter:
 def __init__(self,window=1.0): self.t=[]; self.w=window
 def tick(self): now=time.monotonic(); self.t=[x for x in self.t if now-x<self.w]; self.t.append(now)
 def rate(self): return len(self.t)
