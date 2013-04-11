import fractions
from .. import abstract
from .. import lib
from .. import libzone

def test_classes(test):
	test.fail_if_subclass(lib.Timestamp, lib.Measure)
	test.fail_if_subclass(lib.Date, lib.Days)
	test.fail_if_subclass(lib.Week, lib.Weeks)
	test.fail_if_subclass(lib.GregorianMonth, lib.Months)
	test.fail_if_not_subclass(lib.Measure, abstract.Time)
	test.fail_if_not_subclass(lib.Days, abstract.Time)
	test.fail_if_not_subclass(lib.Weeks, abstract.Time)
	test.fail_if_not_subclass(lib.Months, abstract.Time)

def test_instants(test):
	ts=lib.Timestamp(0)
	secs=lib.Measure(0)
	# no adjustments in __new__
	test.fail_if_not_equal(ts, secs)

def test_ratios(test):
	test.fail_if_not_equal(1000000, lib.Context.compose('second', 'microsecond'))
	test.fail_if_not_equal(
		fractions.Fraction(1,1000000), lib.Context.compose('microsecond', 'second'))

def test_of_Measure(test):
	mult = int(lib.Measure.of(second=1))
	ts = lib.Measure.of(second = 20)
	test.fail_if_not_equal(ts.start, lib.Measure.of())

	test.fail_if_not_equal(ts, 20 * mult)
	ts = lib.Measure.of(second = -20)
	test.fail_if_not_equal(ts, -20 * mult)
	ts = lib.Measure.of(day = 1)
	test.fail_if_not_equal(ts, 24 * 60 * 60 * mult)
	# multiple fields
	ts = lib.Measure.of(day = 1, second = 20)
	test.fail_if_not_equal(ts, (24 * 60 * 60 * mult) + (20 * mult))
	# and more
	ts = lib.Measure.of(day = 1, minute = 2, second = 20)
	test.fail_if_not_equal(ts, (24 * 60 * 60 * mult) + (2*60*mult) + (20 * mult))

	# and much more o.O
	units = {
		'week': 1,
		'day': 1,
		'hour': 1,
		'minute': 1,
		'second': 1,
		'megasecond': 1,
		'kilosecond': 1,
		'millisecond': 1,
		'centisecond': 1,
		'decisecond': 1,
		lib.Measure.unit: 111,
	}

	total = 111 + mult + (
		(60 * mult) + \
		(60 * 60 * mult) + \
		(24 * 60 * 60 * mult) + \
		(7 * 24 * 60 * 60 * mult) + \
		((10 ** 6) * mult) + \
		((10 ** 3) * mult) + \
		int((10 ** (-3)) / (10 ** (-9))) + \
		int((10 ** (-2)) / (10 ** (-9))) + \
		int((10 ** (-1)) / (10 ** (-9)))
	)
	test.fail_if_not_equal(total, lib.Measure.of(**units))

	# 1111...
	units = {
		'microsecond': 123,
		'millisecond': 2,
		'centisecond': 1,
		'decisecond': 2,
		'second': 1,
		'decasecond': 1,
		'hectosecond': 2,
		'kilosecond': 121,
		'megasecond': 211,
		'gigasecond': 121,
		'terasecond': 211,
		'petasecond': 121,
		'exasecond': 117,
		'zettasecond': 218,
		'yottasecond': 19
	}
	# The number is the concatenation of the above parts.
	test.fail_if_not_equal(19218117121211121211121211212123000,
		lib.Measure.of(**units)
	)

def test_of_months(test):
	us = lib.Measure.of(month=5)
	d = lib.Days.of(month=5)
	m = lib.Months.of(day = d)
	test.fail_if_not_equal(int(m), 5)

def test_of_iso(test):
	isostr = "1778-06-01T20:21:22.23"
	ts = lib.Timestamp.of(iso=isostr)
	pts = ts.of(
		year = 1778, month = 5, day = 0,
		hour = 20, minute = 21, second = 22,
		microsecond = 230000)
	test.fail_if_not_equal(ts, pts)
	test.fail_if_not_equal(ts.select('iso'), isostr)
	test.fail_if_not_equal(pts.select('iso'), isostr)
	test.fail_if_not_equal(ts.of(iso=ts.select('iso')), pts)

