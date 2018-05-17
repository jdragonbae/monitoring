import sys
import pandas
import numpy

number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]
logfile_normal = "hackday_normal.log"
logfile_deployed = "hackday_deployed.log"

def get_df(logfile_name):
	df = pandas.read_csv(logfile_name, sep=';')
	return df

if __name__ == '__main__':
	
	df_normal = pandas.read_csv(logfile_normal, sep=';')
	df_deployed = pandas.read_csv(logfile_deployed, sep=';')

	for column in df_normal.columns.tolist():
		if (column in number_type_logs):
			print "=====" + column + "====="
			print "threshold: " + str(df_normal[column].min()) + "~" + str(df_normal[column].max())
			print "deployed mean: " + str(df_deployed[column].mean())
