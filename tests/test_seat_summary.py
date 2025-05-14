import unittest

from elections_lk import SeatSummary


class TestCase(unittest.TestCase):
    def test_seat_summary(self):
        seat_summary = SeatSummary(total_seats=10)
        self.assertEqual(seat_summary.total_seats, 10)
