from django.test import TestCase
from django.urls import reverse


class TimeSeriesViewTests(TestCase):
    def test_lon(self):
        """
        Longitude values are included in the range from -180 to 180: other values are not admitted and should
        return a 404 not found.
        """
        url = reverse('gpm:time_series', args=['something'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
