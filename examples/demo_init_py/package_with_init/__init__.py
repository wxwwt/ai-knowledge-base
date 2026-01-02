"""
有 __init__.py 的包示例
"""

# 1. 定义包的公共接口
__all__ = ['hello', 'get_version']

# 2. 包级别的初始化代码
print("📦 package_with_init 被导入，执行初始化代码")

# 3. 简化导入路径（可选）
from .module_a import hello
from .module_b import get_version

# 4. 包级别的变量
VERSION = "1.0.0"


