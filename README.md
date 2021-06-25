<center><h1>焦虑中的孩子们 —— “985废物引进计划” 豆瓣小组人物画像</h1></br>
小组成员： 刘圳 01180107   刘雅欣 14190205</center>




## 一、**作业目标**

本作业希望回答以下问题

1. > 1. 这一特殊群体关心的领域和话题是什么
   > 2. 帖文的显著主题是什么，有什么
   > 3. 不同话题之间的关联性有多大
   > 4. 在这样一个有自我否定倾向的小组内，成员的情感倾向如何

## 二、**作业数据**来源

通过网络爬取豆瓣“985 废物引进计划小组”的帖文与回复等非结构化数据，以及用户 id，链接，成员关系等结构化数据。由于网络代理失效、爬虫规则限制以及电脑性能等多方因素，我们仅爬取了 10 万字级别的的文本。但我们希望扩展至对 GB 甚至 TB 级别的文本进行真正的大数据分析。



## 三、**作业方法与结果分析**

1. 1. #### 词频统计与增量聚类

      目前有关增量聚类的研究主要是将增量数据看成是时间序列数据或按特定顺序的数据, 主要可以分成两类: 一类是每次将所有数据进行迭代,即从第一个数据到最后一个数据进行迭代运算, 其优点是精度高, 不足之处是不能利用前一次聚类的结果, 浪费资源; 另一类是利用上一次聚类的结果,每次将一个数据点划分到已有簇中, 即新增的数据点被划入中心离它最近的簇中并将中心移向新增的数据点, 也就是说新增的数据点不会影响原有划分, 其优点是不需要每次对所有数据进行重新聚类, 不足之处是泛化能力弱, 监测不出孤立点。因此, 如何设计增量聚类算法以提高聚类效率, 成为当前聚类分析的一个重要挑战。现在很多聚类算法都是对单一数据类型的数据进行聚类, 但是现实数据中非常多的数据都是混合数据类型的数据, 既包含数值属性数据, 还是分类属性数据, 简单地丢弃其中一种数据类型, 或者将其中一种数据类型转换成另一种, 都会影响聚类的精度。因此, 混合属性数据增量聚类的研究具有非常重要的意义。

      

      词频统计见我们代码包内 ‘wordcount’ 文件夹

      ```shell
      >>> {'想', '学校', '喜欢', '真的', '实习', '专业', '大学', '朋友', '生活', '考研', '工作', '毕业', '时间', '学习', '感觉', '同学', '找', '做', '里', '面试', '老师', '公司', '家里', ‘月'}
      ```

      

   2. #### 基于 TextRank 的文本关键词抽取方法

      TextRank算法是基于PageRank算法的。PageRank算法的核心思想是，网页重要性由两部分组成：

   3. 1. - 如果一个网页被大量其他网页链接到说明这个网页比较重要，即被链接网页的数量；
         - 如果一个网页被排名很高的网页链接说明这个网页比较重要，即被链接网页的权重。

   4. TextRank算法在PageRank算法的思路上做了改进。该算法把文本拆分成词汇作为网络节点，组成词汇网络图模型，将词语间的相似关系看成是一种推荐或投票关系，使其可以计算每一个词语的重要性。基于TextRank的文本关键词抽取是利用局部词汇关系，即共现窗口，对候选关键词进行排序，该方法的步骤如下：

   5. > （1） 对于给定的文本D进行分词、词性标注和去除停用词等数据预处理操作。本分采用结巴分词，保留'n','nz','v','vd','vn','l','a','d'这几个词性的词语，最终得到n个候选关键词，即D=[t1,t2,…,tn] ；
      >
      > （2） 构建候选关键词图G=(V,E)，其中V为节点集，由候选关键词组成，并采用共现关系构造任两点之间的边，两个节点之间仅当它们对应的词汇在长度为K的窗口中共现则存在边，K表示窗口大小即最多共现K个词汇； 
      >
      > （3） 根据公式迭代计算各节点的权重，直至收敛；
      >
      > （4） 对节点权重进行倒序排列，得到排名前TopN个词汇作为文本关键词。

   6. Jieba 库中 jieba.analyse.textrank 函数可直接实现 TextRank 算法，本文采用该函数进行实验。基于TextRank方法实现文本关键词抽取的代码执行步骤如下：

   7. > （1）读取样本源文件sample_data.csv;
      >
      > （2）获取每行记录的标题和摘要字段，并拼接这两个字段；
      >
      > （3）加载自定义停用词表stopwords.txt;
      >
      > （4）遍历文本记录，采用 jieba.analyse.textrank 函数筛选出指定词性，以及 top N个文本关键词，并将结果存入数据框中；
      >
      > （5）将最终结果写入文件keys_TextRank.csv中

   8. ![截屏2021-06-25 上午9.17.46](/Users/lydia/Desktop/截屏2021-06-25 上午9.17.46.png)

   9. 