def test_of_iso_date(test):
	isostr = "1999-01-01"
	isod = lib.Date.of(iso=isostr)
	d = lib.Date.of(year = 1999, month = 0, day = 0)
	test.fail_if_not_equal(isod.select('date'), (1999,1,1))
	test.fail_if_not_equal(d, isod)

leap_samples = [
	(False, "1600-02-29T00:00:00.0"), # shouldnt wrap
	(True, "1601-02-29T00:00:00.0"), # should wrap
	(False, "1604-02-29T00:00:00.0"), # shouldn't wrap
	(True, "1700-02-29T00:00:00.0"), # should wrap
	(True, "1800-02-29T00:00:00.0"), # should wrap
	(True, "1900-02-29T00:00:00.0"), # should wrap
	(False, "2000-02-29T00:00:00.0"), # shouldn't wrap
]

def test_of_leaps(test):
	for should_wrap, iso in leap_samples:
		ts = lib.Timestamp.of(iso=iso)
		if should_wrap:
			test.fail_if_equal(iso, ts.select('iso'))
		else:
			test.fail_if_not_equal(iso, ts.select('iso'))

def test_of_relative(test):
	ts = lib.Timestamp.of(iso="2000-01-00T12:45:00")
	test.fail_if_not_equal(ts.select('year'), 1999)
	test.fail_if_not_equal(ts.select('month', 'year'), 11)
	test.fail_if_not_equal(ts.select('day', 'month'), 30)
	test.fail_if_not_equal(ts.select('date'), (1999,12,31))
	test.fail_if_not_equal(ts.select('datetime'), (1999,12,31,12,45,0))

def test_date_contains(test):
	d = lib.Date.of(year=2000,month=6,day=4)
	p = lib.Timestamp.of(year=2000,month=6,day=3,hour=3,minute=23,second=1)
	test.fail_if_in(p, d)
	test.fail_if_in(d, p)
	d = lib.Date.of(year=2000,month=6,day=3)
	test.fail_if_not_in(p, d)
	test.fail_if_in(d, p)

def test_week_contains(test):
	w = lib.Week.of(date=(1999,12,30))
	d = lib.Date.of(w)
	dts = lib.Timestamp.of(d)
	wts = lib.Timestamp.of(w)
	test.fail_if_not_in(dts, w)
	test.fail_if_not_in(wts, w)
	test.fail_if_not_in(d, w)
	test.fail_if_not_in(d.elapse(day=1), w)
	test.fail_if_not_in(d.elapse(day=2), w)
	test.fail_if_not_in(d.elapse(day=3), w)
	test.fail_if_not_in(d.elapse(day=4), w)
	test.fail_if_not_in(d.elapse(day=5), w)
	test.fail_if_not_in(d.elapse(day=6), w)
	# negatives
	test.fail_if_in(d.elapse(day=-1), w)
	test.fail_if_in(d.elapse(day=7), w)

def test_part_datetime(test):
	# Presuming the datum in this test.
	# Remove or rework if desired.
	t = lib.Timestamp.of(datetime=(2000, 1, 2, 0, 0, 0,))
	test.fail_if_not_equal(0, t)
	t = lib.Timestamp(lib.Timestamp.of(datetime=(2000, 1, 2, 0, 0, 0)) + 1)
	test.fail_if_not_equal(1, t)
	t = lib.Timestamp(lib.Timestamp.of(datetime=(2000, 1, 2, 0, 0, 0)) - 1)
	test.fail_if_not_equal(-1, t)

def test_relative_times(test):
	previous_month = lib.Timestamp.of(
		datetime=(2000, 0, 1, 0, 0, 0)
	)
	rprevious_month = lib.Timestamp.of(
		datetime=(1999, 12, 1, 0, 0, 0)
	)
	test.fail_if_not_equal(previous_month, rprevious_month)

	previous_day = lib.Timestamp.of(
		datetime=(2000, 1, 0, 0, 0, 0)
	)
	rprevious_day = lib.Timestamp.of(
		datetime=(1999, 12, 31, 0, 0, 0)
	)
	test.fail_if_not_equal(previous_day, rprevious_day)

