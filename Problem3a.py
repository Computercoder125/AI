#Sean Gor
#Problem 3: Leetcode problem to return the greatest number of stones Allison can get when playing a Nim game with one other player

from functools import lru_cache #import statements
from itertools import accumulate
from typing import List
class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        # Suffix sums: S[i] = sum(piles[i:])
        S = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            S[i] = S[i + 1] + piles[i]

        @lru_cache(maxsize=None)
        def dfs(i, M):
            if i >= n:
                return 0  # no stones left, no margin
            best = float('-inf')
            # Try taking x piles, up to 2M or until end
            limit = min(2 * M, n - i)
            for x in range(1, limit + 1):
                take = S[i] - S[i + x]
                # negamax step: current gain minus opponent's best margin next
                best = max(best, take - dfs(i + x, max(M, x)))
            return best

        diff = dfs(0, 1)           # Alice − Bob with optimal play
        total = S[0]
        return (total + diff) // 2  # Alice's stones
    
if __name__ == "__main__":    
    piles =  [2,7,9,4,4]
    print(Solution().stoneGameII(piles))