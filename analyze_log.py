import sys, os
import pandas
import numpy
from scipy import stats


number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]
servers = ['10.41.2.31', '10.41.1.25', '10.41.5.49', '10.41.2.41', '10.41.0.232', '10.41.5.67', '10.41.2.84', '10.41.0.162', '10.41.5.74']

for server in servers:
	if os.path.isfile("hackday_logs/"+server+".log"):
		df = pandas.read_csv("hackday_logs/"+server+".log", sep=';')
		df = df.tail(100)

		columns = df.columns.tolist()
		for column in columns:
			if column not in number_type_logs:
				df.drop(column, axis=1, inplace=True)
		
		print df.describe()

		for col in df.columns.tolist():
			if (col in ['rxpck/s', 'txpck/s']):
				if (df[col].std() > df[col].mean()*5):
					print "possible issue in: server "+server+" col "+col						
			elif (df[col].std() > df[col].mean()/10):
				print "possible issue in: server "+server+" col "+col
		print "============================================"
