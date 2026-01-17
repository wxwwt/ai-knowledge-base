# examples/rag/chapter03/ex07_hybrid_retrieve_run.py
# 混合检索运行示例

from examples.rag.chapter03.documents import DOCUMENTS
from examples.rag.chapter03.retrieve.hybrid_retrieve import hybrid_retrieve

def main():
    # 测试查询
    query = "什么是蓝精灵协议？"
    
    print("=" * 60)
    print(f"查询: {query}")
    print("=" * 60)
    print()
    
    # 执行混合检索
    results = hybrid_retrieve(
        query=query,
        documents=DOCUMENTS,
        top_k_rule=5,
        top_k_vector=5,
        debug=True
    )
    
    print()
    print("=" * 60)
    print("最终结果（按综合分数排序）")
    print("=" * 60)
    
    for i, item in enumerate(results, 1):
        print(f"\n[{i}] 分数: {item.score:.2f}")
        print(f"    来源: {item.sources}")
        if item.rule_score is not None:
            print(f"    规则分数: {item.rule_score:.2f}")
        if item.vector_score is not None:
            print(f"    向量分数: {item.vector_score:.2f}")
        print(f"    内容: {item.document.page_content[:100]}...")
        print(f"    项目: {item.document.metadata.get('project', 'N/A')}")

if __name__ == "__main__":
    main()
