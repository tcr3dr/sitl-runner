import os
import dronekit
import time
import re
from dronekit_sitl import SITL

s = SITL(path=os.path.join(os.path.dirname(__file__), 'build/out/apm'))
s.launch([], wd=os.path.join(os.path.dirname(__file__), 'build/test'))

time.sleep(.5)
vehicle = dronekit.connect('tcp:127.0.0.1:5760')
for line in open(os.path.join(os.path.dirname(__file__), 'build/out/default.parm')):
    if re.match(r'^\s*#', line):
        continue
    try:
        pname, pvalue = line.split()
        vehicle.parameters.set(pname, float(pvalue), retries=0)
    except Exception as e:
        import traceback
        traceback.print_exc()
vehicle.flush()
time.sleep(10)
vehicle.close()
s.p.kill()

print 'eeprom generated.'