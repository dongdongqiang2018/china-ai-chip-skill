---
name: biren-sudebugger
description: BIREN suDebugger 调试器参考指南。基于 LLDB 实现的 GPU 调试器，提供断点设置、单步调试、变量查看、线程控制等功能，用于调试 BIRENSUPA 代码，支持 GMode 和 TCIP 范式。
keywords:
  - sudebugger
  - biren
  - 调试器
  - debugger
  - LLDB
  - GPU调试
  - 壁仞
---

# suDebugger Command Reference

suDebugger 是 BIRENSUPA SDK 开发工具集中的调试器组件，基于 LLDB 实现。

## Quick Start

```bash
# 编译时使用 -O0 -g -G 选项
brcc -O0 -g -G src.su -o test

# 启动调试
sudbg ./test

# 调试器输出
Connection established.
Process 1 stopped
* thread #1, stop reason = entry
>> <command>
```

## Installation

验证安装：
```bash
sudbg --version
```

## Debugging Flow

```
源代码 → BRCC 编译 → 可执行二进制 → debug server → debug client → 调试
```

远程调试架构：
1. 运行 debug server
2. 连接 debug client
3. 设置断点、单步执行
4. 查看变量和内存

## Command Line Options

| Option | Description |
|--------|-------------|
| `-l / --liblldb '<path>'` | 调试器依赖的 brcc 库路径 |
| `-p / --port '<num>'` | 调试器运行时的启动端口 |

## Debug Commands

### Start and Exit

| Long Command | Short Command | Description |
|--------------|---------------|-------------|
| `restart` | `r` | 连接下一个 kernel 进行调试 |
| `exit` | `q` | 断开 server，退出调试器 |

### Step Debugging

| Long Command | Short Command | Description |
|--------------|---------------|-------------|
| `thread step-over` | `n` | 单步执行，跳过函数调用 |
| `thread step-in` | `s` | 单步进入，不忽略函数调用 |
| `thread step-out` | `finish` | 单步退出，从 callee 返回 caller |
| `thread continue` | `th c` | 单步继续，直到断点或异常 |

### Breakpoints

| Long Command | Short Command | Description |
|--------------|---------------|-------------|
| `breakpoint set --name <symbol>` | `b <symbol>` | 在函数名/方法名上设置断点 |
| `breakpoint set --file <file> --line <n>` | `b <file:n>` | 在文件行号上设置断点 |
| `breakpoint delete <id>` | `br del <id>` | 删除断点 |
| `breakpoint enable <id>` | `br en <id>` | 使能断点 |
| `breakpoint disable <id>` | `br dis <id>` | 关闭断点 |
| `breakpoint list` | `br l` | 列出所有断点 |

### Thread and Stack

| Long Command | Short Command | Description |
|--------------|---------------|-------------|
| `thread select <id>` | `t <id>` | 切换到指定 GPU 线程 |
| `thread list` | `th l` | 查看 GPU 当前 warp 线程 |
| `frame select <id>` | `f <id>` | 切换栈帧 |
| `thread backtrace` | `bt` | 查看全部调用栈信息 |

### Print

| Long Command | Short Command | Description |
|--------------|---------------|-------------|
| `frame variable <var>` | `p <var>` | 打印局部变量 |
| `memory read <addr>` | `x <addr>` | 打印地址的 tlm 内存 |

## Supported Modes

- **GMode**: 基础模式
- **TCIP**: 模式（不支持 TCI 和 CWarp）

## Limitations

1. 不支持类似 gdb 的 restart 命令重启调试线程（GPU 调试器 restart 含义是进入下一个 kernel）
2. if/else 分支调试时可能不符合预期直觉
3. 无法打印 host 侧变量
4. 无法打印 workitem 相关变量（如 `thread_idx`）
5. 无法打印 device 侧全局变量及 `__shared__` 修饰符定义的变量

## Compilation Options

```bash
# 编译时务必使用 -O0 -g -G 选项
brcc -O0 -g -G src.su -o test
```

| Option | Description |
|--------|-------------|
| `-O0` | 关闭优化，便于调试 |
| `-g` | 生成主机端调试信息 |
| `-G` | 生成设备端调试信息 |

## Example Session

```bash
# 编译
brcc -O0 -g -G vector_add.su -o vector_add

# 启动调试
sudbg ./vector_add

# 设置断点
(b) vectorAdd

# 运行到断点
(th) c

# 单步执行
(n)

# 打印变量
(p) i

# 退出
(q)
```

## Notes

- 需要使用 -G 选项编译以提供准确的源程序位置信息
- 基于 brSimulator 实现
- 适合功能调试，不适合性能调试

## Related Tools

- **brSimulator**: 仿真器
- **suSanitizer**: 检查工具
- **BRCC**: 编译器