2. 3. #### 文本聚类

3. 1. - ##### KMeans 聚类

   2. k均值聚类算法（k-means clustering algorithm）是一种迭代求解的聚类分析算法，其步骤是，预将数据分为K组，则随机选取K个对象作为初始的聚类中心，然后计算每个对象与各个种子聚类中心之间的距离，把每个对象分配给距离它最近的聚类中心。聚类中心以及分配给它们的对象就代表一个聚类。每分配一个样本，聚类的聚类中心会根据聚类中现有的对象被重新计算。这个过程将不断重复直到满足某个终止条件。终止条件可以是没有（或最小数目）对象被重新分配给不同的聚类，没有（或最小数目）聚类中心再发生变化，误差平方和局部最小。

   3. 聚类结果：

   4. ```shell
      0: [11, 19, 20, 21, 26, 31, 36, 56, 61, 62, 66, 68, 70, 75, 78, 93, 98, 105, 108, 111, 113, 118, 134, 160, 175, 179, 184, 194, 196, 201, 207, 212, 217, 236, 240, 243, 245, 248, 250, 266, 283, 284, 296, 306, 307, 308, 311, 312, 313, 324, 334, 338, 339, 352, 354, 357, 359, 361, 364, 370, 371, 376, 380, 383, 384, 387, 389, 392, 395, 400, 405, 408, 415]
      
      1: [2, 3, 5, 6, 8, 10, 14, 18, 23, 24, 29, 41, 48, 50, 53, 58, 64, 65, 73, 80, 92, 94, 95, 97, 99, 100, 106, 119, 125, 132, 142, 145, 146, 151, 158, 168, 171, 172, 182, 188, 197, 203, 204, 209, 214, 227, 228, 235, 237, 238, 241, 246, 253, 255, 256, 257, 264, 267, 272, 277, 282, 293, 294, 295, 298, 301, 302, 303, 332, 342, 344, 346, 366, 378, 379, 386, 388, 391, 393, 397, 404, 416, 427]
      
      2: [0, 9, 13, 47, 55, 60, 114, 128, 136, 140, 154, 162, 166, 258, 271, 276, 368, 413, 414]
      
      3: [7, 17, 27, 32, 35, 49, 51, 52, 54, 57, 59, 63, 71, 77, 81, 90, 102, 109, 110, 115, 122, 131, 138, 148, 157, 164, 222, 223, 239, 242, 247, 262, 270, 274, 275, 279, 288, 292, 333, 341, 343, 356, 363, 365, 367, 373, 399, 406, 412]
      
      4: [1, 4, 12, 15, 16, 22, 25, 28, 30, 33, 34, 37, 38, 39, 40, 42, 43, 44, 45, 46, 67, 69, 72, 74, 76, 79, 82, 83, 84, 85, 86, 87, 88, 89, 91, 96, 101, 103, 104, 107, 112, 116, 117, 120, 121, 123, 124, 126, 127, 129, 130, 133, 135, 137, 139, 141, 143, 144, 147, 149, 150, 152, 153, 155, 156, 159, 161, 163, 165, 167, 169, 170, 173, 174, 176, 177, 178, 180, 181, 183, 185, 186, 187, 189, 190, 191, 192, 193, 195, 198, 199, 200, 202, 205, 206, 208, 210, 211, 213, 215, 216, 218, 219, 220, 221, 224, 225, 226, 229, 230, 231, 232, 233, 234, 244, 249, 251, 252, 254, 259, 260, 261, 263, 265, 268, 269, 273, 278, 280, 281, 285, 286, 287, 289, 290, 291, 297, 299, 300, 304, 305, 309, 310, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 325, 326, 327, 328, 329, 330, 331, 335, 336, 337, 340, 345, 347, 348, 349, 350, 351, 353, 355, 358, 360, 362, 369, 372, 374, 375, 377, 381, 382, 385, 390, 394, 396, 398, 401, 402, 403, 407, 409, 410, 411, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426]
      ```

   5. 

   6. - ##### DBScan 聚类

   7. 与基于距离的聚类算法不同的是，基于密度的聚类算法可以发现任意形状的聚类。在基于密度的聚类算法中，通过在数据集中寻找被低密度区域分离的高密度区域，将分离出的高密度区域作为一个独立的类别。可以对任意形状的稠密数据集进行聚类，相对的，K-Means之类的聚类算法一般只适用于凸数据集。DBScan 算法还可以在聚类的同时发现异常点，对数据集中的异常点不敏感。

   8. 在 scikit-learn 中的 DBSCAN API 为 ——

   9. ```python
      def __init__(self, eps=0.5, min_samples=5, metric='euclidean',
                       metric_params=None, algorithm='auto', leaf_size=30, p=None,
                       n_jobs=1):
      ```

   10. 其中，核心参数：

   11. - eps: float，ϵ-邻域的距离阈值
       - min_samples ：int，样本点要成为核心对象所需要的 ϵ-邻域的样本数阈值

   12. 属性：

   13. - core_sample_indices_ : 核心点的索引，因为labels_不能区分核心点还是边界点，所以需要用这个索引确定核心点
       - components_：训练样本的核心点
       - labels_：每个点所属集群的标签，-1代表噪声点

   14. 优点为 ——

   15. - 不需要用户先验地设置簇的个数，可以划分具有复杂形状的簇，还可以找出不属于任何簇的点。
       - 可以对任意形状的稠密数据集进行聚类，相对的，K-Means之类的聚类算法一般只适用于凸数据集。
       - 可以在聚类的同时发现异常点，对数据集中的异常点不敏感。
       - DBSCAN 比凝聚聚类和 k 均值稍慢，但仍可以扩展到相对较大的数据集。

   16. 缺点为我们需要设置 eps

   17. ![Figure_1](/Users/lydia/Desktop/Figure_1.png)

   18. 聚类分析结果：

   19. ```shell
       -1: [9, 85, 86, 146, 172, 203, 307, 312, 354, 361, 386, 388, 391, 393, 400], 
       0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 87, 88, 89, 90, 91, 93, 94, 95, 96, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 114, 115, 116, 117, 118, 119, 120, 121, 122, 124, 126, 127, 128, 129, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 145, 147, 148, 150, 152, 153, 154, 155, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 171, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 204, 205, 206, 207, 208, 209, 212, 213, 214, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 242, 243, 244, 245, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 308, 309, 310, 311, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 355, 356, 357, 358, 359, 360, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 380, 381, 382, 383, 384, 385, 387, 389, 390, 392, 394, 396, 397, 398, 399, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427]
       
       1: [24, 29, 241, 246]
       
       2: [92, 97, 379]
       
       3: [113, 339, 395]
       
       4: [123, 125, 149, 151]
       
       5: [130, 144, 156, 170]
       
       6: [210, 211, 215, 216]
       ```

   20. 

   21. - ##### LDA 算法

         LDA是常见的主题模型之一，是一类无监督学习算法，在训练时不需要手工标注的训练集，需要的仅仅是文档集以及指定主题的数量k即可。此外LDA的另一个优点则是，对于每一个主题均可找出一些词语来描述它。

         ###### 聚类分析结果

   22. ```shell
       Topic #0: 工作 学校 专业 985 实习 大学 学习 感觉 老师 真的
       Topic #1: 工作 专业 真的 毕业 生活 时间 感觉 学校 考研 朋友
       
       0: [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 23, 24, 29, 34, 35, 38, 39, 40, 41, 43, 45, 46, 48, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 65, 67, 69, 71, 73, 76, 77, 79, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 95, 100, 102, 103, 104, 105, 106, 107, 109, 112, 113, 114, 116, 120, 124, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 138, 139, 141, 142, 143, 145, 150, 152, 153, 154, 155, 158, 159, 160, 161, 162, 163, 164, 165, 167, 168, 169, 171, 175, 176, 177, 178, 183, 184, 185, 186, 187, 188, 189, 191, 192, 193, 195, 196, 197, 199, 200, 203, 206, 207, 212, 217, 219, 220, 224, 225, 226, 227, 228, 229, 230, 232, 233, 234, 235, 237, 238, 239, 241, 242, 246, 247, 250, 252, 253, 256, 257, 258, 259, 260, 262, 264, 265, 266, 267, 270, 271, 272, 274, 275, 276, 277, 279, 280, 282, 284, 285, 286, 288, 292, 293, 297, 298, 299, 300, 305, 307, 310, 312, 315, 317, 319, 321, 322, 323, 324, 325, 326, 327, 329, 332, 333, 334, 336, 337, 339, 343, 344, 345, 346, 347, 348, 351, 358, 365, 366, 367, 368, 369, 372, 373, 374, 375, 377, 380, 381, 382, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 399, 400, 401, 402, 413, 414, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427]
       
       1: [3, 4, 5, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 30, 31, 32, 33, 36, 37, 42, 44, 47, 49, 50, 63, 64, 66, 68, 70, 72, 74, 75, 78, 80, 81, 92, 93, 94, 96, 97, 98, 99, 101, 108, 110, 111, 115, 117, 118, 119, 121, 122, 123, 125, 130, 131, 140, 144, 146, 147, 148, 149, 151, 156, 157, 166, 170, 172, 173, 174, 179, 180, 181, 182, 190, 194, 198, 201, 202, 204, 205, 208, 209, 210, 211, 213, 214, 215, 216, 218, 221, 222, 223, 231, 236, 240, 243, 244, 245, 248, 249, 251, 254, 255, 261, 263, 268, 269, 273, 278, 281, 283, 287, 289, 290, 291, 294, 295, 296, 301, 302, 303, 304, 306, 308, 309, 311, 313, 314, 316, 318, 320, 328, 330, 331, 335, 338, 340, 341, 342, 349, 350, 352, 353, 354, 355, 356, 357, 359, 360, 361, 362, 363, 364, 370, 371, 376, 378, 379, 383, 397, 398, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 415]
       ```

   23. 

