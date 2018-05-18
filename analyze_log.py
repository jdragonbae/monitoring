import sys, os
import pandas
import numpy
import datetime
from scipy import stats


number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]
servers = ['10.41.2.31', '10.41.1.25', '10.41.5.49', '10.41.2.41', '10.41.0.232', '10.41.5.67', '10.41.2.84', '10.41.0.162', '10.41.5.74']

for server in servers:
	if os.path.isfile("hackday_logs/"+server+".log"):
		df = pandas.read_csv("hackday_logs/"+server+".log", sep=';')

		#=================
		# use data from since 1 hour ago
		#=================
		df['time'] = pandas.to_datetime(df['time'])
		start_time = datetime.datetime.now() - datetime.timedelta(hours = 1)
		end_time = datetime.datetime.now()
		mask = (df['time'] > start_time) & (df['time'] <= end_time)
		df = df.loc[mask]

		print df.describe()

		columns = df.columns.tolist()
		for column in columns:
			if column not in number_type_logs:
				df.drop(column, axis=1, inplace=True)
		
		if df.shape[0] < 300:
			print "Less than 300 logs have been recorded in the past hour. Results might not be reliable."

		for col in df.columns.tolist():
			
			#=================
			# mean vs stdev
			#=================
			if (col in ['rxpck/s', 'txpck/s']):
				if (df[col].std() > df[col].mean()*5):
					print "possible issue in: server "+server+" col "+col
			else:
				if (df[col].std() > df[col].mean()/10):
					print "possible issue in: server "+server+" col "+col
			
			#=================
			# percent usage
			#=================
			if (col in ['cpu-0-idle', 'cpu-1-idle']):
				if (df[col].mean() > 75):
					print "possible issue in: server "+server+" col "+col
			elif (col == 'mem-info'):
				if (df[col].mean() < 3000000):
					print "possible issue in: server "+server+" col "+col
		print "============================================"
