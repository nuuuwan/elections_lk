import unittest

from elections_lk import ElectionPresidential, ProjectionSeries


class TestProjectionSeries(unittest.TestCase):
    def test_build(self):
        elections = ElectionPresidential.list_all()
        series = ProjectionSeries(
            train_elections=elections[:-1],
            test_elections=elections[-1:],
        )
        x = series.build()
        n = len(elections[-1].results)
        self.assertEqual(len(x), n - ProjectionSeries.MIN_M)
