import sys
import pandas
import numpy
from scipy import stats


number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]
servers = ['10.41.2.31', '10.41.1.25', '10.41.5.49', '10.41.2.41', '10.41.0.232', '10.41.5.67', '10.41.2.84', '10.41.0.162', '10.41.5.74']

for server in servers:
	df = pandas.read_csv("logs/"+server+".log", sep=';')

	print "******" + server + "******"
	for column in df.columns.tolist():
		if (column in number_type_logs):
			print "=====" + column + "====="
			print "mean:\t" + str(df[column].mean())
			print "median:\t" + str(df[column].median())
			print "max:\t" + str(df[column].max())
			print "min:\t" + str(df[column].min())

	print df
	df[(numpy.abs(stats.zscore(df)) < 3).all(axis=1)]
	print df