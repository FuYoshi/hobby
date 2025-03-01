#!/usr/bin/python
"""
Filename: sort.py
Authors: Yoshi Fu
Project: Sorting Algorithms
Date: February 2025

Summary:
TODO
"""


import random


def generate_random_array(size: int) -> list[int]:
    """Generate a random array.

    Returns:
        list[int]: random array.
    """
    return [random.randint(1, 100) for _ in range(size)]


def bubble_sort(arr: list[int]) -> list[int]:
    """Sort an array using bubble sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    n: int = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(arr: list[int]) -> list[int]:
    """Sort an array using insertion sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    n: int = len(arr)
    for i in range(1, n):
        key: int = arr[i]
        j: int = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def selection_sort(arr: list[int]) -> list[int]:
    """Sort an array using selection sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    n: int = len(arr)
    for i in range(n):
        min_idx: int = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def quick_sort(arr: list[int]) -> list[int]:
    """Sort an array using quick sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    if len(arr) <= 1:
        return arr
    pivot: int = arr[len(arr) // 2]
    left: list[int] = [x for x in arr if x < pivot]
    middle: list[int] = [x for x in arr if x == pivot]
    right: list[int] = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(arr: list[int]) -> list[int]:
    """Sort an array using merge sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    if len(arr) <= 1:
        return arr
    mid: int = len(arr) // 2
    left: list[int] = arr[:mid]
    right: list[int] = arr[mid:]
    left = merge_sort(left)
    right = merge_sort(right)
    return list(left + right)


def count_sort(arr: list[int]) -> list[int]:
    """Sort an array using counting sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    max_val: int = max(arr)
    count: list[int] = [0] * (max_val + 1)
    output: list[int] = [0] * len(arr)

    for num in arr:
        count[num] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1

    for i, _ in enumerate(arr):
        arr[i] = output[i]
    return arr


def radix_sort(arr: list[int]) -> list[int]:
    """Sort an array using radix sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    max1: int = max(arr)
    exp: int = 1
    while max1 // exp > 0:
        count_sort(arr)
        exp *= 10
    return arr


def bucket_sort(arr: list[int]) -> list[int]:
    """Sort an array using bucket sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    max_val: int = max(arr)
    size: int = len(arr)

    buckets: list[list] = [[] for _ in range(size)]
    for i in range(size):
        index = int(arr[i] * size / (max_val + 1))
        buckets[index].append(arr[i])

    for i in range(size):
        buckets[i].sort()

    result: list = []
    for i in range(size):
        result.extend(buckets[i])
    return result


def heap_sort(arr: list[int]) -> list[int]:
    """Sort an array using heap sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """

    def heapify(arr: list[int], n: int, i: int) -> None:
        largest: int = i
        l: int = 2 * i + 1
        r: int = 2 * i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n: int = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


def shell_sort(arr: list[int]) -> list[int]:
    """Sort an array using shell sort.

    Args:
        arr (list[int]): array to sort.

    Returns:
        list[int]: sorted array.
    """
    n: int = len(arr)
    gap: int = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp: int = arr[i]
            j: int = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def main() -> None:
    """Main function."""
    arr: list[int] = generate_random_array(10)
    print(f"Original array: {arr}")
    print(f"Bubble sort:    {bubble_sort(arr)}")
    print(f"Bucket sort:    {bucket_sort(arr)}")
    print(f"Count sort:     {count_sort(arr)}")
    print(f"Heap sort:      {heap_sort(arr)}")
    print(f"Insertion sort: {insertion_sort(arr)}")
    print(f"Merge sort:     {merge_sort(arr)}")
    print(f"Radix sort:     {radix_sort(arr)}")
    print(f"Selection sort: {selection_sort(arr)}")
    print(f"Shell sort:     {shell_sort(arr)}")
    print(f"Quick sort:     {quick_sort(arr)}")


if __name__ == "__main__":
    main()
