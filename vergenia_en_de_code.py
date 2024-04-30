# 实现列表对应元素相加（加密部分）
def add_list(x,y):
    result = []
    for i in range(len(x)):
        z = x[i] + y[i]
        result.append(z)
    return result


# 实现列表元素对应相减（解密部分）
def sub_list(x,y):
    result = []
    for i in range(len(x)):
        z = x[i] - y[i]
        result.append(z)
    return result

# 构造映射 字符---->num
def c2n():
    list_c = []
    list_n = []
    for i in range(26):
        list_n.append(i)
        list_c.append(chr(i+97))
    dic_c2n = dict(map(lambda x,y:[x,y],list_c,list_n))
    return dic_c2n


# 构造映射 num---->字符
def n2c():
    list_c = []
    list_n = []
    for i in range(26):
        list_n.append(i)
        list_c.append(chr(i+97))
    dic_n2c = dict(map(lambda x,y:[x,y],list_n,list_c))
    return dic_n2c

def encode(s,key):
    print('加密后的字符： ',end='')
    dic_c2n = c2n()
    dic_n2c = n2c()
    list_s = []
    list_key = []
    list_finall = []
    for i in s:
        i = i.lower()
        list_s.append(dic_c2n[i])
    for i in key:
        i = i.lower()
        list_key.append(dic_c2n[i])
    for i in list_key:
        if len(list_key) <= len(list_s):
            list_key.append(i)
    list_result = add_list(list_s,list_key)
    for i in list_result:
        if i > 25:
            i -= 26
        list_finall.append(dic_n2c[i])
    for i in list_finall:
        print(i.upper(),end='')

# 解密
def decode(s,key):
    print('解密后的字符： ',end='')
    dic_c2n = c2n()
    dic_n2c = n2c()
    list_s = []
    list_key = []
    list_finall = []
    for i in s:
        i = i.lower()
        list_s.append(dic_c2n[i])
    for i in key:
        i = i.lower()
        list_key.append(dic_c2n[i])
    for i in list_key:
        if len(list_key) < len(list_s):
            list_key.append(i)
    list_result = sub_list(list_s,list_key)
    for i in list_result:
        if i < 0:
            i += 26
        list_finall.append(dic_n2c[i])
    for i in list_finall:
        print(i,end='')

# 函数入口
answer = input(f'请输入所需的操作：编码/E or 解码/D:  ')
try:
    if answer.upper() == 'E':
        key = input('请输入Key:')
        s = input('请输入需要加密的字符：')
        encode(s,key)
    elif answer.upper() == 'D':
        key = input('请输入Key:')
        s = input('请输入需要解密的字符：')
        decode(s,key)
    else:
        print('输入错误！')
except KeyError:
    print('请勿输入空格！')