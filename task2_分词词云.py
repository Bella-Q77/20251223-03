import os
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname='simhei.ttf', size=12) if os.path.exists('simhei.ttf') else None

# 读取停用词
with open('停用词.txt', 'r', encoding='utf-8') as f:
    stopwords = set([line.strip() for line in f if line.strip()])

# 读取专有词汇词典
with open('专有词汇词典.txt', 'r', encoding='utf-8') as f:
    custom_dict = [line.strip() for line in f if line.strip()]

# 将专有词汇添加到jieba词典
for word in custom_dict:
    jieba.add_word(word)

# 读取红楼梦文本
with open('红楼梦文本(UTF-8).txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 预处理文本：去除标点符号和特殊字符
text = re.sub(r'[^\w\s]', '', text)

# 使用jieba分词
words = jieba.lcut(text)

# 去除停用词
filtered_words = [word for word in words if word not in stopwords and len(word) > 1]

# 统计词频
word_freq = {}
for word in filtered_words:
    word_freq[word] = word_freq.get(word, 0) + 1

# 按词频排序
sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

# 取前150个词
top_words = sorted_words[:150]

print('前20个高频词:')
for word, freq in top_words[:20]:
    print(f'{word}: {freq}')

# 生成词云
# 检查是否有中文字体文件
if os.path.exists('simhei.ttf'):
    wc = WordCloud(
        font_path='simhei.ttf',
        width=800,
        height=600,
        background_color='white',
        max_words=150,
        max_font_size=100,
        random_state=42
    )
else:
    # 如果没有中文字体，使用默认字体（可能无法正确显示中文）
    wc = WordCloud(
        width=800,
        height=600,
        background_color='white',
        max_words=150,
        max_font_size=100,
        random_state=42
    )

# 生成词云
wc.generate_from_frequencies({word: freq for word, freq in top_words})

# 显示词云
plt.figure(figsize=(12, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('红楼梦高频词云图', fontproperties=font, fontsize=16)

# 保存词云
plt.savefig('红楼梦词云图.png', dpi=300, bbox_inches='tight')
plt.show()

print('\n红楼梦词云图已保存为: 红楼梦词云图.png')

# 保存词频统计结果
with open('高频词统计.txt', 'w', encoding='utf-8') as f:
    for word, freq in top_words:
        f.write(f'{word}: {freq}\n')

print('高频词统计结果已保存为: 高频词统计.txt')