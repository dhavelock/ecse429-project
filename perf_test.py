import psutil
import subprocess
import time
import datetime

f = open("perf_test_output.csv", "w+")
p = subprocess.Popen(["pytest","performance"])

f.write('time,cpu %,availble mem. %\n')
while p.poll() is None:
    f.write(str(datetime.datetime.now().isoformat()) + ',' + str(psutil.cpu_percent()) + ',' + str(psutil.virtual_memory().percent) + '\n')
    time.sleep(1)

f.close()
print('Performance tests complete')