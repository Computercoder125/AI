class Solution:
    
    def stoneGameIII(self, stoneValue):
        n = len(stoneValue)
        dp = [0] * (n + 1)  # initialize array used for dynamic programming
        # Now, work backwards
        for i in range(n - 1, -1, -1):
            best = float('-inf')
            take = 0
            for k in range(3):
                if i + k < n:
                    take += stoneValue[i + k]
                    best = max(best, take - dp[i + k + 1])
            dp[i] = best

        if dp[0] > 0:
            return "Alice"
        if dp[0] < 0:
            return "Bob"
        return "Tie"
    
if __name__ == "__main__":    
    stoneValue = [1,2,3,7]
    print(Solution().stoneGameIII(stoneValue))