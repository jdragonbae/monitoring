import sys
import pandas
import numpy

number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]


def get_df(logfile_name):
	df = pandas.read_csv(logfile_name, sep=';')

	print df.columns.tolist()
	return df

if __name__ == '__main__':
	
	normal_df = get_df('hackday.log')
	deployed_df = get_df('hackday_deployed.log')

	for column in normal_df.columns.tolist():
		if (column in number_type_logs):
			print "=====" + column + "====="
			print "threshold: " + str(normal_df[column].min()) + "~" + str(normal_df[column].max())
			print "deployed mean: " + str(deployed_df[column].mean())
