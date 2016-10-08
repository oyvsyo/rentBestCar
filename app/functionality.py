import pytz
from datetime import datetime, timedelta
from psycopg2.extras import DateTimeTZRange
from crontab import CronTab
from .constants import TIME_FORMAT
from .models import RangeSlot, BinSlot, Tutor, Pattern
from django.db.models import F
import logging
logger = logging.getLogger(__name__)


class Scheduling():
    """
    Class witch contain all scheduling methods and functions.
    """
    def get_free_tutors(self, str_date_start, str_date_end):
        """
        Search in BinSlot free tutors in range of [str_date_start, str_date_end]

        :param str_date_start: data_start in type String, in .constants.TIME_FORMAT format.
        :param str_date_end: data_end in type String. in .constants.TIME_FORMAT format.
        :return: dict; field 'response_code' and useful Information.
            - a) 'response_code'=='406': Some exception.
            - b) Return list of Tutors id with key 'tutors'.
        """
        ans = {}
        try:
            date_start = self._str_to_datetime(str_date_start)
            date_end = self._str_to_datetime(str_date_end)
            if date_start >= date_end:
                ans['response_code'] = '406'
                return ans
            else:
                ans['tutors'] = list(set(map(lambda x: x['tutor'], self._get_free_tutors_by_bin(date_start, date_end))))
                return ans
        except Exception, e:
            logger.error(e, exc_info=True)
            ans['response_code'] = '406'
            ans['error'] = str(e)
            return ans

    def get_free_timeslots(self, srt_tutor_id, str_date_start, str_date_end):
        """
        Get free RangeSlots of tutor in range of [str_date_start, str_date_end].
        If str_date_start=='' and str_date_end=='' get all RangeSlots

        :param srt_tutor_id: tutor id, type: string.
        :param str_date_start: data_start in type String, in .constants.TIME_FORMAT format.
        :param str_date_end: data_end in type String. in .constants.TIME_FORMAT format.
        :return: dict; field 'response_code' and useful Information.
            - a) 'response_code'=='406': Some exception.
            - b) Return list of RangeSlots with key 'timeslots'.
        """
        ans = {}
        try:
            tutor_id = int(srt_tutor_id)
            if str_date_start == '' and str_date_end == '':
                slots = RangeSlot.objects.filter(tutor_id=tutor_id)
            else:
                date_start = self._str_to_datetime(str_date_start)
                date_end = self._str_to_datetime(str_date_end)
                slots = RangeSlot.objects.\
                    filter(tutor_id=tutor_id).\
                    filter(date__overlap=DateTimeTZRange(date_start, date_end))

            timeslots = []
            for slot in slots:
                temp = {}
                temp['timeslot_id'] = slot.id
                temp['pattern'] = slot.pattern.mask if slot.pattern else ''
                temp['date_start'] = self._datetime_to_str(slot.date.lower)
                temp['date_end'] = self._datetime_to_str(slot.date.upper)
                temp['type'] = slot.type
                # 2.0
                temp['lesson_id'] = slot.lesson_id
                temp['tutoring_id'] = slot.tutoring_id
                temp['student_name'] = slot.student_name
                temp['student_email'] = slot.student_email
                temp['extra_time'] = slot.extra_time
                temp['title'] = slot.title
                temp['comment'] = slot.comment
                timeslots.append(temp)
            return {'timeslots': timeslots}
        except Exception, e:
            logger.error(e, exc_info=True)
            ans['response_code'] = '406'
            ans['error'] = str(e)
            return ans

    def set_new_timeslot(self, str_tutor_id, str_date_start, str_date_end, str_type, pattern, str_lesson_id='',
                         str_tutoring_id='', str_student_name='', str_student_email='', str_extra_time='', str_title='',
                         str_comment=''):
        """
        Create new RangeSlots and BinSlots.

        :param str_tutor_id: tutor id, type: string.
        :param str_date_start: data_start in type String, in .constants.TIME_FORMAT format.
        :param str_date_end: data_end in type String. in .constants.TIME_FORMAT format.
        :param str_type: type of TimeSlot, choice field of .constants.RANGE_SLOT_TYPE
        :param pattern: cron valid string;
            - a) =='': create non repeated TimeSlot.
            - b) =='* * * * *': create Pattern; create RangeSlots and BinSlots in range of [now, now + days(30)].
            - c) ==Pattern(): create RangeSlots and BinSlots in cron next time.
        :return: dict; field 'response_code' and useful Information.
            - a) 'response_code'=='405': RangeSlots overlap.
            - b) 'response_code'=='406': Some exception.
            - c) 'response_code'=='201': Return list of RangeSlot's id with key 'timeslots_id'.
        """
        ans = {}
        timeslots_created = []
        try:
            tutor_id = int(str_tutor_id)
            date_start = self._str_to_datetime(str_date_start)
            date_end = self._str_to_datetime(str_date_end)
            tutor, created = Tutor.objects.get_or_create(id=tutor_id)
            pattern = None if isinstance(pattern, basestring) and len(pattern) == 0 else pattern
            if RangeSlot.objects.filter(tutor=tutor).filter(
                    date__overlap=DateTimeTZRange(date_start, date_end)).exists():
                ans['response_code'] = '405'
                return ans
            else:
                if isinstance(pattern, basestring):
                    cron = CronTab(pattern)
                    pattern = Pattern.objects.create(mask=pattern, tutor=tutor)
                    date_start_temp = date_start - timedelta(seconds=abs(cron.previous(date_start)))
                    date_end_temp = date_end - timedelta(seconds=abs(cron.previous(date_start)))
                    interval = timedelta(days=30)

                    while date_start_temp < date_start + interval:
                        delta = cron.next(date_start_temp)
                        date_start_temp += timedelta(seconds=delta)
                        date_end_temp += timedelta(seconds=delta)

                        if not RangeSlot.objects.filter(tutor=tutor).filter(
                                date__overlap=DateTimeTZRange(date_start_temp, date_end_temp)).exists():
                            timeslots_created.append(
                                RangeSlot.objects.create(
                                    tutor_id=tutor_id,
                                    date=(date_start_temp, date_end_temp),
                                    pattern=pattern,
                                    type=str_type,
                                    # 2.0
                                    lesson_id=str_lesson_id,
                                    tutoring_id=str_tutoring_id,
                                    student_name=str_student_name,
                                    student_email=str_student_email,
                                    extra_time=str_extra_time,
                                    title=str_title,
                                    comment=str_comment
                                ).id
                            )
                            self._change_bin_dayslot(date_start_temp, date_end_temp, tutor_id, 1)
                else:
                    timeslots_created.append(
                        RangeSlot.objects.create(
                            tutor_id=tutor_id,
                            date=(date_start, date_end),
                            pattern=pattern,
                            type=str_type,
                            # 2.0
                            lesson_id=str_lesson_id,
                            tutoring_id=str_tutoring_id,
                            student_name=str_student_name,
                            student_email=str_student_email,
                            extra_time=str_extra_time,
                            title=str_title,
                            comment=str_comment
                        ).id
                    )
                    self._change_bin_dayslot(date_start, date_end, tutor_id, 1)

                ans['timeslots_id'] = timeslots_created
                ans['response_code'] = '201'
                return ans
        except Exception, e:
            logger.error(e, exc_info=True)
            ans['response_code'] = '406'
            ans['error'] = str(e)
            return ans

    def update_timeslot(self, str_timeslot_id, str_tutor_id, str_date_start, str_date_end, str_type, str_lesson_id=''):
        """
        Update RangeSlot and BinSlot. If isinstance(pattern, Pattern): change only type, else all field.

        :param str_timeslot_id: RangeSlot's id, type: string.
        :param str_tutor_id: Tutor's id, type: string.
        :param str_date_start: data_start in type String, in .constants.TIME_FORMAT format.
        :param str_date_end: data_end in type String. in .constants.TIME_FORMAT format.
        :param str_type: type of TimeSlot, choice field of .constants.RANGE_SLOT_TYPE
        :return: dict; field 'response_code' and useful Information.
            - a) 'response_code'=='405': RangeSlots overlap.
            - b) 'response_code'=='406': Some exception.
            - c) 'response_code'=='407': Doesn't exist.
            - d) 'response_code'=='200': if updated success.
        """
        ans = {}
        try:
            timeslot_id = int(str_timeslot_id)
            tutor_id = int(str_tutor_id)
            date_start = self._str_to_datetime(str_date_start)
            date_end = self._str_to_datetime(str_date_end)
            try:
                timeslot = RangeSlot.objects.get(id=timeslot_id)
            except Exception, e:
                ans['response_code'] = '407'
                return ans

            if timeslot.pattern is not None:
                # Can't edit periodic timeslot
                RangeSlot.objects.filter(id=timeslot_id).update(
                    type=str_type
                )
                ans['hint'] = "Accepted only 'type'."
                ans['response_code'] = '200'
                return ans

            tutor, created = Tutor.objects.get_or_create(id=tutor_id)
            if RangeSlot.objects. \
                    filter(tutor=tutor). \
                    filter(date__overlap=DateTimeTZRange(date_start, date_end)). \
                    exclude(id=timeslot_id). \
                    exists():
                ans['response_code'] = '405'
                return ans
            else:
                self._change_bin_dayslot(timeslot.date.lower, timeslot.date.upper, timeslot.tutor.id, 0)
                RangeSlot.objects.filter(id=timeslot_id).update(
                    tutor=tutor,
                    date=DateTimeTZRange(date_start, date_end),
                    type=str_type,
                    lesson_id=str_lesson_id
                )
                self._change_bin_dayslot(date_start, date_end, timeslot.tutor.id, 1)
                ans['response_code'] = '200'
                return ans
        except Exception, e:
            logger.error(e, exc_info=True)
            ans['response_code'] = '406'
            ans['error'] = str(e)
            return ans

    def delete_timeslot(self, str_timeslot_id):
        """
        Delete RangeSlot and BinSlot.

        :param str_timeslot_id: RangeSlot's id, type: string.
        :return:
            - a) 'response_code'=='406': Some exception.
            - b) 'response_code'=='407': Doesn't exist.
            - c) 'response_code'=='200': if deleted success.
        """
        ans = {}
        try:
            timeslot_id = int(str_timeslot_id)
            if not RangeSlot.objects.filter(id=timeslot_id).exists():
                ans['response_code'] = '407'
                return ans
            else:
                pattern = RangeSlot.objects.get(id=timeslot_id).pattern
                if pattern is None:
                    timeslot = RangeSlot.objects.get(id=timeslot_id)
                    self._change_bin_dayslot(timeslot.date.lower, timeslot.date.upper, timeslot.tutor.id, 0)
                    RangeSlot.objects.filter(id=timeslot_id).delete()
                else:
                    # timeslots = pattern.rangeslot_set.filter(
                    #     date__fully_gt=DateTimeTZRange(datetime.now(), datetime.now()))
                    timeslots = pattern.rangeslot_set.filter(id__gte=timeslot_id)

                    for timeslot in timeslots:
                        self._change_bin_dayslot(timeslot.date.lower, timeslot.date.upper, timeslot.tutor.id, 0)
                        RangeSlot.objects.filter(id=timeslot.id).delete()

                    pattern.delete()
                ans['response_code'] = '200'
                return ans
        except Exception, e:
            logger.error(e, exc_info=True)
            ans['response_code'] = '406'
            ans['error'] = str(e)
            return ans

    def get_timeslot(self, str_timeslot_id):
        """
        Get RangeSlot and BinSlot.

        :param str_timeslot_id: RangeSlot's id, type: string.
        :return:
            - b) 'response_code'=='406': Some exception.
            - c) 'response_code'=='407': Doesn't exist.
        """
        ans = {}
        try:
            timeslot_id = int(str_timeslot_id)
            if not RangeSlot.objects.filter(id=timeslot_id).exists():
                ans['response_code'] = '407'
                return ans
            else:
                timeslot = RangeSlot.objects.get(id=timeslot_id)
                ans['tutor_id'] = timeslot.tutor.id
                if timeslot.pattern is None:
                    ans['pattern'] = ''
                else:
                    ans['pattern'] = timeslot.pattern.mask
                ans['date_start'] = self._datetime_to_str(timeslot.date.lower)
                ans['date_end'] = self._datetime_to_str(timeslot.date.upper)
                ans['type'] = timeslot.type
                # 2.0
                ans['lesson_id'] = timeslot.lesson_id
                ans['tutoring_id'] = timeslot.tutoring_id
                ans['student_name'] = timeslot.student_name
                ans['student_email'] = timeslot.student_email
                ans['extra_time'] = timeslot.extra_time
                ans['title'] = timeslot.title
                ans['comment'] = timeslot.comment
                return ans
        except Exception, e:
            logger.error(e, exc_info=True)
            ans['response_code'] = '406'
            ans['error'] = str(e)
            return ans

    def _change_bin_dayslot(self, date_start, date_end, tutor_id, value):
        """
        Change binmask to 'value'.

        :param date_start: data_start in type datetime.
        :param date_end: data_end in type datetime.
        :param tutor_id: Tutor's id, type: int.
        :param value: int [1, 0].
        :return: None.

        """
        midnight = date_start.replace(hour=0, minute=0) + timedelta(days=1)
        if date_start < midnight < date_end:
            self._change_bin_dayslot(date_start, midnight, tutor_id, value)
            self._change_bin_dayslot(midnight, date_end, tutor_id, value)
            return

        midday = date_start.replace(hour=12, minute=0)
        if date_start < midday < date_end:
            self._change_bin_dayslot(
                date_start=date_start,
                date_end=date_end.replace(hour=12, minute=0),
                tutor_id=tutor_id,
                value=value
            )
            self._change_bin_dayslot(
                date_start=date_start.replace(hour=12, minute=0),
                date_end=date_end,
                tutor_id=tutor_id,
                value=value
            )
        else:
            date, bitmask, am = self._get_bitmask(date_start, date_end)
            try:
                day_bin, created = BinSlot.objects.get_or_create(
                    date=date,
                    tutor_id=tutor_id
                )
            except Exception, e:
                logger.error(e, exc_info=True)
            else:
                if am:
                    if value == 1:
                        day_bin.bin_am |= bitmask
                    else:
                        day_bin.bin_am &= ~bitmask
                else:
                    if value == 1:
                        day_bin.bin_pm |= bitmask
                    else:
                        day_bin.bin_pm &= ~bitmask
                day_bin.save()

    def _get_bitmask(self, date_start, date_end):
        """
        Transform date_start, date_end to bin presentation.

        :param date_start: data_start in type datetime.
        :param date_end: data_end in type datetime.
        :return: triple:
            1) date of TimeSlot, type: datetime.date().
            2) bitmask of TimeSlot, type: int.
            3) True if it's AM else False, type: Bool.
        """
        def _get_bit_of_time(time):
            """
            Get position of bit for time.

            :param time: time in datetime.time().
            :return: position of bit, type: int.
            """
            return time.hour % 12 * 4 + time.minute / 15

        ans_date = date_start.date()
        ans_bitmask = 0
        ans_am = True if date_start.time() < date_start.replace(hour=12, minute=0).time() else False

        left = _get_bit_of_time(date_start.time())
        right = _get_bit_of_time(date_end.time())
        right = 12 * 4 if right == 0 else right

        for i in range(left, right):
            ans_bitmask |= 1 << i
        return (ans_date, ans_bitmask, ans_am)

    def _get_free_tutors_by_bin(self, date_start, date_end):
        """
        Search Tutors by bitmask.

        :param date_start: data_start in type datetime.
        :param date_end: data_end in type datetime.
        :return: list of Tutor's id.
        """
        midnight = date_start.replace(hour=0, minute=0) + timedelta(days=1)
        if date_start < midnight < date_end:
            slots = self._get_free_tutors_by_bin(date_start, midnight)
            slots += self._get_free_tutors_by_bin(midnight, date_end)
            return slots

        midday = date_start.replace(hour=12, minute=0)
        if date_start < midday < date_end:
            slots = self._get_free_tutors_by_bin(
                date_start=date_start,
                date_end=date_end.replace(hour=12, minute=0),
            )
            slots += self._get_free_tutors_by_bin(
                date_start=date_start.replace(hour=12, minute=0),
                date_end=date_end,
            )
            return slots
        else:
            date, bitmask, am = self._get_bitmask(date_start, date_end)
            if am:
                slots = list(BinSlot.objects.filter(date=date, bin_am=F('bin_am').bitor(bitmask)).values('tutor'))
            else:
                slots = list(BinSlot.objects.filter(date=date, bin_pm=F('bin_pm').bitor(bitmask)).values('tutor'))
            return slots

    def _str_to_datetime(self, str_date):
        """
        Convert str_date in format(.constants.TIME_FORMAT) to datetime.

        :param str_date: date in format(.constants.TIME_FORMAT)
        :return: date in datetime.
        """
        return datetime.strptime(str_date, TIME_FORMAT).replace(tzinfo=pytz.utc)

    def _datetime_to_str(self, date):
        """
        Convert datetime to str_date in format(.constants.TIME_FORMAT).

        :param date: date in datetime
        :return: str_date in format(.constants.TIME_FORMAT) to datetime.
        """
        return date.strftime(TIME_FORMAT)
