import random

# 椭圆曲线参数
P = 503  # 模数
a = 4    # 椭圆曲线可控的参数
b = 1
Gx = 283  # 素阶点横纵坐标值
Gy = 315
n = 7     # 生成公钥的私钥

# 点加运算
def point_add(x1, y1, x2, y2, a, P):
    # print(f"点加运算输入: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
    if x1 is None or x2 is None:
        return [None, None]  # 如果任一点是无穷远点
    if x1 == x2 and y1 == y2:
        if y1 == 0:
            return [None, None]  # 无穷远点
        # 相同点加倍
        slope = (3 * x1 ** 2 + a) * pow(2 * y1, P - 2, P) % P
    else:
        if x1 == x2:
            return [None, None]  # 垂直线，结果为无穷远点
        # 不同点相加
        slope = ((y2 - y1) * pow(x2 - x1, P - 2, P)) % P
    x3 = (slope ** 2 - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    # print(f"点加运算结果: x3={x3}, y3={y3}")
    return [x3, y3]


# 解密函数
def decrypt(c2, c1, n, a, P):
    """
    解密函数，通过计算 n*c1 的负点，然后与密文点 c2 相加得到明文点。

    参数:
    c2: 密文点之一
    c1: 密文点之一
    n: 私钥
    a: 椭圆曲线参数
    P: 模数

    返回:
    解密后的点坐标
    """
    temp = [c1[0], c1[1]]
    for _ in range(n - 1):
        temp = point_add(temp[0], temp[1], c1[0], c1[1], a, P)
        if temp[0] is None or temp[1] is None:
            raise ValueError("解密过程中遇到了无穷远点")
    temp[1] = -temp[1] % P
    result = point_add(c2[0], c2[1], temp[0], temp[1], a, P)
    return result


def get_ng(G_x, G_y, k, a, p):
    """
    计算 kG，其中 G 是椭圆曲线上的基点，k 是一个整数。

    参数:
    G_x, G_y: 基点 G 的坐标
    k: 积数
    a: 椭圆曲线参数
    p: 模数

    返回:
    kG 的坐标 (x, y)
    """
    result_x, result_y = G_x, G_y
    # Omar Reyad提出的方法中，通过重复点加操作来计算 kG。
    for _ in range(k - 1):
        result_x, result_y = point_add(result_x, result_y, G_x, G_y, a, p)
    return result_x, result_y


def map_plain_text_to_curve(plain_text):
    """
    将明文字符映射到椭圆曲线点。

    参数:
    plain_text: 要映射的明文字符串

    返回:
    椭圆曲线点列表，每个点对应一个明文字符
    """
    mapping_point = []
    print("明文映射的点为：", end="")
    for char in plain_text:
        intchar = ord(char)  # 将字符转换为 ASCII 数值
        mapping_k = intchar + 1  # 映射表中的索引
        # 根据Omar Reyad的方法，通过映射表将ASCII字符码转换为椭圆曲线上的点。
        G_x, G_y = Gx, Gy
        k_G_x, k_G_y = get_ng(G_x, G_y, mapping_k, a, P)  # 计算 kG
        mapping_point.append([k_G_x, k_G_y])
        print(f"{char}=>({k_G_x},{k_G_y})", end="---")
    print("")
    return mapping_point


def decode_curve_points_to_text(mapping_points):
    """
    将椭圆曲线点解码回明文字符。

    参数:
    mapping_points: 椭圆曲线点列表，每个点对应一个字符

    返回:
    解码后的明文字符串
    """
    decoded_text = ""
    for x, y in mapping_points:
        for char in range(128):  # 遍历所有可能的 ASCII 字符
            G_x, G_y = Gx, Gy
            # 使用Omar Reyad的方法，通过查找映射表还原每个字符对应的椭圆曲线点。
            k_G_x, k_G_y = get_ng(G_x, G_y, char + 1, a, P)
            if k_G_x == x and k_G_y == y:  # 找到匹配的点
                decoded_text += chr(char)
                break
    return decoded_text


def perform_encryption_and_decryption(a, b, P, Gx, Gy, n, Mx, My):
    """
    执行加密和解密过程，包括随机生成数 r、计算点 G 和 c1、生成 nG 和密文点 c2。

    参数:
    a, b: 椭圆曲线参数
    P: 模数
    Gx, Gy: 基点 G 的坐标
    n: 私钥
    Mx, My: 明文点的坐标
    """
    while True:
        try:
            # 随机数
            r = random.randint(1, P - 1)
            print(f"随机数 r: {r}")
            # 通过给定的私钥n得到的G G = nP 和 通过随机数r得到的c1 rP (即 c1)
            G = [Gx, Gy]
            c1 = [Gx, Gy]
            for _ in range(n - 1):
                G = point_add(G[0], G[1], Gx, Gy, a, P)
            for _ in range(r - 1):
                c1 = point_add(c1[0], c1[1], Gx, Gy, a, P)

            print(f"给定的 G: {G}")
            print(f"通过随机数 c1: {c1}")

            # 计算 nG
            nG = G[:]
            for _ in range(r - 1):
                nG = point_add(nG[0], nG[1], G[0], G[1], a, P)

            print(f"生成的 nG: {nG}")

            # 计算 c2 = M + nG
            c2 = point_add(Mx, My, nG[0], nG[1], a, P)
            if c2[0] is None or c2[1] is None:
                raise ValueError("加密过程中遇到了无穷远点")

            # 解密
            decrypted_m = decrypt(c2, c1, n, a, P)
            print(f'加密坐标 (c2): {c2}')
            print(f'解密坐标: {decrypted_m}')
            break  # 成功执行，退出循环

        except ValueError as e:
            print(f"错误: {e}，重新尝试加密解密过程...")


if __name__ == '__main__':
    plain_text = "Hello"
    print(f"明文: {plain_text}")

    # 明文映射到椭圆曲线点
    mapped_points = map_plain_text_to_curve(plain_text)

    # 对每个映射点进行加密解密
    for point in mapped_points:
        Mx, My = point
        perform_encryption_and_decryption(a, b, P, Gx, Gy, n, Mx, My)

    # 解码回明文
    decoded_text = decode_curve_points_to_text(mapped_points)
    print(f"解码后的明文: {decoded_text}")


