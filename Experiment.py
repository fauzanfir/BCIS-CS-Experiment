import math
import numpy as np
import time
import tracemalloc
from memory_profiler import profile

def swap(array, i, j):
    tmp = array[i]
    array[i] = array[j]
    array[j] = tmp
    return array

def isequal(array, sl, sr):
    for k in range(sl + 1, sr - 1):
        if array[k] != array[sl]:
            array = swap(array, k, sl)
            return k
    return -1

def insert_right(array, item, sr, right):
    j = sr
    while (j <= right) and (item > array[j]):
        array[j-1] = array[j]
        j += 1
    array[j-1] = item
    return array

def insert_left(array, item, sl, left):
    j = sl
    while (j >= left) and (item < array[j]):
        array[j+1] = array[j]
        j -= 1
    array[j+1] = item
    return array

def BCIS(array):
    start = time.time()
    sl = 0
    sr = len(array) - 1
    while sl < sr:
        i = sl + 1
        array = swap(array, sr, sl + ((sr - sl) // 2))
        if array[sl] == array[sr]:
            if isequal(array, sl, sr) != -1:
                return array, (time.time() - start) * (10 ** 3)
            
        if array[sl] > array[sr]:
            array = swap(array, sl, sr)

        if (sr - sl) >= 100:
            for i_ in range(sl + 1, int((sr - sl) ** (0.5))):
                if array[sr] < array[i_]:
                    array = swap(array, sr, i_)
                elif array[sl] > array[i_]:
                    array = swap(array, sl, i_)
                i += 1

        lc = array[sl]
        rc = array[sr]

        while i < sr:
            curr_item = array[i]
            if curr_item >= rc:
                array[i] = array[sr - 1]
                array = insert_right(array, curr_item, sr, len(array) - 1)
                sr -= 1
            elif curr_item <= lc:
                array[i] = array[sl + 1]
                array = insert_left(array, curr_item, sl, 0)
                sl += 1
                i += 1
            else:
                i += 1
        sl += 1
        sr -= 1
    return array, (time.time() - start) * (10 ** 3)

def counting_sort(array):
    start = time.time()
    B = [0 for i in range(len(array))]
    k = max(array)
    C = [0 for i in range(k + 1)]

    for j in range(len(array)):
        C[array[j]] += 1
    
    for i in range(1, k + 1):
        C[i] += C[i-1]
    
    for j in range(len(array)-1, -1, -1):
        B[C[array[j]]-1] = array[j]
        C[array[j]] -= 1
    
    return B, (time.time() - start) * (10 ** 3)
    
def file_to_list(filename):
    fileobj=open(filename)
    lines=fileobj.readlines()
    lines=[int(line.strip()) for line in lines]
    return lines

def run_experiment(datasets_num):
    for num in datasets_num:
        dataset = file_to_list("dataset_" + str(num) + ".txt")
        dataset_sorted = np.sort(dataset)
        dataset_reversed = dataset_sorted[::-1]

        print("-------------------------------------------------------")
        print("Dataset with %d numbers unsorted:" % (num))

        tracemalloc.start()
        sorted_dataset, time_1 = BCIS(dataset)
        mem1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("- BCIS executed in %f ms" % (time_1))
        print("- BCIS memory consumption is %s bytes" % (str(mem1[1])))

        tracemalloc.start()
        counting_sorted_dataset, time_4 = counting_sort(dataset)
        mem4 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("- Counting sort executed in %f ms" % (time_4))
        print("- Cuonting sort memory consumption is %s bytes" % (str(mem4[1])))

        print("---")
        print("Dataset with %d numbers sorted:" %(num))

        tracemalloc.start()
        sorted_dataset_sorted, time_2 = BCIS(dataset_sorted)
        mem2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("- BCIS executed in %f ms" % (time_2))
        print("- BCIS memory consumption is %s bytes" % (str(mem2[1])))

        tracemalloc.start()
        counting_sorted_dataset_sorted, time_5 = counting_sort(dataset_sorted)
        mem5 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("- Counting sort executed in %f ms" % (time_5))
        print("- Counting sort memory consumption is %s bytes" % (str(mem5[1])))

        print("---")
        print("Dataset with %d numbers reversed:" %(num))

        tracemalloc.start()
        sorted_dataset_reversed, time_3 = BCIS(dataset_reversed)
        mem3 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("- BCIS executed in %f ms" % (time_3))
        print("- BCIS memory consumption is %s bytes" % (str(mem3[1])))

        tracemalloc.start()
        counting_sorted_dataset_reversed, time_6 = counting_sort(dataset_reversed)
        mem6 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("- Counting sort executed in %f ms" % (time_6))
        print("- Counting sort memory consumption is %s bytes" % (str(mem6[1])))
        
if __name__ == '__main__':
    run_experiment([500, 5000, 50000])   