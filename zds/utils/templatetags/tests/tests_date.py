# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta

from django.test import TestCase
from django.template import Context, Template


class DateFormatterTest(TestCase):
    # todo: Add test with localization parameters

    def setUp(self):

        now = datetime.now()
        date_previous_in_day = now - timedelta(hours=1)
        date_previous_abs = datetime(2013, 9, 12, hour=11, minute=10, second=42, microsecond=10)
        date_future_in_day = now + timedelta(hours=1)
        yearlapse = now - timedelta(days=366)

        self.context = Context({"date_previous_in_day": date_previous_in_day,
                                "date_previous_abs": date_previous_abs,
                                "date_future_in_day": date_future_in_day,
                                "yearlapse": yearlapse,
                                "date_epoch": 42,
                                "NoneVal": None})

    def test_format_date(self):
        # Default behaviour
        tr = Template("{% load date %}"
                      "{{ date_previous_in_day | format_date }}"
                      ).render(self.context)
        self.assertEqual(u"il y a une heure", tr)

        tr = Template("{% load date %}"
                      "{{ date_future_in_day | format_date }}"
                      ).render(self.context)
        self.assertEqual(u"Dans le futur", tr)

        tr = Template("{% load date %}"
                      "{{ date_previous_abs | format_date }}"
                      ).render(self.context)
        self.assertEqual(u"jeudi 12 septembre 2013 à 11h10", tr)

        # small == False :=> Same behaviour
        tr = Template("{% load date %}"
                      "{{ date_previous_in_day | format_date:False }}"
                      ).render(self.context)
        self.assertEqual(u"il y a une heure", tr)

        tr = Template("{% load date %}"
                      "{{ date_future_in_day | format_date:False }}"
                      ).render(self.context)
        self.assertEqual(u"Dans le futur", tr)

        tr = Template("{% load date %}"
                      "{{ date_previous_abs | format_date:False }}"
                      ).render(self.context)
        self.assertEqual(u"jeudi 12 septembre 2013 à 11h10", tr)

        # small == True :=> absolute date change
        tr = Template("{% load date %}"
                      "{{ date_previous_in_day | format_date:True }}"
                      ).render(self.context)
        self.assertEqual(u"il y a une heure", tr)

        tr = Template("{% load date %}"
                      "{{ date_future_in_day | format_date:True }}"
                      ).render(self.context)
        self.assertEqual(u"Dans le futur", tr)

        tr = Template("{% load date %}"
                      "{{ date_previous_abs | format_date:True }}"
                      ).render(self.context)
        self.assertEqual(u"12/09/13 à 11h10", tr)

        # Bad format
        tr = Template("{% load date %}"
                      "{{ NoneVal | format_date }}"
                      ).render(self.context)
        self.assertEqual(u"None", tr)

    def test_tooltip_date(self):
        # Default behaviour

        # Todo: Add test to step time less than one day with tooltip
        # Todo: I don't know how to test this without hugly hack on datetime.now()

        tr = Template("{% load date %}"
                      "{{ date_future_in_day | tooltip_date }}"
                      ).render(self.context)
        self.assertEqual(u"Dans le futur", tr)

        tr = Template("{% load date %}"
                      "{{ yearlapse | tooltip_date }}"
                      ).render(self.context)
        self.assertEqual(u"il y a 1\xa0année", tr)

        # Bad format
        tr = Template("{% load date %}"
                      "{{ NoneVal | tooltip_date }}"
                      ).render(self.context)
        self.assertEqual(u"None", tr)

    def test_humane_time(self):

        # Default behaviour
        tr = Template("{% load date %}"
                      "{{ date_epoch | humane_time }}"
                      ).render(self.context)

        # Since ZdS is in Europe/Paris, hours can be 1 or 2
        is_dst = time.daylight and time.localtime().tm_isdst > 0
        utc_offset_sec = time.altzone if is_dst else time.timezone
        hours = -1 * utc_offset_sec / 3600

        self.assertEqual(tr, u"jeudi 01 janvier 1970 à 0{}h00".format(hours))
