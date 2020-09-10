class strco:
    def Dam(arr, s):
        inf = float("inf")
        ans = 5
        ind = -1
        for ir, a in enumerate(arr):
            d = [[inf for j in range(len(a) + 1)] for i in range(len(s) + 1)]
            d[0][1] = 0
            d[1][0] = 0
            d[0][0] = 0
            for i in range(1, len(s) + 1):
                for j in range(1, len(a) + 1):
                    d[i][j] = min(d[i - 1][j] + 1,
                                  d[i][j - 1] + 1,
                                  d[i - 1][j - 1] + (a[j - 1] != s[i - 1]))
                    if (i != 1 and
                        j != 1 and
                        s[i - 1] == a[j - 2] and
                        s[i - 2] == a[j - 1]):
                        d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
            if (d[-1][-1] < ans):
                ans = d[-1][-1]
                ind = ir
        return ind
