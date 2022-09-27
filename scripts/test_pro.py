import math
from typing import List


class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        s = set()
        p1 = p2 = 0

        while True:
            if p2 > k or p2 >= len(nums):
                break
            for l in s:
                if math.fabs(nums[p2]-l) <= t:
                    return True
            s.add(nums[p2])
            p2+=1

        while True:
            print(s)
            if p2 >= len(nums):
                break
            p1 = p2-k-1
            s.remove(nums[p1])
            for l in s:
                if math.fabs(nums[p2]-l) <= t:
                    return True
            s.add(nums[p2])
            p2+=1
            p1+=1
        return False


s = Solution()
print(s.containsNearbyAlmostDuplicate([1], 1, 1))