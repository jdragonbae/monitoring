import sys, os
import numpy, pandas
import time, datetime
import curses
from scipy import stats


number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]
servers = ['10.41.2.31', '10.41.1.25', '10.41.5.49', '10.41.2.41', '10.41.0.232', '10.41.5.67', '10.41.2.84', '10.41.0.162', '10.41.5.74']

def report_progress(cpu0avg, cpu0cur, cpu1avg, cpu1cur, memavg, memcur, rxavg, rxcur, txavg, txcur):

    counter = 0
    for server, state in cpu0avg.iteritems():
        stdscr.addstr(counter+0, 0, "====================[\t"+server+"\t]====================")        
        stdscr.addstr(counter+1, 0, "[CPU 0 Idle]\tAverage: {0}\tCurrent: {0}".format(cpu0avg[server], cpu0cur[server]))
        stdscr.addstr(counter+2, 0, "[CPU 1 Idle]\tAverage: {0}\tCurrent: {0}".format(cpu1avg[server], cpu1cur[server]))
        stdscr.addstr(counter+3, 0, "[Free Mem]\tAverage: {0}\tCurrent: {0}".format(cpu1avg[server], cpu1cur[server]))
        counter += 4
    stdscr.refresh()


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    cpu0avg = {}
    cpu0cur = {}
    cpu1avg = {}
    cpu1cur = {}
    memavg = {}
    memcur = {}
    rxavg = {}
    rxcur = {}
    txavg = {}
    txcur = {}

    try:
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

                columns = df.columns.tolist()
                for column in columns:
                    if column not in number_type_logs:
                        df.drop(column, axis=1, inplace=True)

                for col in df.columns.tolist():

                    #=================
                    # cpu
                    #=================

                    if col == 'cpu-0-idle':
                        cpu0avg[server] = str.format('{:.3f}', df[col].mean())
                        cpu0cur[server] = str.format('{:.3f}', df[col].iloc[-1])
                    elif col == 'cpu-1-idle':
                        cpu1avg[server] = str.format('{:.3f}', df[col].mean())
                        cpu1cur[server] = str.format('{:.3f}', df[col].iloc[-1])

                    #=================
                    # mem
                    #=================

                    elif col == 'free-mem':
                        memavg[server] = str.format('{:.3f}', df[col].mean())
                        memcur[server] = str.format('{:.3f}', df[col].iloc[-1])

                    #=================
                    # network
                    #=================

                    elif col == 'rxpck/s':
                        rxavg[server] = str.format('{:.3f}', df[col].mean())
                        rxcur[server] = str.format('{:.3f}', df[col].iloc[-1])
                    elif col == 'txpck/s':
                        txavg[server] = str.format('{:.3f}', df[col].mean())
                        txcur[server] = str.format('{:.3f}', df[col].iloc[-1])

        for i in range(0, 20): # arbitrary number of times, this should be fixed
            report_progress(cpu0avg, cpu0cur, cpu1avg, cpu1cur, memavg, memcur)
            time.sleep(1)

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
