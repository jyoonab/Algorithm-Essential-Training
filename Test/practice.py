def solution(priorities, location):
    answer = 0
    print(priorities, location)
    print(list(set(priorities)), location)
    print(list(dict.fromkeys(priorities)), location)


    return answer


input1 = [3,4,2,1,1,2,3,4]
input2 = [5,6,7,8]

solution(input1, input2)




# Remove All Duplicates from the List
# https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists
'''
list(dict.fromkeys(priorities) # [4, 3, 2, 1] [5, 6, 7, 8] # keeps order as it was
list(set(priorities)) # [1, 2, 3, 4] [5, 6, 7, 8] # gives arbitrary order(it seems it gives sorted order)
'''

# ZIP
'''
list1 = ['a','b','c']
list2 = [1, 2, 3]

zip(list1, list2) # return iterable object

zip_list = list(zip(list1, list2)) # use list type
zip_dict = dict(zip(list1, list2)) # use dict type

# 리스트형(tuple) iterate 하는법
print(zip_list[0])
print(zip_list[0][0])
print(zip_list[0][1])

# Dict형 iterate 하는법
print(zip_dict)
print(zip_dict['a'])
print(zip_dict['b'])

for i in zip_dict:
    print(zip_dict[i])
'''

# String 시작, 끝, 검색(Boolean)
'''
test_string = 'M-string-1002-A'

test_string.startwith('M-') # True
test_string.endwith('-C') # False

test_string.startwith('1002', 9, 13) # True
test_string.startwith('1000', 9, 13) # False
'''

# List Merge
'''
input1 = [1,2,3,4,1,2,3,4]
input2 = [5,6,7,8]

print(input1 + input2) # [1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 7, 8]
input1.append(input2)
print(input1) # [1, 2, 3, 4, 1, 2, 3, 4, [5, 6, 7, 8]]
input1.extend(input2)
print(input1) # [1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 7, 8]
'''
