# 实现列表对应元素相加（加密部分）
def add_list(x,y):
    result = []
    for i in range(len(x)):
        z = (x[i] + y[i]) % 26
        result.append(z)
    return result


# 实现列表元素对应相减（解密部分）
def sub_list(x,y):
    result = []
    for i in range(len(x)):
        z = (x[i] - y[i]) % 26
        result.append(z)
    return result

# 构造映射 字符---->num
def c2n():
    list_c = []
    list_n = []
    for i in range(26):
        list_n.append(i)
        # +97为对应的ascii
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
    # 构建映射关系
    dic_c2n = c2n()
    dic_n2c = n2c()
    # 原文，密钥，密文
    list_s = []
    list_key = []
    list_finall = []
    # 原文映射到数字
    for i in s:
        i = i.lower()
        list_s.append(dic_c2n[i])
    # 先不管密钥长度，先把密钥也映射成数字
    for i in key:
        i = i.lower()
        list_key.append(dic_c2n[i])

    # 扩充密钥长度直到和原文相等（这个时候已经是数字）
    for i in list_key:
        if len(list_key) <= len(list_s):
            list_key.append(i)

    # 相加取模
    list_result = add_list(list_s,list_key)
    # 取模运算
    for i in list_result:
        # if i > 25:
        #     i -= 26

        # 完成映射
        list_finall.append(dic_n2c[i])
    for i in list_finall:
        print(i.upper(),end='')

# 解密
def decode(s,key):
    print('解密后的字符： ',end='')
    dic_c2n = c2n()
    dic_n2c = n2c()
    # 密文，密钥，原文
    list_s = []
    list_key = []
    list_finall = []
    # 密文映射
    for i in s:
        i = i.lower()
        list_s.append(dic_c2n[i])
    # 密钥映射
    for i in key:
        i = i.lower()
        list_key.append(dic_c2n[i])
    # 密钥扩充
    for i in list_key:
        if len(list_key) < len(list_s):
            list_key.append(i)

    # 相减取模
    list_result = sub_list(list_s,list_key)
    # 取模运算
    for i in list_result:
        # if i < 0:
        #     i += 26

        # 完成映射
        list_finall.append(dic_n2c[i])
    for i in list_finall:
        print(i,end='')

# 函数入口
answer = input(f'请输入所需的操作：编码e/E or 解码d/D,键入0退出程序:  ')
while True:
    try:
        if answer.upper() == 'E':
            key = input('请输入Key:')
            s = input('请输入需要加密的字符：')
            encode(s,key)
            print("\n")
        elif answer.upper() == 'D':
            key = input('请输入Key:')
            s = input('请输入需要解密的字符：')
            decode(s,key)
            print("\n")
        elif answer == "0":
            quit(0)
        else:
            print('输入错误！')
            print("\n")
    except KeyError:
        print('请勿输入空格！')
        print("\n")