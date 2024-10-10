from elections_lk import Party


def main():
    unp = Party.from_code("UNP")
    print(unp.code, unp.color)


if __name__ == "__main__":
    main()
