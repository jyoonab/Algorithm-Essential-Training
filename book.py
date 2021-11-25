def solution(arr: list) -> int:
    N = len(arr)

    print('original :')
    print(arr)
    print("-----")

    dp = [1] * N

    for i in range(N):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    print('dp', dp)
    if dp.count(2) == 0:
        return len(dp)
    else:
        return findAllOne(dp)

def findAllOne(arr: list) -> int:
    ones = []
    result = []
    for i in range(len(arr)):
        if arr[i] == 1:
            ones.append(i)
    print('ones', ones)

    for i in range(len(ones)-1):
        result.append(ones[i+1] - ones[i])

    print('result', result)

    return max(result)+1

if __name__ == '__main__':
    arr = [10, 8, 9, 15, 12, 6, 7]
    arr2 = [9, 7, 6, 2, 1] # [9, 7, 6, 2, 1]
    arr3 = [5, 1, 2, 1, 4, 5] # [1, 2, 1], [1, 4, 5]
    arr4 = [7, 3, 4, 4, 8, 2, 5, 1] # [3, 4, 4, 8, 2]
    arr5 = [1, 2, 3, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
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