4. 4. #### 情感分析

5. 1. - ##### SnowNLP 情感分析  & Cnsenti Python 扩展

   2. 中文情感分析库(Chinese Sentiment))可对文本进行情绪分析、正负情感分析。情感分析默认使用的知网 Hownet，可支持导入自定义 txt 情感词典（pos 和 neg)。并且使用大连理工大学情感本体库，可以计算文本中的七大情绪词(好、乐、哀、怒、惧、恶、惊)分布。其中，sentiment_count() 方法统计正负情感极数，sentiment_calculate() 则可更加精准的计算文本的情感信息。相比于 sentiment_count 只统计文本正负情感词个数，sentiment_calculate还考虑了情感词前是否有强度副词的修饰作用，以及情感词前是否有否定词的情感语义反转作用。

   3. 最终运行结果为 

   4. ![](/Users/lydia/Desktop/截屏2021-06-25 上午12.01.18.png)

6. 1. ```python
      >>> {'words': 74250, 'sentences': 2682, '好': 1861, '乐': 509, '哀': 297, '怒': 12, '惧': 125, '恶': 1154, '惊': 38}
      
      >>> {'words': 74250, 'sentences': 2681, 'pos': 2800, 'neg': 2699}
      
      >>> {'sentences': 2681, 'words': 74250, 'pos': 82444.75, 'neg': 113360.75}
      ```

   2. 导出情感概率分布为：

   3. ![Figure_2](/Users/lydia/Desktop/Figure_2.png)

