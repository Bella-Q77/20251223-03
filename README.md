请查看任务文件中的文档。我需要完成以下分析任务：

1、对 红楼梦文本(UTF-8).txt 中的章节、段落及其字数作出统计分析，结果用散点图展示。

2、对 红楼梦文本(UTF-8).txt 进行分词，并去除停用词，最后以词云图的形式展示出现最多的150个词。

3、基于 红楼梦社交网络权重.csv ，使用其中的chapweight除以段落总数作为新的weight，选取weight >0.04的数据，使用pos=nx.spring_layout(G)语句来定义网络的节点布局算法，然后使用nx.draw_networkx_nodes()、nx.draw_networkx_edges()、nx.draw_networkx_labels()绘制网络的节点、边和标签，生成人物社交网络图。社交网络图中的节点按照统计数量依次排列。
