import math

def Fermat(num):
    # 初始化x为num的平方根
    x = int(math.sqrt(num))
    # 如果x的平方小于num，则x加1
    if x * x < num:
        x += 1

    # y^2 = x^2 - num
    while (True):
        # 计算y^2
        y2 = x * x - num
        # 计算y
        y = int(math.sqrt(y2))
        # 如果y的平方等于y2，说明找到了解
        if y * y == y2:
            break
        # 否则，增加x的值，直到找到解
        x += 1

    # 返回两个因子
    return [x + y, x - y]

# 测试费马因子分解函数
print(Fermat(476714679652321667))