## 四、**作业性能评价**

1. 1. 增量聚类：没有考虑时间问题，只考虑了出现频率
   2. LDA选择的是分类性能最好的投影，而PCA选择样本点投影具有最大方差的方向。LDA 以标签，类别衡量差异性的有监督降维方式，相对于PCA的模糊性，其目的更明确，更能反映样本间的差异。缺点是，局限性大，受样本种类限制，投影空间的维数最多为样本数量N-1维。

## 五、作业总结

在帖文数据中，疑问词及感受表达居多，大家普遍关注的话题集中于对未来的焦虑迷茫以及对现状的不满上，聚类与分词中对工作、专业、实习、考研等话题的讨论十分集中。

TextRank 中，我们抽取了每个帖子的帖文权重比最大的10个词汇，我们原本期望利用其建立关联矩阵，以及进行知识图谱的研究，但由于时间和知识限制，我们计划以后继续完善其。

在文本聚类中，我们发现大部分的帖文拥有同样的聚类，说明尽管学校不同，背景不同，大家对特定话题的关注有着惊人的一致，在3种聚类算法结果中，都有着规模极大的团簇，有着一致的关注对象。并且其与词频统计的结果很相像。

情感方面，通过对情感词前具有的强度副词的修饰作用，以及情感词前是否有否定词的情感语义反转作用进行了校正，前后的情感差距较大，后者比较准确的描述出了小组成员的心境，也说明小组内大家的语言与说辞有更深意，意含褒贬，是小组的一大特点，情感分类中占较大板块的“好”也并不一定全是好，很多也蕴含着对现状的反讽与调侃之意。



## 六、额外说明

1. 由于所有代码与实验均在 macOS 电脑上实现，且微软 Office 平台在 macOS 上有诸多小 bug，实际验证中需要注意 Excel 及 CSV 文件 GBK 格式与 UTF-8 格式的转换，我们利用了 Python 脚本查看文件编码格式。（事实上由于队员平台不统一带来的格式问题，诸多 Windows 平台下的简单操作都需要 macOS 端编写脚本兼容和处理，浪费了诸多精力） 

2. ```python
   import chardet
   path = "..."
   f = open(path, 'rb')
   data = f.read()
   print(chardet.detect(data))
   ```

3. 