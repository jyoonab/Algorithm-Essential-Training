def solution(arr: list) -> int:
    first_up_slope = -1
    slope_list = [0]
    peak_list = []
    result_list = []

    print(arr)

    # save slope as list
    for i in range(len(arr)-1):
        slope = arr[i+1] - arr[i]

        if slope == 0 and i != 0:
            slope_list += slope_list[-1:]
        elif slope == 0:
            slope_list.append(0)
        elif slope > 0:
            slope_list.append(1)
        elif slope < 0:
            slope_list.append(-1)

    print(slope_list)

    for i in range(len(slope_list)-1):
        if slope_list[i] < slope_list[i+1]:
            peak_list.append(i)
        elif slope_list[i] > slope_list[i+1]:
            peak_list.append(i)

    if slope_list[1] == -1:
        peak_list = peak_list[1:]

    if slope_list[len(slope_list)-1] == -1:
        peak_list.append(len(slope_list)-1)

    print(peak_list)

    counter = 0
    while counter < len(peak_list)-1:
        result_list.append(peak_list[counter+2]-peak_list[counter])
        counter += 2

    if len(result_list) == 0:
        return len(arr)

    if len(result_list) == 1:
        if len(slope_list)-1 == result_list[0]:
            return len(arr)
        else:
            return len(slope_list) - result_list[0]

    return max(result_list)+1

if __name__ == '__main__':
    arr = [10, 8, 9, 15, 12, 6, 7]
    arr2 = [9, 7, 6, 2, 1] # [9, 7, 6, 2, 1]
    arr3 = [5, 1, 2, 1, 4, 5] # [1, 2, 1], [1, 4, 5]
    arr4 = [7, 3, 4, 4, 8, 2, 5, 1] # [3, 4, 4, 8, 2]
    arr5 = [1, 1, 2, 3, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    arr6 = [6, 4, 1, 2, 3, 6, 9]

    print('my answer: ', solution(arr))
    print()
    print('my answer: ', solution(arr2))
    print()
    print('my answer: ', solution(arr3))
    print()
    print('my answer: ', solution(arr4))
    print()
    print('my answer: ', solution(arr5))
    print()
    print('my answer: ', solution(arr6))
