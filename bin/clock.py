"""
# Repeatedly print the current date and time every 64 milliseconds.

# Carriage returns will be used to overwrite previous displays.
"""
import sys
from .. import sysclock
from .. import library

def print_local_timestamp(now=sysclock.now):
	localtime = library.zone()
	try:
		while not None:
			ts = now()
			st = localtime.localize(ts)[0].select('iso')
			sys.stdout.write(("   " + st + "\r"))
	except KeyboardInterrupt:
		sys.stdout.write("\r\n")
		sys.exit(0)

if __name__ == '__main__':
	print_local_timestamp()
