'''维吉尼亚破解'''
import numpy as np
import math

# s为密文，cmp_string发现的重复字符串
def findSameWords_time_index(s, cmp_string):
    # 找出现次数最多的字符，返回他所有下标和字符本身

    # 初始化 保存不同长度的字符出现次数最多的,键：'字符'，值：[[出现的次数,出现下标间距的最大公约数], [每次出现的下标]]
    dic_wordCount = {cmp_string:[[0,0],[]]}

    # 使用find函数，可以返回第一次匹配的下标，注意，存放到dic数据结构中需要给下标+1
    index = s.find(cmp_string)

    # 找不到的时候循环结束
    while index != -1:
        # 统计次数加1
        dic_wordCount[cmp_string][0][0] += 1
        # 加入对应的字符串的位置
        dic_wordCount[cmp_string][1].append(index + 1)
        # 设置查找的起始位置为当前找到的之后，也就是index+1开始
        index = s.find(cmp_string, index + 1)  # 继续找

    # 键：'字符'，值：[距离的最大公约数, [每次出现的下标]]

    # 总共有多少个下标，出现不足两次一定报错
    temp_time = dic_wordCount[cmp_string][0][0]
    if temp_time < 2: quit(1)

    # 求间距的最大公约数，也就是求[cmp_string][1]，数组元素之间求最大公约数，这就需要两步，第一步先求数组相邻元素之间的差值，再对差值数组求gcd
    # 先初始化为第一个等待被求最大公约数的值，也就是第一段间距
    distance_gcd = dic_wordCount[cmp_string][1][1] - dic_wordCount[cmp_string][1][0]
    # 保证出现了两次以上才能求最大公约数，把原先存放出现次数变为距离的最大公约数
    # 求公约数的次数,从第二个开始到最后一个
    for i in range(1 , temp_time-1 , 1):
        # 重复求最大公因数
        distance_gcd = math.gcd(distance_gcd,dic_wordCount[cmp_string][1][i+1]-dic_wordCount[cmp_string][1][i])
        #print("距离的最大公因子为:", distance_gcd)

    # 得到距离的公因子
    dic_wordCount[cmp_string][0][1] = distance_gcd
    #print("距离的最大公因子为:",distance_gcd)

    return dic_wordCount


# 给定一个密文分组子串计算其重合指数
def count_IC(cipher_after_group):
    count = [0 for i in range(26)]
    L = len(cipher_after_group)
    IC = 0.0
    # 防止大小写导致错误,这个是通过count的下标代表字母，数组内容为出现次数，即，统计一个密文分组中的各字母出现顺序
    for i in range(len(cipher_after_group)):
        if (cipher_after_group[i].isupper()):
            count[ord(cipher_after_group[i]) - ord('A')] += 1
        elif (cipher_after_group[i].islower()):
            count[ord(cipher_after_group[i]) - ord('a')] += 1
    # 计算公式
    for i in range(26):
        IC += (count[i] * (count[i] - 1)) / (L * (L - 1))
    return IC

# 对整组密文进行分组,ken_len也就是猜测的密钥长度，进行，根据密钥位置的分组划分，便于统计
def group(cipher_all, key_len):
    N = ['' for i in range(key_len)]
    for i in range(len(cipher_all)):  # 对密文进行分组
        m = i % key_len
        N[m] += cipher_all[i]
    return N

# 调用分组方法和计算IC值的方法，
def count_key_len(cipher_all, key_len):
    # N也就是根据keylen进行分组的，根据密钥长度进行分组，便于统计
    N = group(cipher_all, key_len)
    IC = [0 for i in range(key_len)]
    # 计算分组的ic值
    for i in range(key_len):
        IC[i] = count_IC(N[i])
    # print(IC)
    print("平均重合指数为%.5f" % (np.mean(IC)))
    return np.mean(IC)#求平均

#计算拟重合指数
def tongjinichonghe(key,s):
    sniic=0
    p = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
         0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
         0.01974, 0.00074]
    tongjinichonghe = [0 for _ in range(0,26)]
    zff = ""
    #ic=-0
    #转换为只有大写字母的字符串
    for t in s:
        if 65 <= ord(t) <= 90:
            zff += t
    #统计每个字母出现的次数
    for cisu in zff:
        tongjinichonghe[ord(cisu) - 65] += 1
    #求出每个凯撒加密的解密，根据拟重合指数找到正确的密钥
    list0=tongjinichonghe
    list1=[0 for _ in range(0,26)]
    for i in range (26):
        list1[i]=list0[(i+key)%26]
    tongjinichonghe=list1
    for i in range (len(tongjinichonghe)):
        niic=tongjinichonghe[i]/len(tongjinichonghe)*p[i]
        sniic+=niic
    return sniic


def decode(s):
    nicos=[0 for _ in range(0,26)]

    for i in range(26):
        nicos[i]=tongjinichonghe(i,s)

    list1=sorted(nicos)
    num = nicos.index(list1[-1])
    ch = chr(num+65)
    #print(ch)
    return ch

# T1
s="CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBWRVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAKLXFPSKAUTEMNDCMGTSXMXBTUIADNGMGPSRELXNJELXVRVPRTULHDNQWTWDTYGBPHXTFALJHASVBFXNGLLCHRZBWELEKMSJIKNBHWRJGNMGJSGLXFEYPHAGNRBIEQJTAMRVLCRREMNDGLXRRIMGNSNRWCHRQHAEYEVTAQEBBIPEEWEVKAKOEWADREMXMTBHHCHRTKDNVRZCHRCLQOHPWQAIIWXNRMGWOIIFKEE"
s_len=len(s)
cmp_string="CHR"
# # 查看分组情况
# print(group(s,5))
# # 查看分组后的IC值
# print(count_key_len(s,5))
# # 卡希斯基法测试密钥长度
# print(findSameWords_time_index(s,cmp_string))



dic = findSameWords_time_index(s,cmp_string)
print("'重复字符':[[出现的次数,距离的最大公因子], [每次出现的下标+1]]")
print(dic)
# 根据指定的重复的关键字，卡希斯基法探测出可能的密钥长度（也就是出现距离的最大公因数），使用重合指数分析法校验
for key_len in range(1,dic[cmp_string][0][1]+1,1):
    print("组数为",key_len,"时")
    grouped_s = group(s, key_len)
    print(grouped_s)
    print(count_key_len(s, key_len))

for i in grouped_s:
    print(decode(i))