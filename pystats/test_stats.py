import time
import unittest
import mock
import stats


class TestStats(unittest.TestCase):
    def setUp(self):
        self.s = stats.Stats()

    def test_incr(self):
        self.s.incr('k')
        self.assertEqual(self.s['k'], 1, 'Error adding first value')
        self.s.incr('k')
        self.s.incr('d')
        self.assertEqual(self.s['k'], 2)
        self.assertEqual(self.s['d'], 1)

    def test_append(self):
        self.s.append('k', 'foo')
        self.assertEqual(self.s['k'], ['foo'])
        self.s.append('k', 'bar')
        self.s.append('d', 'baz')
        self.assertEqual(self.s['k'], ['foo', 'bar'])
        self.assertEqual(self.s['d'], ['baz'])

    def test_avg(self):
        self.s.avg('k', 10)
        self.assertEqual(self.s['k'].value(), 10)
        self.s.avg('k', 20)
        self.assertEqual(self.s['k'].value(), 15)
        self.s.avg('k', 30)
        self.assertEqual(self.s['k'].value(), 20)

    def test_gauge(self):
        for i in range(1, 4):
            self.s.gauge('k', i)
            self.assertEqual(self.s['k'], i)

    def test_rolling_average(self):
        self.s.rolling_avg('k', 10, 2)
        self.assertEqual(self.s['k'].value(), 10)
        self.s.rolling_avg('k', 20, 2)
        self.assertEqual(self.s['k'].value(), 15)
        self.s.rolling_avg('k', 30, 2)
        self.assertEqual(self.s['k'].value(), 25)

    @mock.patch('time.time', mock.Mock(return_value=0))
    def test_timer(self):
        with self.s.timer('k'):
            time.time.return_value = 10
            pass
        self.assertEqual(self.s['k'], 10)


if __name__ == '__main__':
    unittest.main()
