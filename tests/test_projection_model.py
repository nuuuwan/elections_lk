import unittest

from elections_lk import ElectionPresidential, ProjectionModel


class TestProjectionModel(unittest.TestCase):
    def test_train(self):
        elections = ElectionPresidential.list_all()
        train_elections = elections[:-1]
        test_elections = elections[-1:]
        x_pd_ids = ['EC-01A', 'EC-01B', 'EC-01C']
        y_pd_ids = ['EC-01D']

        m_x = len(x_pd_ids)
        m_y = len(y_pd_ids)
        n_train = 18
        n_test = 3

        model = ProjectionModel(
            train_elections, test_elections, x_pd_ids, y_pd_ids
        )

        self.assertEqual(model.X_train.shape, (n_train, m_x))
        self.assertEqual(model.Y_train.shape, (n_train, m_y))
        self.assertEqual(model.X_test.shape, (n_test, m_x))
        self.assertEqual(model.Y_test.shape, (n_test, m_y))

        model.train()
