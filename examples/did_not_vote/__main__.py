import os
from functools import cached_property

from utils import JSONFile, _

from elections_lk import ElectionParliamentary, Party


class DidNotVote:
    @cached_property
    def idx_nocache(self):
        idx = {}
        for election in reversed(ElectionParliamentary.list_all()):
            lk_result = election.lk_result
            total = lk_result.vote_summary.electors
            if total == 0:
                continue
            p_dnv = (total - lk_result.vote_summary.valid) / total

            d = dict(dnv=p_dnv)
            for (
                party,
                votes,
            ) in lk_result.party_to_votes.get_party_to_votes_othered(
                0.1
            ).items():
                d[party] = votes / total

            d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))

            idx[election.year] = d
        return idx

    @cached_property
    def idx(self):
        idx_path = os.path.join("examples", "did_not_vote", "idx.json")
        idx_file = JSONFile(idx_path)
        if idx_file.exists:
            return idx_file.read()

        idx = self.idx_nocache
        idx_file.write(idx)
        return idx

    def draw_rect(self):

        return _(
            "rect",
            None,
            dict(
                x=0,
                y=0,
                width=1,
                height=1,
                fill="white",
                stroke="black",
                stroke_width=0.01,
            ),
        )

    def draw_chart(self):
        idx = self.idx
        n = len(idx.keys())
        inner = []
        PADDING = 0.1
        SCALE = 1 - 2 * PADDING
        BAR_HEIGHT = SCALE / n
        for i_year, (year, d) in enumerate(idx.items()):
            y_year = i_year * BAR_HEIGHT + PADDING
            inner.append(
                _(
                    "text",
                    f"{year}",
                    dict(
                        x=0.02,
                        y=y_year + BAR_HEIGHT / 2,
                        fill="black",
                        font_size=0.03,
                        dominant_baseline="middle",
                    ),
                ),
            )
            cum_p = 0
            for j_party, (party_code, p) in enumerate(d.items()):
                party = Party.from_code(party_code)
                inner.append(
                    _(
                        "g",
                        [
                            _(
                                "rect",
                                None,
                                dict(
                                    x=SCALE * cum_p + PADDING,
                                    y=y_year,
                                    width=SCALE * p,
                                    height=SCALE / n,
                                    fill=party.color,
                                    stroke="white",
                                    stroke_width=0.001,
                                ),
                            ),
                            _(
                                "text",
                                f"{p:.0%} {party_code.upper()}",
                                dict(
                                    x=SCALE * cum_p + PADDING * 1.05,
                                    y=y_year + BAR_HEIGHT / 2,
                                    fill="white",
                                    font_size=0.1 * p,
                                    dominant_baseline="middle",
                                ),
                            ),
                        ],
                    )
                )
                cum_p += p

        return _("g", inner)

    def draw_text(self):
        return _(
            "g",
            [
                _(
                    "text",
                    "Sri Lankan Parliamentary Elections",
                    dict(
                        x=0.5,
                        y=0.05,
                        font_size=0.05,
                        text_anchor="middle",
                        fill="black",
                        dominant_baseline="middle",
                    ),
                ),
                _(
                    "text",
                    "DNV = Did Not Vote or Vote Rejected",
                    dict(
                        x=0.5,
                        y=0.95,
                        font_size=0.05,
                        text_anchor="middle",
                        fill=Party.from_code("dnv").color,
                        dominant_baseline="middle",
                    ),
                ),
            ],
        )

    def draw(self):
        svg = _(
            "svg",
            [self.draw_rect(), self.draw_chart(), self.draw_text()],
            dict(
                viewBox="0 0 1 1",
                width="900",
                height="900",
                font_family="BahnSchrift",
            ),
        )
        svg_path = os.path.join("examples", "did_not_vote", "did_not_vote.svg")
        svg.store(svg_path)
        return svg_path


def main():
    os.startfile(DidNotVote().draw())


if __name__ == "__main__":
    main()
