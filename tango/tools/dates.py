import copy
from datetime import date
from datetime import datetime
import re

class InvalidDateString(Exception): pass

def month_number_from_name(month_name):
    """
    >>> month_number_from_name('JuLy')
    7
    """
    return datetime.strptime(month_name, '%B').month

def sanitize_date_components(year, month, day, today=None):
    """
    Takes 3 integers and runs sanity check on them, for example:

    * If year is 2 digits, assume it's the previous century if it's
      10 years past the current date, else the current century.
      In order to have this functionality for times other than right now,
      an optional 'today' argument can be passed.

    * If month is greater than 12, then really month is day and day is
      month

    >>> sanitize_date_components(05, 7, 13, today=date(2012,1,1))
    (2005, 7, 13)

    >>> sanitize_date_components(05, 13, 7, today=date(2012,1,1))
    (2005, 7, 13)

    >>> sanitize_date_components(94, 7, 13, today=date(2012,1,1))
    (1994, 7, 13)

    >>> sanitize_date_components(02, 7, 13, today=date(1999, 1, 1))
    (2002, 7, 13)

    >>> sanitize_date_components(02, 7, 13, today=date(1991, 1, 1))
    (2002, 7, 13)

    >>> sanitize_date_components(10, 7, 13, today=date(1991, 1, 1))
    (1910, 7, 13)

    """

    if today is None:
        today = date.today()

    if len(str(year)) < 4:
        today_century_bit = int(str(today.year)[0:2])
        today_year_bit = int(str(today.year)[2:4])

        # default
        century_bit = today_century_bit

        # if the 90's or greater, assume we're talking about a date in the
        # next century if it's less than 10 into the new century.
        if today_year_bit > 90 and year < 10:
            century_bit += 1

        elif year > today_year_bit + 10:
            century_bit -= 1

        year += century_bit * 100
        
    if month > 12:
        _month = month
        month = day
        day = _month

    return (year, month, day)


def process_date(date_str):
    """
    Takes a string that represents a date and tries to return
    a datetime.date object if it can figure it out.

    >>> # year month day
    >>> process_date("2008-07-06") == date(2008, 7, 6)
    True
    >>> process_date("2008/07/06") == date(2008, 7, 6)
    True
    >>> process_date("2008 07 06") == date(2008, 7, 6)
    True
    >>> process_date("2008 13 06") == date(2008, 6, 13)
    True
    >>> process_date("2008-7-6") == date(2008, 7, 6)
    True

    >>> # full month day year
    >>> process_date("July 6th 2008") == date(2008, 7, 6)
    True
    >>> process_date("July 06 2008") == date(2008, 7, 6)
    True
    >>> process_date("July 6th") == date(date.today().year, 7, 6)
    True
    >>> process_date("July/06/2008") == date(2008, 7, 6)
    True

    >>> # abbr month day year
    >>> process_date("07/06/2008") == date(2008, 7, 6)
    True
    >>> process_date("13/06/2008") == date(2008, 6, 13)
    True
    >>> process_date("07/06") == date(date.today().year, 7, 6)
    True
    """

    swap = lambda x, y: (y, x)

    # date is of format:
    # "2008-07-06"
    # "2008/07/06"
    # "2008 07 06"
    # "2008 7 6"
    pattern = re.compile(r"""^
        (?P<year>\d{4})
        [-/\s]
        (?P<month>\d{1,2})
        [-/\s]
        (?P<day>\d{1,2})
    """, re.VERBOSE)
    match = pattern.match(date_str)
    if match:
        year = int(match.group('year'))
        month = int(match.group('month'))
        day = int(match.group('day'))

        if month > 12:
            month, day = swap(month, day)

        return date(year, month, day)


    # date is of format "July 6th 2008"
    pattern = re.compile(r"""^
        (?P<month>[a-zA-Z]+)       # 'July'
        [-/\s]                      # divider (- / or a space)
        (?P<day>\d{1,2})            # 06 or 6
        (?:[a-zA-Z]{2})?                  # optional 'st', 'th' or 'rd'
        (?:[-/\s](?P<year>\d{4}))?  # optional year component (preceded by divider)
    """, re.VERBOSE)
    match = pattern.match(date_str)
    if match:
        month = month_number_from_name(match.group('month'))
        day = int(match.group('day'))

        if match.group('year') is not None:
            year = int(match.group('year'))
        else:
            year = date.today().year

        return date(year, month, day)


    # date is of format "7/6", "07/06" or "13/07"
    pattern = re.compile(r"""^
        (?P<month>\d{1,2})
        [-/ ]
        (?P<day>\d{1,2})
        (?:[-/ ](?P<year>\d{2,4}))?
    """, re.VERBOSE)
    match = pattern.match(date_str)
    if match:
        month = int(match.group('month'))
        day = int(match.group('day'))

        if month > 12:
            _month = month
            day = month
            month = day

        year = date.today().year

        return date(year, month, day)

    raise InvalidDateString("{date_str} is not a valid date string.".format(
        date_str=date_str,
    ))


if __name__ == "__main__":
    #if False:
    if True:
        import doctest
        doctest.testmod()
    #print process_date("2008-07-06")

