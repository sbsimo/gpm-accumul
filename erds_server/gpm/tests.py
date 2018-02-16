from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class TimeSeriesViewTests(TestCase):
    def test_lon(self):
        """
        Longitude values are included in the range from -180 to 180: other values are not admitted and should
        return a 404 not found.
        """
        # random literal should be excluded
        kw = {'lat': '45.2', 'lon': 'random_text', 'time_period_hours': '12'}
        self.assertRaises(NoReverseMatch, reverse, 'gpm:time_series', kwargs=kw)

        # lon value out of range
        kw['lon'] = '190'
        url = reverse('gpm:time_series', kwargs=kw)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        # lon value in the valid range
        kw['lon'] = '7.8'
        url = reverse('gpm:time_series', kwargs=kw)
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 404])

    def test_lat(self):
        """
        Latitude values for GPM data are included in the range from -60 to 60: other values are not admitted and should
        return a 404 not found.
        """
        # random literal should be excluded
        kw = {'lat': 'random_text', 'lon': '7.8', 'time_period_hours': '12'}
        self.assertRaises(NoReverseMatch, reverse, 'gpm:time_series', kwargs=kw)

        # lon value out of range
        kw['lat'] = '61.2'
        url = reverse('gpm:time_series', kwargs=kw)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        # lon value in the valid range
        kw['lat'] = '45.2'
        url = reverse('gpm:time_series', kwargs=kw)
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 404])

    def test_time_period_hours(self):
        """
        Time periods must be positive integers.
        """
        # random literal should be excluded
        kw = {'lat': '45.2', 'lon': '7.8', 'time_period_hours': 'gibbone'}
        self.assertRaises(NoReverseMatch, reverse, 'gpm:time_series', kwargs=kw)

        kw['time_period_hours'] = '12.5'
        self.assertRaises(NoReverseMatch, reverse, 'gpm:time_series', kwargs=kw)

        # lon value in the valid range
        kw['time_period_hours'] = '12'
        url = reverse('gpm:time_series', kwargs=kw)
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 404])
