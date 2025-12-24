# 红楼梦文本分析与可视化
import re
import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 任务1：统计章节、段落及其字数
print("任务1：章节、段落及其字数统计分析")
with open('红楼梦文本(UTF-8).txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 提取章节
chapters = re.split(r'第[一二三四五六七八九十百]+回', text)
chapters = [chapter.strip() for chapter in chapters if chapter.strip()]

# 统计每个章节的段落数和字数，以及每个段落的字数
chapter_stats = []
paragraph_stats = []
for i, chapter in enumerate(chapters, 1):
    paragraphs = [p.strip() for p in chapter.split('\n') if p.strip()]
    paragraph_count = len(paragraphs)
    word_count = sum(len(p) for p in paragraphs)
    chapter_stats.append({'章节': i, '段落数': paragraph_count, '字数': word_count})
    
    # 统计每个段落的字数
    for j, para in enumerate(paragraphs, 1):
        paragraph_stats.append({'章节': i, '段落': j, '字数': len(para)})

# 转换为DataFrame
chapter_df = pd.DataFrame(chapter_stats)
paragraph_df = pd.DataFrame(paragraph_stats)
print("章节统计结果：")
print(chapter_df.head())
print(f"总章节数：{len(chapter_df)}")
print(f"总段落数：{chapter_df['段落数'].sum()}")
print(f"总字数：{chapter_df['字数'].sum()}")

print("\n段落统计结果：")
print(paragraph_df.head(20))
print(f"总段落数：{len(paragraph_df)}")
print(f"平均段落字数：{paragraph_df['字数'].mean():.2f}")
print(f"最长段落字数：{paragraph_df['字数'].max()}")
print(f"最短段落字数：{paragraph_df['字数'].min()}")

# 绘制散点图：章节字数
plt.figure(figsize=(12, 8))
plt.scatter(chapter_df['章节'], chapter_df['字数'], alpha=0.6, color='blue', label='章节字数')
plt.xlabel('章节')
plt.ylabel('字数')
plt.title('红楼梦章节字数统计散点图')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('章节字数统计散点图.png', dpi=300, bbox_inches='tight')
plt.close()
print("章节字数统计散点图已生成：章节字数统计散点图.png")

# 绘制散点图：段落字数
plt.figure(figsize=(12, 8))
plt.scatter(range(len(paragraph_df)), paragraph_df['字数'], alpha=0.6, color='red', label='段落字数')
plt.xlabel('段落序号')
plt.ylabel('字数')
plt.title('红楼梦段落字数统计散点图')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('段落字数统计散点图.png', dpi=300, bbox_inches='tight')
plt.close()
print("段落字数统计散点图已生成：段落字数统计散点图.png")

# 绘制散点图：章节段落字数对比
plt.figure(figsize=(12, 8))
plt.scatter(chapter_df['章节'], chapter_df['字数'], alpha=0.6, color='blue', label='章节字数')
plt.scatter(chapter_df['章节'], chapter_df['段落数'], alpha=0.6, color='green', label='段落数')
plt.xlabel('章节')
plt.ylabel('数量')
plt.title('红楼梦章节、段落及其字数统计')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('章节段落字数统计散点图.png', dpi=300, bbox_inches='tight')
plt.close()
print("章节段落字数统计散点图已生成：章节段落字数统计散点图.png")

# 任务2：分词、去除停用词并生成词云
print("\n任务2：分词、去除停用词并生成词云")

# 加载停用词
with open('停用词.txt', 'r', encoding='utf-8') as f:
    stopwords = set([line.strip() for line in f if line.strip()])

# 加载专有词汇
with open('专有词汇词典.txt', 'r', encoding='utf-8') as f:
    for line in f:
        word = line.strip()
        if word:
            jieba.add_word(word)

# 分词并去除停用词
words = []
for chapter in chapters:
    paragraphs = [p.strip() for p in chapter.split('\n') if p.strip()]
    for para in paragraphs:
        seg_list = jieba.cut(para)
        words.extend([word for word in seg_list if word not in stopwords and len(word) > 1])

# 统计词频
word_freq = pd.Series(words).value_counts()
print("词频统计结果：")
print(word_freq.head(20))

# 生成词云
wc = WordCloud(
    font_path='simhei.ttf',  # 需要系统有黑体字体
    background_color='white',
    width=1200,
    height=800,
    max_words=150,
    margin=2
)
wc.generate_from_frequencies(word_freq)

plt.figure(figsize=(15, 10))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('红楼梦高频词汇词云图')
plt.savefig('红楼梦高频词汇词云图.png', dpi=300, bbox_inches='tight')
plt.close()
print("红楼梦高频词汇词云图已生成：红楼梦高频词汇词云图.png")

# 任务3：绘制人物社交网络图
print("\n任务3：绘制人物社交网络图")

# 读取社交网络数据
social_df = pd.read_csv('红楼梦社交网络权重.csv', encoding='utf-8')
print("社交网络数据：")
print(social_df.head())

# 计算新的weight：chapweight / 段落总数
total_paragraphs = chapter_df['段落数'].sum()
social_df['weight'] = social_df['chapweight'] / total_paragraphs
print(f"总段落数：{total_paragraphs}")
print("新的权重计算结果：")
print(social_df[['First', 'Second', 'chapweight', 'weight']].head())

# 选取weight > 0.04的数据
filtered_df = social_df[social_df['weight'] > 0.04]
print(f"筛选后的数据量：{len(filtered_df)}")
print("筛选后的数据：")
print(filtered_df.head())

# 创建网络图
G = nx.Graph()
for _, row in filtered_df.iterrows():
    G.add_edge(row['First'], row['Second'], weight=row['weight'])

# 计算节点布局
pos = nx.spring_layout(G, k=0.15, iterations=20)

# 绘制网络图
plt.figure(figsize=(18, 18))

# 绘制边
edges = G.edges(data=True)
edge_weights = [d['weight'] * 1000 for (u, v, d) in edges]  # 放大权重以便显示
nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray')

# 绘制节点
node_sizes = [G.degree(node) * 1000 for node in G.nodes()]  # 节点大小与度数成正比
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue', alpha=0.8)

# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=12, font_family='SimHei')

plt.title('红楼梦人物社交网络图（weight > 0.04）', fontsize=20)
plt.axis('off')
plt.savefig('红楼梦人物社交网络图.png', dpi=300, bbox_inches='tight')
plt.close()
print("红楼梦人物社交网络图已生成：红楼梦人物社交网络图.png")

print("\n所有任务完成！生成了以下文件：")
print("1. 章节段落字数统计散点图.png")
print("2. 红楼梦高频词汇词云图.png")
print("3. 红楼梦人物社交网络图.png")