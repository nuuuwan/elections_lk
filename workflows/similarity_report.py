from elections_lk import Similarity
from gig import Ent


def main():
    similarity = Similarity()
    idx = similarity.similarity_idx
    pd_id_list = similarity.pd_id_list

    def get_name(pd_i):
        pd_id = pd_id_list[pd_i]
        ent = Ent.from_id(pd_id)
        return ent.name.ljust(20)

    print('-' * 32)
    for (i, j), s in list(idx.items())[:10]:
        print(get_name(i), get_name(j), s)
    print('-' * 32)
    for (i, j), s in list(idx.items())[-10:]:
        print(get_name(i), get_name(j), s)
    print('-' * 32)


if __name__ == "__main__":
    main()
