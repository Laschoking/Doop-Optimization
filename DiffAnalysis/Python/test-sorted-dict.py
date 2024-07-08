from sortedcontainers import SortedList,SortedDict


if __name__ == "__main__":
    l = SortedDict()
    l[("a","b")] = 1
    l[("a", "a")] = 2
    print(l)