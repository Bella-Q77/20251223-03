import os
import re
import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname='simhei.ttf', size=10) if os.path.exists('simhei.ttf') else None

# 读取社交网络权重数据
edges = []
node_count = {}

with open('红楼梦社交网络权重.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        first = row['First']
        second = row['Second']
        chapweight = float(row['chapweight'])
        duanweight = float(row['duanweight'])
        
        edges.append((first, second, chapweight, duanweight))
        
        # 统计节点出现次数
        node_count[first] = node_count.get(first, 0) + 1
        node_count[second] = node_count.get(second, 0) + 1

# 计算总段落数（从第一个任务的结果中获取，或者这里重新计算）
# 由于第一个任务已经统计了总段落数，这里先假设一个值，实际运行时可以修改
# 或者我们可以重新计算总段落数
with open('红楼梦文本(UTF-8).txt', 'r', encoding='utf-8') as f:
    text = f.read()
    # 分割段落
    paragraphs = re.split(r'\n{2,}|。\n', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    total_paragraphs = len(paragraphs)

print(f'总段落数: {total_paragraphs}')

# 创建图
G = nx.Graph()

# 添加节点和边
for first, second, chapweight, duanweight in edges:
    # 计算新的weight: chapweight / total_paragraphs
    weight = chapweight / total_paragraphs
    
    # 降低阈值，确保有足够的边被保留
    if weight > 0.005:  # 从0.04降低到0.005
        G.add_edge(first, second, weight=weight)

# 检查图中是否有节点和边
print(f'图中节点数: {G.number_of_nodes()}')
print(f'图中边数: {G.number_of_edges()}')

# 按节点出现次数排序
sorted_nodes = sorted(node_count.items(), key=lambda x: x[1], reverse=True)

print('按出现次数排序的前20个节点:')
for node, count in sorted_nodes[:20]:
    print(f'{node}: {count}')

# 定义节点布局算法
# 调整布局参数，确保节点分布更合理
pos = nx.spring_layout(G, seed=42, k=0.3, iterations=200)

# 绘制网络图
plt.figure(figsize=(16, 12))

# 绘制边
edges = G.edges(data=True)
weights = [d['weight'] for u, v, d in edges]
# 调整边的宽度和透明度
nx.draw_networkx_edges(G, pos, edgelist=edges, width=[w*50 for w in weights], alpha=0.7, edge_color='darkblue')

# 绘制节点
# 调整节点大小和颜色
node_sizes = [node_count.get(node, 0) * 50 for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.8, node_color='crimson')

# 绘制节点标签
if font:
    nx.draw_networkx_labels(G, pos, font_properties=font, font_size=10, font_color='black')
else:
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

# 添加标题
plt.title('红楼梦人物社交网络图', fontproperties=font, fontsize=16)

# 隐藏坐标轴
plt.axis('off')

# 保存图表
plt.savefig('人物社交网络图.png', dpi=300, bbox_inches='tight')
plt.show()

print('\n人物社交网络图已保存为: 人物社交网络图.png')

# 保存网络数据
nx.write_gexf(G, '人物社交网络.gexf')
print('人物社交网络数据已保存为: 人物社交网络.gexf')