def test_lib_select(test):
	ts = lib.Timestamp.of(iso="1599-03-02T03:23:10.003211")
	test.fail_if_not_equal(3, lib.select.hour.day()(ts))
	test.fail_if_not_equal(10, lib.select.second.minute()(ts))
	test.fail_if_not_equal(3211, lib.select.microsecond.second()(ts))
	test.fail_if_not_equal(23, lib.select.minute.hour()(ts))
	#
	test.fail_if_not_equal(1, lib.select.day.month()(ts))
	test.fail_if_not_equal(2, lib.select.month.year()(ts))
	test.fail_if_not_equal(1599, lib.select.year()(ts))
	test.fail_if_not_equal(99, lib.select.year.century()(ts))

def test_lib_update(test):
	ts = lib.Timestamp.of(iso="1599-03-02T03:23:10.003211")
	test.fail_if_not_equal(ts.update('month', 0, 'year'), lib.Timestamp.of(iso="1599-01-02T03:23:10.003211"))
	test.fail_if_not_equal(ts.update('month', 11, 'year'), lib.Timestamp.of(iso="1599-12-02T03:23:10.003211"))
	test.fail_if_not_equal(ts.update('month', 5, 'year'), lib.Timestamp.of(iso="1599-6-02T03:23:10.003211"))
	test.fail_if_not_equal(ts.update('month', 6, 'year'), lib.update.month.year(6)(ts))
	test.fail_if_not_equal(ts.update('day', 15, 'month'), lib.update.day.month(15)(ts))
	test.fail_if_not_equal(ts.update('day', 2, 'week'), lib.update.day.week(2)(ts))
	test.fail_if_not_equal(ts.update('hour', 23, 'day'), lib.update.hour.day(23)(ts))

def test_date(test):
	ts = lib.Timestamp.of(iso="1825-01-15T3:45:01.021344")
	d = lib.Date.of(ts)
	test.fail_if_not_in(ts, d)

def test_truncate(test):
	samples = [
		(lib.Timestamp.of(iso="2000-03-18T13:34:59.999888777"), [
			('week', lib.Timestamp.of(iso="2000-03-12T00:00:00.0")),
		]),
		(lib.Timestamp.of(iso="2000-03-19T13:34:59.999888777"), [
			('week', lib.Timestamp.of(iso="2000-03-19T00:00:00.0")),
		]),
		(lib.Timestamp.of(iso="1923-04-18T13:34:59.999888777"), [
			('second', lib.Timestamp.of(iso="1923-04-18T13:34:59.000")),
			('minute', lib.Timestamp.of(iso="1923-04-18T13:34:00.0")),
			('hour', lib.Timestamp.of(iso="1923-04-18T13:00:00.0")),
			('day', lib.Timestamp.of(iso="1923-04-18T00:00:00.0")),
			('week', lib.Timestamp.of(iso="1923-04-15T00:00:00.0")),
			('month', lib.Timestamp.of(iso="1923-04-01")),
			('year', lib.Timestamp.of(iso="1923-01-01")),
		]),
	]

	for (ts, cases) in samples:
		for (unit, result) in cases:
			truncd = ts.truncate(unit)
			test.fail_if_not_equal(truncd, result)

def test_measure_method(test):
	old = lib.Timestamp.of(iso="1900-01-01T00:00:00")
	new = lib.Timestamp.of(iso="1900-01-11T00:00:00")
	test.fail_if_not_equal(old.measure(new), lib.Measure.of(day=10))
	test.fail_if_not_equal(new.measure(old), lib.Measure.of(day=-10))

def test_rollback(test):
	ts = lib.Timestamp.of(iso="1982-05-18T00:00:00")
	test.fail_if_not_equal(ts.measure(ts.rollback(minute=5)), ts.Measure.of(minute=-5))

def test_timeofday_select(test):
	zero = lib.Timestamp(0)
	test.fail_if_not_equal((0, 0, 0), zero.select('timeofday'))
	ts = lib.Timestamp.of(iso="1812-01-01T03:45:02")
	test.fail_if_not_equal((3, 45, 2), ts.select('timeofday'))

	ts = lib.Timestamp.of(iso="1825-01-15T3:45:01.021344")
	hour, minute, second = ts.select('timeofday')
	test.fail_if_not_equal(hour, 3)
	test.fail_if_not_equal(minute, 45)
	test.fail_if_not_equal(second, 1)

