import os
from functools import cache, cached_property

from gig import Ent, EntType
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans
from utils import Log

from elections_lk.core import ElectionParliamentary, ElectionPresidential
from utils_future import AnimatedGIF

log = Log("Correlation")


class Correlation:
    def __init__(self, mode, limit, n_clusters):
        self.mode = mode
        self.limit = limit
        self.n_clusters = n_clusters

    @cached_property
    def prefix(self):
        return f"{self.mode}-{self.n_clusters}-correlation"

    @cached_property
    def elections(self):
        elections = (
            ElectionParliamentary.list_all() + ElectionPresidential.list_all()
        )
        sorted_elections = sorted(elections, key=lambda e: e.year, reverse=True)
        if self.limit:
            sorted_elections = sorted_elections[: self.limit]
        log.info(f"Loaded {len(sorted_elections)} elections")
        return sorted_elections

    @cached_property
    def years(self):
        return sorted(set([election.year for election in self.elections]))

    @cached_property
    def id_to_label(self):
        if self.mode == "pd":
            pd_ents = Ent.list_from_type(EntType.PD)
            ed_ents = Ent.list_from_type(EntType.ED)

            return (
                {ent.id: ent.name for ent in pd_ents}
                | {ent.id + "P": ent.name + "(P)" for ent in ed_ents}
                | {"LK": "Sri Lanka"}
            )

        ed_ents = Ent.list_from_type(EntType.ED)
        return {ent.id: ent.name for ent in ed_ents} | {"LK": "Sri Lanka"}

    @cached_property
    def id_list(self):
        return sorted(list(self.id_to_label.keys()))

    @cached_property
    def cluster_to_id_list(self):
        id_list = self.id_list
        features = [self.get_feature_for_id(id) for id in id_list]
        kmeans = KMeans(
            n_clusters=self.n_clusters,
            n_init=30,
        ).fit(features)
        clusters = kmeans.labels_

        cluster_to_id = {}
        for cluster_id, id in zip(clusters, id_list):
            if cluster_id not in cluster_to_id:
                cluster_to_id[cluster_id] = []
            cluster_to_id[cluster_id].append(id)

        cluster_centroids = kmeans.cluster_centers_

        t_list = []
        for cluster_id, id_list in cluster_to_id.items():
            distance = Correlation.get_distance(
                tuple(cluster_centroids[cluster_id]),
                self.get_feature_for_id("LK"),
            )
            t_list.append((cluster_id, id_list, distance))

        sorted_t_list = sorted(t_list, key=lambda t: t[-1])

        sorted_cluster_to_id = {
            t[0]: sorted(
                t[1],
                key=lambda id: Correlation.get_distance(
                    self.get_feature_for_id(id), self.get_feature_for_id("LK")
                ),
            )
            for t in sorted_t_list
        }

        return sorted_cluster_to_id

    @cached_property
    def id_to_cluster(self):
        d = {}
        for cluster, id_list in self.cluster_to_id_list.items():
            for id in id_list:
                d[id] = cluster
        return d

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
        f = []
        for election in self.elections:
            try:
                result = election.get_result(region_id)
            except BaseException as e:
                log.error(f"[{election.year}]: {e}")
                result = None
            for party in self.get_lk_party_list(election):
                fi = round(result.party_to_votes.p(party), 2) if result else 0
                f.append(fi)
        return tuple(f)

    @staticmethod
    @cache
    def get_distance(f1, f2):
        d = 0
        total_d = 0
        for f1i, f2i in zip(f1, f2):
            d += abs(f1i - f2i) * f1i * f2i
            total_d += f1i * f2i
        return round(d / total_d, 2)

    @staticmethod
    def get_color(distance):

        MAX_DISTANCE_FOR_COLOR = 0.1
        if distance < MAX_DISTANCE_FOR_COLOR:
            return (255, int(255 * distance / MAX_DISTANCE_FOR_COLOR), 0)

        return None

    def draw(
        self,
        unit_dim=40,
        title_dim=400,
        cluster_gap_multiple=1,
        header_height=100,
        padding=100,
        font_size=40,
        dpi=(75, 75),
        max_n_clusters=23,
    ):

        n = len(self.id_list)

        width = (
            (n + max_n_clusters * cluster_gap_multiple) * unit_dim
            + title_dim
            + padding * 2
        )
        height = width + header_height

        im = Image.new("RGB", (width, height), (255, 255, 255))

        i1 = 0
        for i_cluster, id_list in enumerate(self.cluster_to_id_list.values()):
            for id1 in id_list:
                f1 = self.get_feature_for_id(id1)

                i2 = 0
                for i_cluster2, id_list2 in enumerate(
                    self.cluster_to_id_list.values()
                ):
                    for id2 in id_list2:
                        f2 = self.get_feature_for_id(id2)
                        distance = self.get_distance(f1, f2)

                        color = Correlation.get_color(distance)
                        if color:
                            x1 = (
                                padding
                                + title_dim
                                + (i_cluster * cluster_gap_multiple + i1)
                                * unit_dim
                            )
                            y1 = (
                                padding
                                + header_height
                                + title_dim
                                + (i_cluster2 * cluster_gap_multiple + i2)
                                * unit_dim
                            )

                            im.paste(
                                color, (x1, y1, x1 + unit_dim, y1 + unit_dim)
                            )
                        i2 += 1
                i1 += 1

        draw = ImageDraw.Draw(im)

        font_path = os.path.join("fonts", "UbuntuMono-Regular.ttf")
        font = ImageFont.truetype(font_path, size=font_size)

        i = 0
        for i_cluster, id_list in enumerate(self.cluster_to_id_list.values()):
            for id1 in id_list:

                x = (
                    padding
                    + title_dim
                    + (i + i_cluster * cluster_gap_multiple) * unit_dim
                )
                y = padding + header_height

                im_txt = Image.new(
                    "RGB", (title_dim, unit_dim), (255, 255, 255)
                )
                im_txt_draw = ImageDraw.Draw(im_txt)
                label = self.get_label(id1)
                im_txt_draw.text((0, 0), label, font=font, fill="black")
                im_txt = im_txt.rotate(90, expand=1)
                im.paste(im_txt, (x, y))

                x = padding
                y = (
                    padding
                    + header_height
                    + title_dim
                    + (i + i_cluster * cluster_gap_multiple) * unit_dim
                )
                draw.text((x, y), label, fill="black", font=font)

                i += 1

        draw.text(
            (padding, padding),
            "Sri Lankan Presidential & Parliamentary Elections",
            fill="black",
            font=font,
        )

        title = f"Election Results Difference by {self.mode.upper()}"
        if self.limit:
            title += f" (Top {self.limit})"

        draw.text(
            (padding, padding + header_height * 0.5),
            title,
            fill="black",
            font=font,
        )

        subtitle = self.years[0] + "-" + self.years[-1]

        draw.text(
            (padding, padding + header_height),
            subtitle,
            fill="black",
            font=font,
        )

        subtitle2 = f"{self.n_clusters} Cluster(s)"

        draw.text(
            (padding, padding + header_height * 1.5),
            subtitle2,
            fill="black",
            font=font,
        )

        image_path = os.path.join("analysis_output", f"{self.prefix}.png")
        im.save(image_path, dpi=dpi)
        size_m = round(os.path.getsize(image_path) / 1024 / 1024, 2)
        log.info(f'Wrote to "{image_path} ({size_m} MB)"')

        return image_path


if __name__ == "__main__":
    LIMIT = 11
    for mode in ["pd"]:
        image_path_list = []
        for n_clusters in range(1, 22 + 1 + 1):
            correlation = Correlation(
                mode=mode,
                n_clusters=n_clusters,
                limit=LIMIT,
            )
            image_path = correlation.draw()
            image_path_list.append(image_path)

        animated_gif_path = os.path.join(
            "analysis_output", f"{mode}-correlation.gif"
        )
        AnimatedGIF(image_path_list, duration_ms=1000).save(animated_gif_path)
        size_m = round(os.path.getsize(animated_gif_path) / 1024 / 1024, 2)
        log.info(f'Wrote to "{animated_gif_path}" ({size_m} MB)')
