from subprocess import Popen, PIPE


def convert(n, add):
    return (n + add + 17) % 17


def replace(needles, idx, val):
    ret = list(needles)
    ret[idx] = val
    return ret


def gen_candidate_rec(pos, needles, fuzzy_pos, res):
    if len(needles) == pos:
        res.append(needles)
        return

    if pos in fuzzy_pos:
        for add in range(2):
            val = convert(needles[pos], add)
            gen_candidate_rec(
                pos + 1, replace(needles, pos, val), fuzzy_pos, res)
    else:
        gen_candidate_rec(pos + 1, needles, fuzzy_pos, res)


def gen_candidate(needles):
    num_needle = len(needles)

    fuzzy_pos = set()

    for i in range(num_needle):
        if needles[i][-1] == '?':
            fuzzy_pos.add(i)
            needles[i] = needles[i][:-1]

    needles = list(map(int, needles))

    res = []
    gen_candidate_rec(0, needles, fuzzy_pos, res)
    return res


def search(needles):
    needles = needles.split(",")

    p = Popen(['./search'], stdin=PIPE,
              stdout=PIPE, cwd='./lib/search-sfmt-seed')
    lines = "{} {}".format(len(needles), ' '.join(map(str, needles)))
    stdout, stderr = p.communicate(lines.encode('utf-8'))

    rets = [x.split() for x in stdout.decode('utf-8').split("\n") if x]
    results = [{'add': ret[3], 'seed': ret[0], 'encoded_needle': ret[1], 'step': ret[2]}
               for ret in rets]
    return results


if __name__ == '__main__':
    needles = "8,11,5,11?,8,10?,9?"
    needles = "03 00 16 12 13 04 01 09 13 13 14 13"
    import time
    s = time.time()
    print(search(needles))
    print(time.time() - s)