def test_align(test):
	"""
	The most important use of alignment is for finding the n-th
	since the first or last of a month.
	"""
	def select_last_thurs(ts):
		ts = ts.elapse(month=1)
		ts = ts.update('day', -1, 'month')
		ts = ts.update('day', 0, 'week', align=-4)
		return ts
	ts = lib.Timestamp.of(iso="2010-02-08T12:30:00")
	test.fail_if_not_equal(select_last_thurs(ts).select('date'), (2010, 2, 25))
	ts = lib.Timestamp.of(iso="2010-01-09T12:30:00")
	test.fail_if_not_equal(select_last_thurs(ts).select('date'), (2010, 1, 28))
	ts = lib.Timestamp.of(iso="2010-09-14T12:30:00")
	test.fail_if_not_equal(select_last_thurs(ts).select('date'), (2010, 9, 30))
	ts = lib.Timestamp.of(iso="2010-03-21T13:30:00")
	test.fail_if_not_equal(select_last_thurs(ts).select('date'), (2010, 3, 25))

def test_unix(test):
	unix_epoch = lib.Timestamp.of(iso="1970-01-01T00:00:00")
	ts = lib.Timestamp.of(unix=0)
	test.fail_if_not_equal(unix_epoch, ts)
	test.fail_if_not_equal(unix_epoch, lib.unix(0))
	test.fail_if_not_equal(ts.select('unix'), 0)

def test_hashing(test):
	us0 = lib.Measure(0)
	ts0 = lib.Timestamp(0)
	ds0 = lib.Days(0)
	dt0 = lib.Date(0)
	M0 = lib.Months(0)
	gm0 = lib.GregorianMonth(0)
	d = {0:'foo'}
	d[us0] = 'us'
	d[ts0] = 'ts'
	d[ds0] = 'ds'
	d[dt0] = 'dt'
	d[M0] = 'M'
	d[gm0] = 'GM'
	test.fail_if_not_equal(1, len(d)) # wait, really?

def test_now(test):
	test.fail_if_not_instance(lib.now(), lib.Timestamp)

def test_business_week(test):
	expected = [
		lib.Date.of(iso="2009-02-16T3:45:15.0"),
		lib.Date.of(iso="2009-02-17T3:45:15.0"),
		lib.Date.of(iso="2009-02-18T3:45:15.0"),
		lib.Date.of(iso="2009-02-19T3:45:15.0"),
		lib.Date.of(iso="2009-02-20T3:45:15.0"),
	]
	test.fail_if_not_equal(
		lib.business_week(lib.Date.of(iso="2009-02-15T3:45:15.0")),
		expected
	)
	test.fail_if_not_equal(
		lib.business_week(lib.Date.of(iso="2009-02-16T3:45:15.0")),
		expected
	)
	test.fail_if_not_equal(
		lib.business_week(lib.Date.of(iso="2009-02-17T3:45:15.0")),
		expected
	)
	test.fail_if_not_equal(
		lib.business_week(lib.Date.of(iso="2009-02-18T3:45:15.0")),
		expected
	)
	test.fail_if_not_equal(
		lib.business_week(lib.Date.of(iso="2009-02-19T3:45:15.0")),
		expected
	)
	test.fail_if_not_equal(
		lib.business_week(lib.Date.of(iso="2009-02-20T3:45:15.0")),
		expected
	)
	test.fail_if_not_equal(
		lib.business_week(lib.Date.of(iso="2009-02-21T3:45:15.0")),
		expected
	)

def test_subseconds(test):
	val = lib.Measure.of(second=1, subsecond=0.5)
	test.fail_if_not_equal(val, lib.Measure.of(centisecond=150))

	test.fail_if_not_equal(float(val.select('subsecond')), 0.5)

def test_clock_features(test):
	clock = lib.clock
	test.fail_if_not_instance(clock.demotic(), lib.Timestamp)
	test.fail_if_not_instance(clock.monotonic(), lib.Measure)
	test.fail_if_not_instance(clock.sleep(123), lib.Measure)
	for x, t in zip(range(3), clock.meter()):
		test.fail_if_less_than(t, 0)
		test.fail_if_not_instance(t, lib.Measure)
	for x, t in zip(range(3), clock.delta()):
		test.fail_if_less_than(t, 0)
		test.fail_if_not_instance(t, lib.Measure)
	with clock.stopwatch() as total:
		pass
	test.fail_if_not_instance(total(), lib.Measure)
	test.fail_if_not_equal(total(), total())

	periods = clock.periods(lib.Measure.of(subsecond=0.1))
	test.fail_if_not_equal(next(periods)[0], 0) # fragile
	clock.sleep(lib.Measure.of(subsecond=0.1))
	test.fail_if_not_equal(next(periods)[0], 1) # fragile
	clock.sleep(lib.Measure.of(subsecond=0.2))
	test.fail_if_not_equal(next(periods)[0], 2) # fragile

