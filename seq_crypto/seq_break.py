import numpy as np

def gaussian_elimination(A, b):
    # 将系数矩阵和结果向量转换为 numpy 数组
    A = np.array(A)
    b = np.array(b)

    # 矩阵的行数和列数
    rows, cols = A.shape

    # 检查矩阵是否为方阵
    if rows != cols:
        raise ValueError("Coefficient matrix is not square")

    # 增广矩阵
    augmented_matrix = np.column_stack((A, b))

    # Gaussian消元法
    for i in range(rows):
        # 找到当前列的主元素所在的行
        max_row = max(range(i, rows), key=lambda x: abs(augmented_matrix[x][i]))

        # 交换行
        augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]

        # 将当前列下方的元素置零
        for j in range(i + 1, rows):
            if augmented_matrix[j][i] == 1:
                augmented_matrix[j] ^= augmented_matrix[i]

    # 回代，得到解向量
    x = np.zeros(rows, dtype=int)
    for i in range(rows - 1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i + 1, rows):
            x[i] ^= augmented_matrix[i][j] * x[j]

    return x

# 定义输入矩阵（模2）
input_matrix = [[1, 1, 1],
                [1, 1, 0],
                [1, 0, 1]]

# 定义输出矩阵（模2）
output_matrix = [0, 1, 0]

# 解方程组，求解系数
coefficients = gaussian_elimination(input_matrix, output_matrix)

# 输出结果
print("系数:", coefficients)


