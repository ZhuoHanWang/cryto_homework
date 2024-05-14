def linear_shift_register(seed, rounds):
    state = list(seed)  # 初始化寄存器状态
    output_sequence = []  # 存储输出序列
    state_sequence = []  # 存储状态序列
    period = None  # 周期长度

    for _ in range(rounds):
        # 计算输出
        output = int(state[3]) ^ int(state[0])
        output_sequence.append(output)

        # 计算新的状态
        new_state = [str(output)] + state[:-1]

        # 更新状态序列
        state_sequence.append(new_state)

        # 更新状态
        state = new_state

        # 如果周期还未找到且状态序列中有重复的状态
        if period is None and len(set(map(tuple, state_sequence))) != len(state_sequence):
            period = len(state_sequence) - 1  # 周期长度为上一次状态重复的位置

    return output_sequence, state_sequence, period

# 初始化序列
seed_sequence = ['1', '0', '0', '1']

# 执行20轮输出
output_seq, state_seq, period_length = linear_shift_register(seed_sequence, 20)

# 打印结果
print("Output sequence:")
print(output_seq)
print("\nState sequence:")
for state in state_seq:
    print(''.join(state))
print("\nPeriod length:", period_length)