def test_clock_sleeper(test):
	clock = lib.clock
	s = clock.sleeper()
	s.frequency = 100
	s.remainder = 100
	x = next(s)
	test.fail_if_not_instance(x, lib.Measure)
	test.fail_if_less_than(x, lib.Measure(100))

	s.remainder = 400
	s.disturb()
	x = next(s)
	test.fail_if_not_instance(x, lib.Measure)
	test.fail_if_not_equal(x, lib.Measure(0))

	# show retention of all disturbs
	s.remainder = 50
	s.disturb()
	s.disturb()
	s.disturb()
	test.fail_if_not_equal(next(s), lib.Measure(0))
	test.fail_if_not_equal(next(s), lib.Measure(0))
	test.fail_if_not_equal(next(s), lib.Measure(0))
	test.fail_if_less_than(next(s), lib.Measure(50))

def test_range(test):
	test.fail_if_not_equal(list(lib.range(
			lib.Timestamp.of(year=2000,month=0,day=0),
			lib.Timestamp.of(year=2001,month=0,day=0),
			lib.Months.of(year=1)
		)), [
			lib.Timestamp.of(year=2000,month=0,day=0),
		]
	)
	test.fail_if_not_equal(list(lib.range(
			lib.Timestamp.of(year=2000,month=0,day=0),
			lib.Timestamp.of(year=2002,month=0,day=0),
			lib.Months.of(year=1)
		)), [
			lib.Timestamp.of(year=2000,month=0,day=0),
			lib.Timestamp.of(year=2001,month=0,day=0),
		]
	)

def test_field_delta(test):
	ts = lib.Timestamp.of(year=3000,hour=3,minute=59,second=59)
	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('minute',
			ts, ts.elapse(second=3)
		))), [
			lib.Timestamp.of(year=3000,hour=4,minute=0)
		]
	)

	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('second',
			ts, ts.elapse(second=3)
		))), [
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=0),
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=1),
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=2),
		]
	)

	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('second',
			ts, ts.elapse(second=4)
		))), [
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=0),
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=1),
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=2),
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=3),
		]
	)

	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('hour',
			ts, ts.elapse(second=1)
		))), [
			lib.Timestamp.of(year=3000,hour=4,minute=0,second=0),
		]
	)

	# backwards field_delta
	ts = lib.Timestamp.of(year=3000,hour=4,minute=0,second=0)

	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('minute',
			ts, ts.rollback(second=3)
		))), [
			lib.Timestamp.of(year=3000,hour=3,minute=59)
		]
	)

	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('second',
			ts, ts.rollback(second=3)
		))), [
			lib.Timestamp.of(year=3000,hour=3,minute=59,second=59),
			lib.Timestamp.of(year=3000,hour=3,minute=59,second=58),
			lib.Timestamp.of(year=3000,hour=3,minute=59,second=57),
		]
	)

	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('second',
			ts, ts.rollback(second=3)
		))), [
			lib.Timestamp.of(year=3000,hour=3,minute=59,second=59),
			lib.Timestamp.of(year=3000,hour=3,minute=59,second=58),
			lib.Timestamp.of(year=3000,hour=3,minute=59,second=57),
		]
	)

	test.fail_if_not_equal(
		list(lib.range(*lib.field_delta('hour',
			ts, ts.rollback(second=1)
		))), [
			lib.Timestamp.of(year=3000,hour=3,minute=0,second=0),
		]
	)


def test_Months_elapse(test):
	m = lib.Months(1)
	ts = lib.Timestamp.of(date=(2000,2,1))
	test.fail_if_not_equal(ts.elapse(m), lib.Timestamp.of(date=(2000,3,1)))
	test.fail_if_not_equal(ts.rollback(m), lib.Timestamp.of(date=(2000,1,1)))

