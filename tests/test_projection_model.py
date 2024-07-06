import random
import unittest

from elections_lk import ElectionPresidential, ProjectionModel


class TestProjectionModel(unittest.TestCase):
    def test_train(self):
        elections = ElectionPresidential.list_all()
        train_elections = elections[:-1]
        test_elections = elections[-1:]
        x_pd_ids = ['EC-01A', 'EC-01B', 'EC-01C']
        y_pd_ids = ['EC-01D', 'EC-01E', 'EC-01F']

        model = ProjectionModel(
            train_elections, test_elections, x_pd_ids, y_pd_ids
        )

        self.assertEqual(model.X_train.shape, (14, 1))
        self.assertEqual(model.Y_train.shape, (14, 1))
        self.assertEqual(model.X_test.shape, (2, 1))
        self.assertEqual(model.Y_test.shape, (2, 1))

        model.train()


    def test_complete(self):
        elections = ElectionPresidential.list_all()
        train_elections = elections[:-1]
        test_elections = elections[-1:]
        y_pd_ids = test_elections[0].pd_ids
        random.seed(0)
        random.shuffle(y_pd_ids)
        x_pd_ids = y_pd_ids[:-20]

        model = ProjectionModel(
            train_elections, test_elections, x_pd_ids, y_pd_ids
        )

        model.train()

        country_result = model.test_elections[0].country_result
        parties = country_result.party_to_votes.get_parties(0.1)

        Y_hat = model.evaluate(model.X_test)
        print(model.X_test)
        print(model.Y_test)
        print(Y_hat)

        for i_party, party in enumerate(parties):
            expected_p_votes = country_result.party_to_votes.p_dict[party]
            projected_p_votes = Y_hat[i_party][0]
            self.assertAlmostEqual(expected_p_votes, projected_p_votes, places=2)

