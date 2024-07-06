import unittest

from elections_lk import ElectionPresidential, ProjectionModel


class TestProjectionModel(unittest.TestCase):
    def test_train(self):
        elections = ElectionPresidential.list_all()
        train_elections = elections[:-1]
        test_elections = elections[-1:]
        x_pd_ids = ['EC-01A', 'EC-01B', 'EC-01C']

        model = ProjectionModel(
            train_elections, test_elections, x_pd_ids, 
        )

        self.assertEqual(model.X_train.shape, (18, 1))
        self.assertEqual(model.Y_train.shape, (18, 1))
        self.assertEqual(model.X_test.shape, (3, 1))
        self.assertEqual(model.Y_test.shape, (3, 1))

        model.train()
