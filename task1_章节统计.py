import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname='simhei.ttf', size=12) if os.path.exists('simhei.ttf') else None

# 读取红楼梦文本
with open('红楼梦文本(UTF-8).txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 统计章节（假设章节以第X回开头）
chapters = re.split(r'第[一二三四五六七八九十百]+回', text)
chapters = [chapter.strip() for chapter in chapters if chapter.strip()]

# 统计每个章节的段落数和字数
chapter_stats = []
total_paragraphs = 0

for i, chapter in enumerate(chapters, 1):
    # 分割段落（以两个换行符或句号加换行符分隔）
    paragraphs = re.split(r'\n{2,}|。\n', chapter)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    paragraph_count = len(paragraphs)
    total_paragraphs += paragraph_count
    
    # 统计字数
    word_count = sum(len(p) for p in paragraphs)
    
    chapter_stats.append({
        'chapter': f'第{i}回',
        'paragraph_count': paragraph_count,
        'word_count': word_count
    })
    
    print(f'章节 {i}: {paragraph_count} 段落, {word_count} 字')

print(f'\n总章节数: {len(chapters)}')
print(f'总段落数: {total_paragraphs}')

# 生成散点图
plt.figure(figsize=(12, 8))

# 提取数据
chapter_indices = np.arange(1, len(chapter_stats) + 1)
paragraph_counts = [stat['paragraph_count'] for stat in chapter_stats]
word_counts = [stat['word_count'] for stat in chapter_stats]

# 绘制散点图
plt.scatter(paragraph_counts, word_counts, alpha=0.6)

# 添加标题和标签
plt.title('红楼梦章节段落数与字数散点图', fontproperties=font, fontsize=16)
plt.xlabel('段落数', fontproperties=font, fontsize=12)
plt.ylabel('字数', fontproperties=font, fontsize=12)

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图表
plt.savefig('章节段落字数散点图.png', dpi=300, bbox_inches='tight')
plt.show()

print('\n章节段落字数散点图已保存为: 章节段落字数散点图.png')