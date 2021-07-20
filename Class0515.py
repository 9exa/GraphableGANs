# -*- coding = utf-8 -*-
# @Time : 2021/5/15 15:51
# @Author : ..
# @File : Class0515.py
# @Software : PyCharm

'''
# class 1 输出
# 格式化输出
age = 18
print("age:%d "%age) #%d表示数据化类型(data)，%s(string)

print("name:%s,nationality:%s"%("tt","China"))

print("a","b",sep=".") #sep表示选择分隔符

print("a1",end="") #用end来选择结束方式，直接连接
print("a2",end="\t") #tab
print("a3",end="\n") #换行
print("a4")

password = input("input password please") #输入变量赋值
print("your password:",password)

a = input("input:")
print(type(a)) #输出a的字符型

a1 = int(a) #transform from string to int
print("put a number:%d" %a1) #ashould use %s since a is a string
'''

# class 2 循环
'''
if 1:               # True or non zero
    print("True1")
    print("True2")  # 相同层次语句要同样缩进格式
else:
    print("False")
print("end")        # 通过缩进表达程序范围

score = input("put your score:")
score1 = int(score)
if score1 >= 90 and score1 <= 100:
    print("your grade is A")
elif score1 >= 80 and score1 < 90:
    print("your grade is B")
else:                               # 可以继续嵌套
    if score1 >= 70 and score1 < 80:
        print("your grade is C")
# elif score >= 0 and score < 60:   (use elif to end
# elif and else can be used together

male = 1
single = 0

if male == 1:
    print("male")
    if single == 1:
        print("single")
    else:
        print("not single")
else:
    print("female")


# 剪刀石头布
import random # 引入随机库
a = input("input 0 or 1 or 2")
a1 = int(a)             # 0 rock, 1 scissor, 2 paper
x = random.randint(0,2)
if a1 == 0 or a1 == 1 or a1 == 2:   # 石头剪刀布布是个循环比较，这里枚举解决
    if a1 == 0:
        if x == 1:
            print("win")
        if x == 2:
            print("lose")
        elif x == 0:
            print("same")
    if a1 == 1 :
        if x == 2:
            print("win")
        if x == 0:
            print("lose")
        elif x == 1:
            print("same")
    if a1 == 2:
        if x == 0:
            print("win")
        if x == 1:
            print("lose")
        elif x == 2:
            print("same")
else:
    print("meaningless input")

print(x)

# x = random.random()   (randint(0,2),includes 0 1 2
# 目前好像没有其他省略的方法了，看能否先判断收到两个input，再判断各自多少
'''

# for and while循环

