"""
The next fn is a result of CrossRef not always having an accurate publication
date.  So, we take a best-guess that the earliest date associated with the
record is probably the publication date, or the closest thing to it.
"""

import datetime
from dateutil.tz import tzutc
from dateutil import parser
import logging
 

class CrossRefEarliestDate:
    def __init__(self,works_record):
        self.earliest_date = self.cr_earliest_date(works_record)


    def parse_date_parts(self,date_parts):
        if type(date_parts)==list and len(date_parts):
            y = date_parts[0]
            try:
                m = date_parts[1]
            except:
                m = 1
            try:
                d = date_parts[2]
            except:
                d = 1
            date_parts_dt = datetime.datetime(y,m,d,0,0, tzinfo=tzutc())
            return date_parts_dt
        else:
            return None

    def cr_earliest_date(self,works_record):
        '''
        Takes a CrossRef works record and returns the earliest date associated with it.
        packages: dateutil.parser
        '''
        # logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        if 'earliest_date' in works_record and type(works_record['earliest_date'])==dict:
            return works_record['earliest_date']
        else:
            date_types = ['created', 'deposited', 'indexed', 'issued',
                        'published-online', 'published-print']
            dates = []
            for date_type in date_types:
                # date_types are often missing in CrossRef works records, so we're checking
                if date_type in works_record:
                    date_dict = works_record[date_type]
                    for thing in date_dict:
                        if type(date_dict[thing])==list:
                            date_parts = date_dict[thing][0]
                            if date_parts==[None]:
                                date_parts_dt=None
                            else:
                                date_parts_dt = self.parse_date_parts(date_parts)
                            if date_parts_dt!=None:
                                dates.append(date_parts_dt)
                        try:
                            dates.append(parser.parse(date_dict[thing]))
                        except:
                            # in case the parser fails
                            pass
                else:
                    pass
            earliest = min(dates)
            formatted_earliest = self.format_earliest_date(earliest)
            return formatted_earliest

    def format_earliest_date(self,earliest_date):
        date_parts = [earliest_date.year,
                     earliest_date.month,
                     earliest_date.day]
        timestamp = int(earliest_date.timestamp()*1000)
        date_time = datetime.datetime.strftime(earliest_date,
                                                "%Y-%m-%dT%H:%M:%SZ")
        return {'date-parts':date_parts,
               'timestamp':timestamp,
               'date-time':date_time}