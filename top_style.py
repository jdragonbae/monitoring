import sys, os
import numpy, pandas
import time, datetime
import curses
from scipy import stats


number_type_logs = ["cpu-0-idle", "cpu-1-idle", "free-mem", "rxpck/s", "txpck/s"]
servers = ['10.41.2.31', '10.41.1.25', '10.41.5.49', '10.41.2.41', '10.41.0.232', '10.41.5.67', '10.41.2.84', '10.41.0.162', '10.41.5.74']

def report_progress(filename, progress):
    """progress: 0-10"""
    stdscr.addstr(0, 0, "Moving file: {0}".format(filename))
    stdscr.addstr(1, 0, "Total progress: [{1:10}] {0}%".format(progress * 10, "#" * progress))
    stdscr.refresh()

if __name__ == "__notmain__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        for i in range(10):
            report_progress("file_{0}.txt".format(i), i+1)
            time.sleep(0.5)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()

def report_progress_cpu(cpu0avg, cpu0cur, cpu1avg, cpu1cur):
    """
    stdscr.addstr(0, 0, "CPU 0 Idle - Average: {0}".format(cpu0avg))
    stdscr.addstr(1, 0, "CPU 0 Idle - Current: {0}".format(cpu0cur))
    stdscr.addstr(2, 0, "CPU 1 Idle - Average: {0}".format(cpu1avg))
    stdscr.addstr(3, 0, "CPU 1 Idle - Current: {0}".format(cpu1cur))
    stdscr.refresh()
    """
    counter = 0
    for server, state in cpu0avg.iteritems():
        stdscr.addstr(counter+0, 0, "["+server+"] CPU 0 Idle - Average: {0}".format(cpu0avg[server]))
        stdscr.addstr(counter+1, 0, "["+server+"] CPU 0 Idle - Current: {0}".format(cpu0cur[server]))
        stdscr.addstr(counter+2, 0, "["+server+"] CPU 1 Idle - Average: {0}".format(cpu1avg[server]))
        stdscr.addstr(counter+3, 0, "["+server+"] CPU 1 Idle - Current: {0}".format(cpu1cur[server]))
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

        for i in range(0, 20): # arbitrary number of times, this should be fixed
            report_progress_cpu(cpu0avg, cpu0cur, cpu1avg, cpu1cur)
            time.sleep(1)

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
