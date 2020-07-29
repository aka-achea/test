from random import randint
from timeit import repeat

def run_sorting_algorithm(algorithm, array):
    # 调用特定的算法对提供的数组执行。
    # 如果不是内置sort()函数，那就只引入算法函数。
    setup_code = f"from __main__ import {algorithm}" \
        if algorithm != "sorted" else ""

    stmt = f"{algorithm}({array})"

    # 十次执行代码，并返回以秒为单位的时间
    times = repeat(setup=setup_code, stmt=stmt, repeat=3, number=10)

    # 最后，显示算法的名称和运行所需的最短时间
    print(f"Algorithm: {algorithm}. Minimum execution time: {min(times)}")

def bubble_sort(array):
    n = len(array)

    for i in range(n):
        # 创建一个标识，当没有可以排序的时候就使函数终止。
        already_sorted = True

        # 从头开始逐个比较相邻元素，每一次循环的总次数减1，
        # 因为每次循环一次，最后面元素的排序就确定一个。
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                # 如果此时的元素大于相邻后一个元素，那么交换。
                array[j], array[j + 1] = array[j + 1], array[j]

                # 如果有了交换，设置already_sorted标志为False算法不会提前停止
                already_sorted = False

        # 如果最后一轮没有交换，数据已经排序完毕，退出
        if already_sorted:
            break
        print(array)
    return array

def insertion_sort(array, left=0, right=None):
    if right is None:
        right = len(array) - 1

    # 从指示的left元素循环，直到right被指示
    for i in range(left + 1, right + 1):
        # 这个是我们想要放在正确位置的元素
        key_item = array[i]

        # 初始化变量，用于寻找元素正确位置
        j = i - 1
        # 遍历元素左边的列表元素，一旦key_item比被比较元素小，那么找到正确位置插入
        while j >= left and array[j] > key_item:
            # 把被检测元素向左平移一个位置，并将j指向下一个元素（从右向左）
            array[j + 1] = array[j]
            j -= 1

        # 当完成元素位置的变换，把key_item放在正确的位置上
        array[j + 1] = key_item
    return array

def merge(left, right):
    # 如果第一个数组为空，那么不需要合并，
    # 可以直接将第二个数组返回作为结果
    if len(left) == 0:
        return right
    # 如果第二个数组为空，那么不需要合并，
    # 可以直接将第一个数组返回作为结果
    if len(right) == 0:
        return left
    result = []
    index_left = index_right = 0

    # 查看两个数组直到所有元素都装进结果数组中
    while len(result) < len(left) + len(right):
        # 这些需要排序的元素要依次被装入结果列表，因此需要决定将从
        # 第一个还是第二个数组中取下一个元素
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        # 如果哪个数组达到了最后一个元素，那么可以将另外一个数组的剩余元素
        # 装进结果列表中，然后终止循环
        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break
    return result

def merge_sort(array):
    # 如果输入数组包含元素不超过两个，那么返回它作为函数结果
    if len(array) < 2:
        return array
    midpoint = len(array) // 2
    # 对数组递归地划分为两部分，排序每部分然后合并装进最终结果列表
    return merge(
        left=merge_sort(array[:midpoint]),
        right=merge_sort(array[midpoint:]))

def quicksort(array):
    # 如果第一个数组为空，那么不需要合并，
    # 可以直接将第二个数组返回作为结果
    if len(array) < 2:
        return array

    low, same, high = [], [], []

    # 随机选择 pivot 元素
    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        # 元素小于pivot元素的装进low列表中，大于piviot元素值的装进high列表中
        # 如果和pivot相等，则装进same列表中
        if item < pivot:
            low.append(item)
        elif item == pivot:
            same.append(item)
        elif item > pivot:
            high.append(item)

    # 最后的结果列表包含排序的low列表、same列表、hight列表
    return quicksort(low) + same + quicksort(high)

def timsort(array):
    min_run = 3
    n = len(array)
    print(array)

    # 开始切分、排序输入数组的小部分，切分在`min_run`定义
    for i in range(0, n, min_run):
        insertion_sort(array, i, min((i + min_run - 1), n - 1))
        print(array)
    print('='*10)
    # 现在可以合并排序的切分块了
    # 从`min_run`开始, 每次循环都加倍直到超过数组的长度
    size = min_run
    while size < n:
        # Determine the arrays that will
        # be merged together
        for start in range(0, n, size * 2):
            # 计算中点（第一个数组结束第二个数组开始的地方）和终点(第二个数组结束的地方)
            midpoint = start + size - 1
            end = min((start + size * 2 - 1), (n-1))

            # 合并两个子数组
            # left数组应该从起点到中点+1, right数组应该从中点+1到终点+1
            merged_array = merge(
                left=array[start:midpoint + 1],
                right=array[midpoint + 1:end + 1])

            # 最后，把合并的数组放回数组
            array[start:start + len(merged_array)] = merged_array
            print(array)
        # 每次迭代都应该让数据size加倍
        size *= 2

    return array





if __name__ == "__main__":
    array = [8,6,4,5,2,4,68,324,24,3]
    print(timsort(array))