def test_month_spectrum(test):
	return
	start = lib.Timestamp.of(year=1600, month=0, day=0)
	end = lib.Timestamp.of(year=2000, month=0, day=0)

	t = start
	while t < end:
		test.fail_if_not_equal(t.select('day','month'), 0)
		n = t.elapse(month=1)
		test.fail_if_equal(n, t)
		test.fail_if_less_than(n, t)
		t = n

	t = end
	while t > start:
		test.fail_if_not_equal(t.select('day','month'), 0)
		n=t.rollback(month=1)
		test.fail_if_equal(n, t)
		test.fail_if_less_than(t, n)
		t = n

def test_zone(test):
	"""
	Presumes that Alaska is ~-10 and Japan is ~+10.
	"""
	today = 'America/Anchorage'
	tomorrow = 'Japan'
	now = lib.now()
	# need to work with the end of the day
	end_of_day = now.update('hour', 23, 'day')

	anchorage_zone = lib.zone(today)
	japan_zone = lib.zone(tomorrow)

	# get the zone offsets according to the end of the day
	anchorage_pit, this_offset = anchorage_zone.localize(now)
	japan_pit, next_offset = japan_zone.localize(now)

	today = lib.Date.of(end_of_day, this_offset)
	tomorrow = lib.Date.of(end_of_day, next_offset)

	test.fail_if_not_equal(today, tomorrow.elapse(day=-1))

def test_zone_dst_offset(test):
	# if this test fails, it *may* be due to timezone database changes
	at = lib.Timestamp.of(iso='2019-11-03T09:00:00.000000000')
	before = at.rollback(second=1)
	after = at.elapse(second=1)

	la_zone = lib.zone('America/Los_Angeles')

	local_at_pit, at_offset = la_zone.localize(at)
	local_before_pit, before_offset = la_zone.localize(before)
	local_after_pit, after_offset = la_zone.localize(after)

	test.fail_if_not_equal(before_offset.is_dst, True)
	test.fail_if_not_equal(at_offset.is_dst, False)
	test.fail_if_not_equal(after_offset.is_dst, False)

def test_zone_default_only(test):
	z = lib.zone('MST')
	pits = lib.range(
		lib.Timestamp.of(iso='2006-01-03T09:00:00.000000000'),
		lib.Timestamp.of(iso='2009-01-03T09:00:00.000000000'),
		lib.Months.of(month=1)
	)
	s = set()
	for x in pits:
		s.add(z.find(x))
	test.fail_if_not_equal(len(s), 1)

def test_zone_normalize(test):
	# at a transition point.
	at = lib.Timestamp.of(iso='2019-11-03T09:00:00.000000000')

	z = lib.zone('America/Los_Angeles')

	at, o = z.localize(at)
	test.fail_if_not_equal(o.is_dst, False)

	before = at.rollback(second=1)

	# normalization of `before` should result in a recognized transition
	n_pit, n_offset = z.normalize(o, before)
	test.fail_if_equal(n_offset, o)

def test_zone_slice(test):
	start = lib.Timestamp.of(iso='2006-01-03T09:00:00.000000000')
	stop = lib.Timestamp.of(iso='2007-12-03T09:00:00.000000000')

	# XXX: assuming LA zone consistency. fix with a contrived libzone.Zone() instance.
	test.fail_if_not_equal(list(lib.zone('America/Los_Angeles').slice(start, stop)), [
		(lib.Timestamp.of(iso='2005-10-30T09:00:00.000000000'), libzone.Offset((-28800, 'PST', 'std'))),
		(lib.Timestamp.of(iso='2006-04-02T10:00:00.000000000'), libzone.Offset((-25200, 'PDT', 'dst'))),
		(lib.Timestamp.of(iso='2006-10-29T09:00:00.000000000'), libzone.Offset((-28800, 'PST', 'std'))),
		(lib.Timestamp.of(iso='2007-03-11T10:00:00.000000000'), libzone.Offset((-25200, 'PDT', 'dst'))),
		(lib.Timestamp.of(iso='2007-11-04T09:00:00.000000000'), libzone.Offset((-28800, 'PST', 'std')))
	])
	test.fail_if_not_equal(list(lib.zone('MST').slice(start, stop)), [])
