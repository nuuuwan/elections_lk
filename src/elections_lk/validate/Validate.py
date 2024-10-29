from utils import Log

from elections_lk.core import ElectionParliamentary, ElectionPresidential

log = Log("Validate")


class Validate:
    @staticmethod
    def party_to_votes(election, result, party_to_votes):
        for party, votes in party_to_votes.items():
            assert votes >= 0, (party, votes)

    @staticmethod
    def summary(election, result, summary):
        for checker, label in [
            (lambda summary: summary.electors > 0, "electors > 0"),
            (
                lambda summary: summary.electors >= summary.polled,
                "electors >= polled",
            ),
            # (
            #     lambda summary: summary.valid + summary.rejected
            #     == summary.polled,
            #     "valid + rejected == polled",
            # ),
        ]:
            if not checker(summary):
                log.error(f"[{label}] {election.title} {result.id} {summary}")

    @staticmethod
    def result(election, result):
        Validate.summary(election, result, result.vote_summary)
        Validate.party_to_votes(election, result, result.party_to_votes)

    @staticmethod
    def single(election):
        log.debug(f"Validating {election.title}")
        for result in election.pd_results:
            Validate.result(election, result)

    @staticmethod
    def run():
        elections = (
            ElectionParliamentary.list_all() + ElectionPresidential.list_all()
        )
        for election in elections:
            Validate.single(election)


if __name__ == "__main__":
    Validate.run()
