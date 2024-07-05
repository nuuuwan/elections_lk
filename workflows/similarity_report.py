from elections_lk import Similarity
from gig import Ent
import random


def main():
    similarity = Similarity()
    idx = similarity.similarity_idx
    pd_id_list = similarity.pd_id_list

    def get_name(pd_i):
        pd_id = pd_id_list[pd_i]
        ent = Ent.from_id(pd_id)
        return ent.name.ljust(20)

    for (i, j), s in list(idx.items()):
        if random.random() < 0.01:
            print(get_name(i), get_name(j), round(s, 4))


if __name__ == "__main__":
    main()
