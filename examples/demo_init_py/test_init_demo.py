"""
演示 __init__.py 的作用和区别
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("演示 1: 有 __init__.py 的包")
print("=" * 60)

# 导入有 __init__.py 的包
from examples.demo_init_py.package_with_init import hello, get_version, VERSION

print(f"✅ 可以直接导入函数: {hello()}")
print(f"✅ 可以直接导入函数: {get_version()}")
print(f"✅ 可以访问包变量: {VERSION}")

print("\n" + "=" * 60)
print("演示 2: 没有 __init__.py 的目录")
print("=" * 60)

# 导入没有 __init__.py 的目录（Python 3.3+）
from examples.demo_init_py.package_without_init.module_c import goodbye

print(f"✅ 仍然可以导入，但需要完整路径: {goodbye()}")

print("\n" + "=" * 60)
print("总结")
print("=" * 60)
print("""
__init__.py 的作用：

1. ✅ 标识包（Python 3.3 之前必须，3.3+ 可选但推荐）
2. ✅ 控制包的导入行为（简化导入路径）
3. ✅ 执行包初始化代码
4. ✅ 定义包的公共接口（__all__）
5. ✅ 使代码结构更清晰、更专业

最佳实践：
- 即使 Python 3.3+ 不强制要求，也建议创建 __init__.py
- 可以留空，也可以添加包级别的初始化代码
- 用于明确标识这是一个 Python 包，而不是普通目录
""")

