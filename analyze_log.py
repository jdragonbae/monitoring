import sys
import pandas
import numpy

number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]
filename = "hackday.log"

def get_df(logfile_name):
	df = pandas.read_csv(logfile_name, sep=';')
	return df

if __name__ == '__main__':
	
	df = pandas.read_csv(filename, sep=';')

	for column in df.columns.tolist():
		if (column in number_type_logs):
			print "=====" + column + "====="
			print "mean:\t" + str(df[column].mean())
			print "median:\t" + str(df[column].median())
			print "max:\t" + str(df[column].max())
			print "min:\t" + str(df[column].min())