'''
for i in range(5):
    print(i)        # from 0 to 4
    
for i in range(0,12,3):
    print(i)        # from 0 to 11 取左0不取右12

name = "abcde"
for x in name:
    print(x,end="\t")

a = ["aa","bb","cc","dd"]
for i in range(len(a)):     # a has 4 items,遍历a
    print(i,a[i])

i = 0
while i < 5:
    print("%d th"%(i+1))
    print("i=%d"%i)
    i += 1          # increase


# sum 1 to 100

i = 0
sum = 0
while i <= 100:
    sum = sum + i
    i += 1
print(sum)

sum = 0
for x in range(1,101,1):
    sum += x
print("sum 1 to %d equals to %d"%(x,sum))

count = 0
while count < 5:
    print(count,"<5")
    count += 1
else:
    print(count,">=5")  # while can be combined with else

# break, continue, pass
i = 0
while i < 10:
    i += 1
    print("-"*10)   # print 10 -
    if i == 5:
        break       # 结束整个循环
    print(i)

i = 0
while i < 10:
    i += 1
    print("-"*10)   # print 10 -
    if i == 5:
        continue    # 结束本次循环（i = 5 has not been printed）
    print(i)

for i in range(1,10):
    for x in range(1,i+1):
        print("%d * %d = %d" % (x, i, x * i), end="\t")
    print()
            # () and ("\n")


# string
paragraph = """     
    apple.
pire.
 google.

"""
print(paragraph)    # """ save all formats

my_str = 'I\'m a student'   # use \ interpret ' or "
print(my_str)

str = "abcdefg"
print(str[0:5:2])     # cut part of the string with step 2 each

print("hello\nworld")   # 转译，\n换行
print(r"hello\nworld")  # r使得\的转移效果消失


# 列表
testlist = [1,"A"]

print(type(testlist[0]))
print(type(testlist[1]))    # 列表可以储存混合类型

# 遍历列表
namelist = ["A","B","C"]
for name in namelist:
    print(name)

length = len(namelist)
i = 0
while i < length:
    print(namelist[i])
    i += 1

# 增删改查
# 增加： [append] & [extend] & [insert]
namelist = ["A","B","C"]
for name in namelist:
    print(name)

nametemp = input("Input your name:")    
namelist.append(nametemp)           # add at the end
for name in namelist:
    print(name)

# append and extend
a = [1,2]
b = [3,4]
a.append(b)     #列表的嵌套：将列表当作一个元素，加入a列表
print(a)

a.extend(b)     #将列表中元素逐一加入a列表
print(a)

# 指定位置增加： [insert]

a = [0,1,2]
a.insert(1,3)   #第一个变量表示下标，第二个表示对象：把3插入1的位置
print(a)        #[0, 3, 1, 2]

# 删 [del] & [pop] & [remove]

a = [0,1,2,3,4]
del a[2]    # 在指定位置删除

a.pop()     # 弹出末尾最后一个元素

b = ["a","b","c","d","e","b"]
b.remove("b")
print(b)    # ['a', 'c', 'd', 'e']  # 直接删除指定内容（找到的第一个）

# 改 [ = ]
b = ["a","b","c","d","e","b"]
b[1] = "小红"                 # 修改指定位置的元素
print(b)                     # ['a', '小红', 'c', 'd', 'e', 'b']

# 查 [in]

b = ["a","b","c","d","e","b"]
findName = input("Required name:")

if findName in b:
    print("Got it")
else:
    print("Invalid")

b = ["a","b","c","d","e","b"]
print(b.index("a",0,4))        # find "a" in from 1 to 4 in b, find exact location
# 如果找不到会直接报错，范围区间左取右弃

b = ["a","b","c","d","e","b"]   # count how many elements
print(b.count("b"))

# order
a = [1,4,2,7,5,6,9]
a.reverse()
print(a)        # cannot print a.reverse directly
a.sort()
print(a)        # 升序
a.sort(reverse=True)    # 降序
print(a)

# schoolName = [[],[],[]]     # 有三个元素的空列表 + 每个元素都是一个空列表
schoolName = [["PKU","TSU"],["HKU","UTS","SYP"],["UNSW","MOU","UYS"]]
# 每个元素中的内容数量可以不同
print(schoolName[0][0]) # 第一个变量指明第几个空列表，第二个变量指明空列表中的位置

# 随机给每个人分配办公室
import random

offices = [[], [], []]

names = ["A", "B", "C", "D", "E", "F", "G"]

for name in names:
    index = random.randint(0, 2)     # 3 office randomly pick one
    offices[index].append(name)     # put the names in this picked office

i = 1
for office in offices:
    print("number of members in %d th office: %d" % (i, len(office)),end="\t")
    i += 1
    for name in office:
        print("%s" % name, end="\t")
    print()

# 输入指定商品列表
products = [["iphone", 6888], ["MacPro", 14800], ["小米6", 2499], ["Coffee", 31], ["Book", 60], ["Nike",699]]

validCode = ["0","1","2","3","4","5","q"]
goodlist = []


while 1:        # 建立一个无限循环
    inputtemp = input("Input the code of your good:")
    if inputtemp in validCode:
        if inputtemp != "q":
            goodCode = int(inputtemp)
            goodlist.append(products[goodCode])
        elif inputtemp == "q":
            break
    else:
        print("Invalid")

print("The good you choose:",goodlist)

sum = 0
for i in range (0,len(goodlist)):
    a = int(goodlist[i][1])
    sum += a
print("The price of all goods you pick is: %d"%sum)
'''


