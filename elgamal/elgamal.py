# 定义Elgamal加密函数
def elgamal_encrypt(p, g, y, plaintext, r):
    # 计算c1：g的r次方对p取模
    c1 = pow(g, r, p)
    # 计算c2：明文乘以y的r次方对p取模
    c2 = (plaintext * pow(y, r, p)) % p
    return c1, c2

# 定义Elgamal解密函数
def elgamal_decrypt(p, x, ciphertext):
    m = []
    for c1, c2 in ciphertext:
        # 计算明文：c2乘以c1的-a次方对p取模
        m_i = (c2 * pow(c1, -x, p)) % p
        m.append(m_i)
    return m


# 给定的参数
p = 691  # 大素数p
g = 29   # 生成元g
x = 259  # 私钥x

# 在通过私钥和给定的两个公钥中的参数推出这个公私钥对的最后一个公钥参数y
y = pow(g,x,p)


# 用于测试解密的例子
ciphertext = [(46, 236), (567, 244), (123, 390), (619, 11), (608, 237), (464, 19), (393, 682), (112, 512), (601, 237), (536, 146)]  # 密文

# 解密密文
plaintext = elgamal_decrypt(p, x, ciphertext)
ascii_list = [chr(num) for num in plaintext]
print("解密后的明文：", ascii_list)



# 加密学号
student_id = "32206400052"  # 在这里替换成你的学号
plaintext_ascii = [ord(char) for char in student_id]  # 将学号转换为ASCII码

# 选择随机数ri进行加密
import random
random.seed(123)
# 每个字符对应有一个随机数，这个随机数处于1<ri<p-1
r_values = [random.randint(1, p-1) for _ in plaintext_ascii]

# 加密学号
encrypted_student_id = [elgamal_encrypt(p, g, y, char, r) for char, r in zip(plaintext_ascii, r_values)]
print("加密后的学号：", encrypted_student_id)

# 还原学号的加密
plaintext = elgamal_decrypt(p, x, encrypted_student_id)
ascii_list = [chr(num) for num in plaintext]
print("还原学号的加密：", ascii_list)