import sys
import os
import subprocess
import datetime


filename_normal = "hackday_normal.log"
filename_deployed = "hackday_deployed.log"

filename = filename_normal
if len(sys.argv) > 1 and sys.argv[1] in ["deployed", "deploy", "d"]:
	filename = filename_deployed

if not os.path.isfile(filename):
	with open(filename, 'w') as writefile:
		writefile.write("index;")
		writefile.write("time;")
		writefile.write("cpu-0-idle;cpu-1-idle;")
		writefile.write("free-mem;")
		writefile.write("rxpck/s;txpck/s;")
		
		writefile.write("\n")

line_count = sum(1 for line in open(filename))

with open(filename, 'a') as appendfile:
	
	#================
	# index
	#=================
	appendfile.write(str(line_count)+";")

	#================
	# datetime.now()
	#=================
	appendfile.write(str(datetime.datetime.now())+";")


	#=================
	# mpstat
	#=================
	cmd = subprocess.Popen("mpstat -P ALL", shell=True, stdout=subprocess.PIPE)
	
	counter = 0
	for line in cmd.stdout:
		counter += 1
		if counter in [5, 6]:
			values = line.split()
			appendfile.write(values[12]+";")


	#=================
	# /proc/meminfo
	#=================
	cmd = subprocess.Popen("cat /proc/meminfo", shell=True, stdout=subprocess.PIPE)

	counter = 0
	for line in cmd.stdout:
		counter += 1
		if counter == 2:
			values = line.split()
			appendfile.write(values[1]+";")
			break


	#=================
	# sar -n
	#=================
	cmd = subprocess.Popen("sar -n DEV 1 1", shell=True, stdout=subprocess.PIPE)

	counter = 0
	for line in cmd.stdout:
		counter += 1
		if counter == 8:
			values = line.split()
			appendfile.write(values[2]+";"+values[3]+";")
			break
	
	
	#=================
	# end logging
	#=================
	appendfile.write("\n")


#=================
# output
#=================
with open(filename, 'r') as readfile:
	for line in readfile:
		sys.stdout.write(line)
