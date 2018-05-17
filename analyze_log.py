import pandas
import numpy


df = pandas.read_csv('hackday.log', sep=';')

number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]

print df.columns.tolist()

for column in df.columns.tolist():
	if (column in number_type_logs):
		print column + " " + str(df[column].mean())
