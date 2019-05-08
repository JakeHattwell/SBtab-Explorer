def sum(nums) :
    total = 0
    if len(nums) == 0 :
        return 0
    elif len(nums) == 1:
        return nums[0]
    return (sum(nums[:len(nums) // 2]) + sum(nums[len(nums) // 2:]))
