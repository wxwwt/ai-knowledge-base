"""
演示命名空间包 vs 普通包的区别
"""

print("=" * 60)
print("Python 3.3+ 的两种包类型")
print("=" * 60)

print("""
1. 命名空间包（Namespace Package）
   - 没有 __init__.py
   - 只能导入模块，不能导入包本身
   - 不能有包级别的变量/函数
   
2. 普通包（Regular Package）
   - 有 __init__.py
   - 可以导入包本身
   - 可以有包级别的变量/函数
   - 可以控制导入行为
""")

print("=" * 60)
print("实际区别演示")
print("=" * 60)

# 命名空间包（没有 __init__.py）
try:
    from demo_namespace_package.package_a import func1
    print("✅ 命名空间包：可以导入模块")
except ImportError as e:
    print(f"❌ 错误: {e}")

try:
    import demo_namespace_package.package_a
    print("✅ 命名空间包：可以 import 包名")
except ImportError as e:
    print(f"❌ 错误: {e}")

# 普通包（有 __init__.py）
try:
    from demo_namespace_package.package_b import func2
    print(f"✅ 普通包：可以直接导入包级别的函数: {func2()}")
except ImportError as e:
    print(f"❌ 错误: {e}")

print("\n" + "=" * 60)
print("总结")
print("=" * 60)
print("""
__init__.py 在 Python 3.3+ 中的作用：

1. ✅ 标识作用：标记为普通包（不是命名空间包）
2. ✅ 功能作用：可以定义包级别的代码、变量、函数
3. ✅ 控制作用：可以简化导入路径（from package import func）
4. ✅ 初始化作用：包被导入时执行初始化代码

所以不仅仅是"标识"，还有实际的功能作用！
""")


