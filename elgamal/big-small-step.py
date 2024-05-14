def discrete_logarithm(p, g, y):
    m = int(p ** 0.5) + 1

    # 计算小步
    small_steps = {}
    for j in range(m):
        small_steps[pow(g, j, p)] = j

    # 计算大步
    g_inv_m = pow(g, -m, p)
    giant_step = y
    for i in range(m):
        if giant_step in small_steps:
            return i * m + small_steps[giant_step]
        giant_step = (giant_step * g_inv_m) % p

    return None

# 给定的参数
p = 65867
g = 15012
y = 48541

# 使用大步小步算法求解私钥x
private_key = discrete_logarithm(p, g, y)
print("私钥 x 为:", private_key)
