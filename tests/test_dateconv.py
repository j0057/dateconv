import unittest

import dateconv

T = 392425860

class TestTime(unittest.TestCase):
    def test_to_struct_time_local(self):
        result = dateconv.to_struct_time_local(T)

        self.assertIsInstance(result, dateconv.time.struct_time)
        self.assertEqual(result[:6], (1982, 6, 9, 1, 11, 0))

    def test_to_struct_time_utc(self):
        result = dateconv.to_struct_time_utc(T)

        self.assertIsInstance(result, dateconv.time.struct_time)
        self.assertEqual(result[:6], (1982, 6, 8, 23, 11, 0))

    def test_from_struct_time_local(self):
        localtime = dateconv.to_struct_time_local(T)
        result = dateconv.from_struct_time_local(localtime)

        self.assertIsInstance(result, int)
        self.assertEqual(result, T)

    def test_from_struct_time_utc(self):
        gmtime = dateconv.to_struct_time_utc(T)
        result = dateconv.from_struct_time_utc(gmtime)

        self.assertIsInstance(result, int)
        self.assertEqual(result, T)

class TestDateTime(unittest.TestCase):
    def test_to_datetime_naive(self):
        result = dateconv.to_datetime_naive(T) 

        self.assertIsInstance(result, dateconv.datetime.datetime)
        self.assertEqual(result.year, 1982)
        self.assertEqual(result.month, 6)
        self.assertEqual(result.day, 9)
        self.assertEqual(result.hour, 1)
        self.assertEqual(result.minute, 11)
        self.assertEqual(result.second, 0)

    def test_to_datetime_local(self):
        result = dateconv.to_datetime_local(T)

        self.assertIsInstance(result, dateconv.datetime.datetime)
        self.assertEqual(result.year, 1982)
        self.assertEqual(result.month, 6)
        self.assertEqual(result.day, 9)
        self.assertEqual(result.hour, 1)
        self.assertEqual(result.minute, 11)
        self.assertEqual(result.second, 0)

        self.assertIsInstance(result.tzinfo, dateconv.datetime.tzinfo)
        self.assertNotEqual(result.tzinfo.tzname(result), "UTC") 

    def test_to_datetime_utc(self):
        result = dateconv.to_datetime_utc(T)

        self.assertIsInstance(result, dateconv.datetime.datetime)
        self.assertEqual(result.year, 1982)
        self.assertEqual(result.month, 6)
        self.assertEqual(result.day, 8)
        self.assertEqual(result.hour, 23)
        self.assertEqual(result.minute, 11)
        self.assertEqual(result.second, 0)

        self.assertIsInstance(result.tzinfo, dateconv.datetime.tzinfo)
        self.assertEqual(result.tzinfo.tzname(result), "UTC")

    def test_from_datetime_naive(self):
        datetime = dateconv.to_datetime_naive(T)
        result = dateconv.from_datetime_naive(datetime)
        self.assertIsInstance(result, int)

    def test_from_datetime_local(self):
        datetime = dateconv.to_datetime_local(T)
        result = dateconv.from_datetime_local(datetime)

        self.assertIsInstance(result, int)
        self.assertEqual(result, T)

    def test_from_datetime_utc(self):
        datetime = dateconv.to_datetime_local(T)
        result = dateconv.from_datetime_utc(datetime)

        self.assertIsInstance(result, int)
        self.assertEqual(result, T)

class TestISO8601(unittest.TestCase):
    def test_to_iso8601(self):
        result = dateconv.to_iso8601(T)

        self.assertIsInstance(result, str)
        self.assertEqual(result, '1982-06-08T23:11:00Z')

    def test_from_iso8601(self):
        result = dateconv.from_iso8601('1982-06-08T23:11:00Z')
        
        self.assertIsInstance(result, int)
        self.assertEqual(result, T)

class TestRFC822(unittest.TestCase):
    def test_to_rfc822(self):
        result = dateconv.to_rfc822(T)
    
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'Tue, 08 Jun 1982 23:11:00 GMT')

    def test_from_rfc822(self):
        result = dateconv.from_rfc822('Tue, 08 Jun 1982 23:11:00 GMT')

        self.assertIsInstance(result, int)
        self.assertEqual(result, T)

    def test_from_rfc822_wrong_1(self):
        with self.assertRaises(ValueError) as e:
            dateconv.from_rfc822('Albatross')
        self.assertEquals(e.exception.message, "Could not parse date 'Albatross'")

class TestPyEphem(unittest.TestCase):
    def test_to_pyephem(self):
        result = dateconv.to_pyephem(T)

        self.assertIsInstance(result, dateconv.ephem.Date)
        self.assertEqual(result.tuple()[:4], (1982, 6, 8, 23))

    def test_from_pyephem(self):
        pass
