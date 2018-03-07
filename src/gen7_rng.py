from pysfmt import SFMT


class Gen7RNG(object):
    def __init__(self, step):
        self.step = step

    def generate_needles(self, seed, N):
        sfmt = SFMT(seed)
        [sfmt.genrand_uint64() for _ in range(self.step)]
        needles = [sfmt.genrand_uint64() % 17 for _ in range(N)]
        return needles

    def calc_encoded_needle(self, seed):
        needles = self.generate_needles(seed, 7)
        return self.encode_needle(needles)

    @staticmethod
    def encode_needle(needles):
        needles = reversed(needles[:7])
        return sum([x * 17 ** i for i, x in enumerate(needles)])

    def ok(self, seed, inputs):
        needles = self.generate_needles(seed, len(inputs))
        return inputs == needles

    def _load_seed(self, db, pos):
        return int.from_bytes(db[4 * pos:4 * pos + 4], 'little')

    def search_seed(self, inputs, db):
        encoded_needle = self.encode_needle(inputs)
        lb, ub = 0, len(db) // 4

        while ub - lb > 1:
            mid = (ub + lb) // 2
            seed = self._load_seed(db, mid)
            cand = self.calc_encoded_needle(seed)

            if cand <= encoded_needle:
                lb = mid
            else:
                ub = mid

        results = []
        while True:
            seed = self._load_seed(db, lb)
            cand = self.calc_encoded_needle(seed)
            cand_needle = self.generate_needles(seed, len(inputs))
            if cand == encoded_needle:
                if cand_needle == inputs:
                    results.append(seed)
            else:
                break
            lb -= 1

        return results
