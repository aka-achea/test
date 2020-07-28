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

def insertion_sort(array):
    # 从数据第二个元素开始循环，直到最后一个元素
    for i in range(1, len(array)):
        # 这个是我们想要放在正确位置的元素
        key_item = array[i]

        # 初始化变量，用于寻找元素正确位置
        j = i - 1

        # 遍历元素左边的列表元素，一旦key_item比被比较元素小，那么找到正确位置插入。
        while j >= 0 and array[j] > key_item:
            # 把被检测元素向左平移一个位置，并将j指向下一个元素（从右向左）
            array[j + 1] = array[j]
            j -= 1

        # 当完成元素位置的变换，把key_item放在正确的位置上
        array[j + 1] = key_item
        print(array)
    return array

if __name__ == "__main__":
    array = [8,6,4,5,2]
    insertion_sort(array)