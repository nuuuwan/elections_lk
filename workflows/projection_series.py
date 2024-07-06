from utils import Log

from elections_lk import ElectionPresidential, ProjectionSeries

log = Log("projection_series")


def main():
    elections = ElectionPresidential.list_all()
    n = len(elections)
    for i in range(1, n):
        series = ProjectionSeries(
            train_elections=elections[:i],
            test_elections=elections[i : i + 1],
        )
        series.build()


if __name__ == "__main__":
    main()
