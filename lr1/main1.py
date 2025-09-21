nums, target = [2, 7, 11, 15], 9


def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if str(nums[i]) == nums[i] or str(nums[j]) == nums[j] or str(target) == target:
                return 'Неверный тип данных'
            else:
                if int(nums[i]) != nums[i] or int(nums[j]) != nums[j] or int(target) != target:
                    return 'Неверный тип данных'
                if nums[i] + nums[j] == target:
                    return [i, j]
                    break


print(two_sum(nums, target))
