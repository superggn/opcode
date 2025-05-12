ADD = 0x01
MUL = 0x02
SUB = 0x03
DIV = 0x04
SDIV = 0x05
MOD = 0x06
SMOD = 0x07
ADDMOD = 0x08
MULMOD = 0x09
EXP = 0x0A
SIGNEXTEND = 0x0B
LT = 0x10
GT = 0x11
SLT = 0x12
SGT = 0x13
EQ = 0x14
ISZERO = 0x15
AND = 0x16
OR = 0x17
XOR = 0x18
NOT = 0x19
BYTE = 0x1A
SHL = 0x1B
SHR = 0x1C
SAR = 0x1D
PUSH0 = 0x5F
PUSH1 = 0x60
PUSH32 = 0x7F
POP = 0x50
MLOAD = 0x51
MSTORE = 0x52
MSTORE8 = 0x53
MSIZE = 0x59


class EVM:
    def __init__(self, code):
        self.code = code  # 初始化字节码，bytes对象
        self.pc = 0  # 初始化程序计数器为0
        self.stack = []  # 堆栈初始为空
        self.memory = bytearray()  # 内存初始化为空

    def next_instruction(self):
        op = self.code[self.pc]  # 获取当前指令
        self.pc += 1  # 递增
        return op

    def push(self, size):
        data = self.code[self.pc:self.pc + size]  # 按照size从code中获取数据
        value = int.from_bytes(data, 'big')  # 将bytes转换为int
        self.stack.append(value)  # 压入堆栈
        self.pc += size  # pc增加size单位

    def pop(self):
        if len(self.stack) == 0:
            raise Exception('Stack underflow')
        return self.stack.pop()  # 弹出堆栈

    def add(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        res = (a + b) % (2 ** 256)  # 加法结果需要模2^256，防止溢出
        self.stack.append(res)

    def mul(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        res = (a * b) % (2 ** 256)  # 乘法结果需要模2^256，防止溢出
        self.stack.append(res)

    def sub(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        res = (a - b) % (2 ** 256)  # 结果需要模2^256，防止溢出
        self.stack.append(res)

    def div(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        if a == 0:
            res = 0
        else:
            res = (a // b) % (2 ** 256)
        self.stack.append(res)

    def sdiv(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        res = a // b % (2 ** 256) if a != 0 else 0
        self.stack.append(res)

    def mod(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        res = a % b if a != 0 else 0
        self.stack.append(res)

    def smod(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        res = a % b if a != 0 else 0
        self.stack.append(res)

    def addmod(self):
        if len(self.stack) < 3:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        n = self.stack.pop()
        res = (a + b) % n if n != 0 else 0
        self.stack.append(res)

    def mulmod(self):
        if len(self.stack) < 3:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        n = self.stack.pop()
        res = (a * b) % n if n != 0 else 0
        self.stack.append(res)

    def exp(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        res = pow(a, b) % (2 ** 256)
        self.stack.append(res)

    def signextend(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        b = self.stack.pop()
        x = self.stack.pop()
        if b < 32:  # 如果b>=32，则不需要扩展
            sign_bit = 1 << (8 * b - 1)  # b 字节的最高位（符号位）对应的掩码值，将用来检测 x 的符号位是否为1
            x = x & ((1 << (8 * b)) - 1)  # 对 x 进行掩码操作，保留 x 的前 b+1 字节的值，其余字节全部置0
            if x & sign_bit:  # 检查 x 的符号位是否为1
                x = x | ~((1 << (8 * b)) - 1)  # 将 x 的剩余部分全部置1
        self.stack.append(x)

    def lt(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(int(b < a))  # 注意这里的比较顺序

    def gt(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(int(b > a))  # 注意这里的比较顺序

    def slt(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(int(b < a))  # 极简evm stack中的值已经是以有符号整数存储了，所以和lt一样实现

    def sgt(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(int(b > a))  # 极简evm stack中的值已经是以有符号整数存储了，所以和gt一样实现

    def eq(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(int(a == b))

    def iszero(self):
        if len(self.stack) < 1:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        self.stack.append(int(a == 0))

    def and_op(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a & b)

    def or_op(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a | b)

    def xor_op(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a ^ b)

    def not_op(self):
        if len(self.stack) < 1:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        self.stack.append(~a % (2 ** 256))  # 按位非操作的结果需要模2^256，防止溢出

    def byte_op(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        position = self.stack.pop()
        value = self.stack.pop()
        if position >= 32:
            res = 0
        else:
            res = (value // pow(256, 31 - position)) & 0xFF
        self.stack.append(res)

    def shl(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append((b << a) % (2 ** 256))  # 左移位操作的结果需要模2^256

    def shr(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b >> a)  # 右移位操作

    def sar(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b >> a)  # 右移位操作

    def mstore(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        offset = self.stack.pop()
        value = self.stack.pop()
        while len(self.memory) < offset + 32:
            self.memory.append(0)  # 内存扩展
        self.memory[offset:offset + 32] = value.to_bytes(32, 'big')

    def mstore8(self):
        if len(self.stack) < 2:
            raise Exception('Stack underflow')
        offset = self.stack.pop()
        value = self.stack.pop()
        while len(self.memory) < offset + 32:
            self.memory.append(0)  # 内存扩展
        self.memory[offset] = value & 0xFF  # 取最低有效字节

    def mload(self):
        if len(self.stack) < 1:
            raise Exception('Stack underflow')
        offset = self.stack.pop()
        while len(self.memory) < offset + 32:
            self.memory.append(0)  # 内存扩展
        value = int.from_bytes(self.memory[offset:offset + 32], 'big')
        self.stack.append(value)

    def msize(self):
        self.stack.append(len(self.memory))

    def run(self):
        while self.pc < len(self.code):
            op = self.next_instruction()

            if PUSH1 <= op <= PUSH32:  # 如果为PUSH1-PUSH32
                size = op - PUSH1 + 1
                self.push(size)
            elif op == PUSH0:  # 如果为PUSH0
                self.stack.append(0)
            elif op == POP:  # 如果为POP
                self.pop()
            elif op == ADD:  # 处理ADD指令
                self.add()
            elif op == MUL:  # 处理MUL指令
                self.mul()
            elif op == SUB:  # 处理SUB指令
                self.sub()
            elif op == DIV:  # 处理DIV指令
                self.div()
            elif op == SDIV:
                self.sdiv()
            elif op == MOD:
                self.mod()
            elif op == SMOD:
                self.smod()
            elif op == ADDMOD:
                self.addmod()
            elif op == MULMOD:
                self.mulmod()
            elif op == EXP:
                self.exp()
            elif op == SIGNEXTEND:
                self.signextend()
            elif op == LT:
                self.lt()
            elif op == GT:
                self.gt()
            elif op == SLT:
                self.slt()
            elif op == SGT:
                self.sgt()
            elif op == EQ:
                self.eq()
            elif op == ISZERO:
                self.iszero()
            elif op == AND:  # 处理AND指令
                self.and_op()
            elif op == OR:  # 处理AND指令
                self.or_op()
            elif op == XOR:  # 处理AND指令
                self.xor_op()
            elif op == NOT:  # 处理AND指令
                self.not_op()
            elif op == BYTE:  # 处理AND指令
                self.byte_op()
            elif op == SHL:  # 处理AND指令
                self.shl()
            elif op == SHR:  # 处理AND指令
                self.shr()
            elif op == SAR:  # 处理AND指令
                self.sar()
            elif op == MLOAD:  # 处理MLOAD指令
                self.mload()
            elif op == MSTORE:  # 处理MSTORE指令
                self.mstore()
            elif op == MSTORE8:  # 处理MSTORE8指令
                self.mstore8()
            elif op == MSIZE:  # 处理MSIZE指令
                self.msize()
            else:
                raise Exception('Invalid opcode')


# if __name__ == '__main__':
# MSTORE
code = b"\x60\x02\x60\x20\x52"
evm = EVM(code)
evm.run()
print(evm.memory[0x20:0x40])
# 输出: [0, 0, 0, ..., 0, 2]
# MLOAD
code = b"\x60\x02\x60\x20\x52\x60\x20\x51"
evm = EVM(code)
evm.run()
print(evm.memory[0x20:0x40])
# 输出: [0, 0, 0, ..., 0, 2]
print(evm.stack)
# output: [2]
