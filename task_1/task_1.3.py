class Solution:
    def intersection(self, nums1, nums2):
        nums1, nums2 = set(nums1), set(nums2)
        return list(nums1.intersection(nums2))