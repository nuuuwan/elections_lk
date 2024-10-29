import colorsys
import os
from functools import cache, cached_property

from gig import Ent, EntType
from PIL import Image, ImageDraw, ImageFont
from utils import Log, TSVFile

from elections_lk import ElectionParliamentary, ElectionPresidential

log = Log("Correlation")


class Correlation:
    @cached_property
    def elections(self):
        return (
            ElectionParliamentary.list_all() + ElectionPresidential.list_all()
        )

    @cached_property
    def id_to_label(self):
        pd_ents = Ent.list_from_type(EntType.PD)
        ed_ents = Ent.list_from_type(EntType.ED)

        return (
            {ent.id: ent.name for ent in pd_ents}
            | {ent.id + "P": "Postal " + ent.name for ent in ed_ents}
            | {"LK": "Sri Lanka"}
        )

        # ed_ents = Ent.list_from_type(EntType.ED)

        # return {ent.id: ent.name for ent in ed_ents} | {"LK": "Sri Lanka"}

    @cached_property
    def id_list(self):
        return sorted(list(self.id_to_label.keys()))

    @cache
    def get_label(self, id):
        label = self.id_to_label.get(id)
        return id.replace("EC-", "") + "-" + label

    @cache
    def get_lk_party_list(self, election):
        lk_result = election.lk_result
        return [
            party
            for party in lk_result.party_to_votes.keys()
            if lk_result.party_to_votes.p(party) > 0.01
        ]

    @cache
    def get_feature_for_id(self, region_id):
        idx = {}
        for election in self.elections:
            try:
                result = election.get_result(region_id)
            except BaseException as e:
                log.error(f"[{election.year}]: {e}")
                result = None
            for party in self.get_lk_party_list(election):
                k = f"{election.year}-{party}"
                idx[k] = (
                    round(result.party_to_votes.p(party), 2) if result else 0
                )
        return idx

    @staticmethod
    @cache
    def get_distance(f1, f2):
        d = 0
        total_d = 0
        for f1i, f2i in zip(f1, f2):
            d += abs(f1i - f2i) * f1i
            total_d += f1i
        return round(d / total_d, 2)

    @cached_property
    def d_list(self):

        sorted_id_list = self.sorted_id_list

        d_list = []
        for id1 in sorted_id_list:
            d = {"id": self.get_label(id1)}
            f1 = tuple(self.get_feature_for_id(id1).values())

            for id2 in sorted_id_list:
                f2 = tuple(self.get_feature_for_id(id2).values())
                d[self.get_label(id2)] = Correlation.get_distance(f1, f2)
            d_list.append(d)

        return d_list

    def write(self):
        tsv_path = os.path.join("analysis_output", "correlation.tsv")
        TSVFile(tsv_path).write(self.d_list)
        log.info(f'Wrote to "{tsv_path}"')

    @cached_property
    def sorted_id_list(self):
        return sorted(
            self.id_list,
            key=lambda x: Correlation.get_distance(
                tuple(self.get_feature_for_id("LK").values()),
                tuple(self.get_feature_for_id(x).values()),
            ),
        )

    @staticmethod
    def get_color(distance):

        MAX_DISTANCE_FOR_COLOR = 0.1
        if distance < MAX_DISTANCE_FOR_COLOR:
            return (255, int(255 * distance / MAX_DISTANCE_FOR_COLOR), 0)

        return None

    def draw(
        self,
        unit_dim=20,
        title_dim=200,
        header_height=100,
        font_size=20,
        dpi=(75, 75),
    ):

        n = len(self.id_list)
        width = n * unit_dim + title_dim
        height = width + header_height

        im = Image.new("RGB", (width, height), (255, 255, 255))

        for i, d in enumerate(self.d_list):
            for j, v in enumerate(list(d.values())[1:]):
                color = Correlation.get_color(v)
                if not color:
                    continue

                x1 = title_dim + i * unit_dim
                y1 = header_height + title_dim + j * unit_dim
                x2 = x1 + unit_dim
                y2 = y1 + unit_dim
                im.paste(color, (x1, y1, x2, y2))

        draw = ImageDraw.Draw(im)

        font_path = os.path.join("fonts", "UbuntuMono-Regular.ttf")
        font = ImageFont.truetype(font_path, size=font_size)

        for i, id in enumerate(self.sorted_id_list):
            label = self.get_label(id)
            x = title_dim + i * unit_dim
            y = header_height

            im_txt = Image.new("RGB", (title_dim, unit_dim), (255, 255, 255))
            im_txt_draw = ImageDraw.Draw(im_txt)
            im_txt_draw.text((0, 0), label, font=font, fill="black")
            im_txt = im_txt.rotate(90, expand=1)
            im.paste(im_txt, (x, y))

            x = 0
            y = header_height + title_dim + i * unit_dim
            draw.text((x, y), label, fill="black", font=font)

        draw.text(
            (0, 0),
            "Sri Lankan Presidential & Parliamentary Elections",
            fill="black",
            font=font,
        )

        draw.text(
            (0, header_height / 2),
            "Election Results Difference",
            fill="black",
            font=font,
        )

        image_path = os.path.join("analysis_output", "correlation.png")
        im.save(image_path, dpi=dpi)
        size_m = round(os.path.getsize(image_path) / 1024 / 1024, 2)
        log.info(f'Wrote to "{image_path} ({size_m} MB)"')


if __name__ == "__main__":
    c = Correlation()
    c.write()
    c.draw()
