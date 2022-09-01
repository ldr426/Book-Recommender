# coding: utf-8 -*-
import math
import pandas as pd


class UserCf:
    # 这个类的主要功能是提供一个基于用户的协同过滤算法
    
    def __init__(self):
        """初始化文件路径，读取书籍评分数据集"""
        self.file_path = './data/BX-Book-Ratings.csv'
        self._init_frame()

    def _init_frame(self):
        self.frame = pd.read_csv(self.file_path,sep=None, error_bad_lines=False)
        self.frame.columns=['UserID','BookID','Rating'] 

    @staticmethod
    def _cosine_sim(target_books, books):
        """
        计算余玄相似度，参考博客：https://blog.csdn.net/MassiveStars/article/details/79601666

         举个列子 空间上面有 2个点A,B。与坐标原点（0,0）组成AOB三角形，角AOB的度数越小，
         那么表示两个坐标点越相近。代入这个书籍推荐上面
         我们这样理解：
         用户A=[‘书1’，‘书2’，‘书3’]=['1','2','3'] ID代表书籍的编号
         用户B=[‘书4’，‘书2’，‘书6’]=['4','2','6'] ID代表书籍的编号
         用户C=[‘书7’，‘书8’，‘书9’]=['21','2','6'] ID代表书籍的编号
         如果用户A登录网址 思考一个问题 我们推荐用户B的书籍，还是用户C的给A？
         求cosAOB = X =26/（3.74*7.48）= 0.92
          cosAOC = Y =43/（3.74*21.9）= 0.525
          cos值越大，角度越小，越相似
         很明显 X > Y 那么 证明用户B距离用户A更近，即B的阅读兴趣与A跟相似，于是
         我们可以把B阅读的书籍推荐给A
         我们用这个方法可以得到最相似的用户，但是还得不到最适合推荐的书籍。这个可以在
         get_topn_items这个方法中解决。
        """
        union_len = len(set(target_books) & set(books))
        if union_len == 0: return 0.0
        product = len(target_books) * len(books)
        cosine = union_len / math.sqrt(product)
        return cosine

    def _get_top_n_users(self, target_user_id, top_n):
        """
        计算和当前用户最相似的top_n (此时top_n为10) 个用户
        :param target_user_id:当前计算的用户ID
        :param top_n: 需要计算的相似的用户数
        :return: 和当前用户最相似的top_n个用户
        """
        # 当前用户评价过的书籍列表
        target_books = self.frame[self.frame['UserID'] == target_user_id]['BookID']
        # 除去当前用户后的用户列表
        other_users_id = [i for i in set(self.frame['UserID']) if i != target_user_id]
        # 其他用户评价的书籍的集合
        other_books = [self.frame[self.frame['UserID'] == i]['BookID'] for i in other_users_id]

        # _cosine_sim()函数计算当前用户评分过的书籍target_books和其他用户评分过的书籍的余弦相似度，此相似度即为用户相似度
        sim_list = [self._cosine_sim(target_books, books) for books in other_books]
        # 将余弦相似度和userID通过zip函数组合起来并排序
        sim_list = sorted(zip(other_users_id, sim_list), key=lambda x: x[1], reverse=True)
        return sim_list[:top_n]

    def _get_candidates_items(self, target_user_id):
        """
        找出当前用户没有评分的所有书籍
        Find all books in source data and target_user did not meet before.
        """
        # 当前用户评价过的BookID
        target_user_books = set(self.frame[self.frame['UserID'] == target_user_id]['BookID'])
        # 当前用户未评价过的BookID
        other_user_books = set(self.frame[self.frame['UserID'] != target_user_id]['BookID'])
        # 不同时包含于target_user_books和other_user_books的元素
        candidates_books = list(target_user_books ^ other_user_books)
        return candidates_books

    def _get_top_n_items(self, top_n_users, candidates_books, top_n):
        """
            本函数用于计算给当前用户推荐度最高的top_n本书


            上面2个方法，依靠上面的注释的内容，我们得到了最相似的用户，那么用户中我们需要怎么推荐书籍？
            原理其实很容易理解：
            
            首先我们有全部用户对于不同书籍的评分，那么我们可以计算出每个书籍的平均得分。这个作为一个权重
            再去乘以之前用户的相似度。那么这个值以上面的例子来说
            用户A=[‘书1’，‘书2’，‘书3’]=['1','2','3'] ID代表书籍的编号
            用户B=[‘书4’，‘书2’，‘书6’]=['4','2','6'] ID代表书籍的编号
            用户C=[‘书7’，‘书8’，‘书9’]=['21','2','6'] ID代表书籍的编号
            
            用户A登录, 他阅读了‘书1’，‘书2’，‘书3’，假设数据库只有用户A，用户B，用户C。
            发现B,C都与A有共同兴趣，即看过书2，那么我们需要推送4,6,21，我们需要计算4,6,21的
            推荐度，并排序返回给A。
            
            那么怎么计算呢？
            
            首先，我们前面求出了A与B,C的相似度。这个值乘以每本书在书籍评分数据的平均值。这样4，21的是可以直接
            得到的，而关于6，我们需要将B的匹配度加上C匹配度（因为B与C都对6进行了评分）。
            
            最后我们得到的一个表格为
            【 书本ID，匹配度 】
            【  xxxxx    1.223】
            【  xxxxx    1.223】
            【  xxxxx    0.423】
            【  xxxxx    1.323】
            【  xxxxx    0.023】
            【  xxxxx    0.000】
    
            我们再对这个表格排序 将前TOPN推荐给用户A。
        """
        # 选取出当前用户最相似的top_n个用户的数据
        top_n_user_data = [self.frame[self.frame['UserID'] == k] for k, _ in top_n_users]
        interest_list = []
        # 遍历当前用户为评分的书籍以及和当前用户最相似的top_n个用户
        for book_id in candidates_books:
            tmp = []
            for user_data in top_n_user_data:
                # 如果遍历的用户对当前书籍评分过，则取出当前对book_id的评分并取平均值；如果未评分，则置为0
                if book_id in user_data['BookID'].values:
                    readdf = user_data[user_data['BookID'] == book_id]
                    tmp.append(round(readdf['Rating'].mean(), 2))
                else:
                    tmp.append(0)
            # 计算top_n个用户对当前书籍的评分值与余弦相似度的乘积，并将其相加，作为当前书籍的兴趣值
            interest = sum([top_n_users[i][1] * tmp[i] for i in range(len(top_n_users))])
            # 将最终所得值和book_id关联，作为目标用户对当前书籍的感兴趣值
            interest_list.append((book_id, interest))
        # 按照兴趣值的从高到底进行排序
        interest_list = sorted(interest_list, key=lambda x: x[1], reverse=True)
        return interest_list[:top_n]

    def calculate(self, target_user_id, top_n):
        """
        基于用户的协同过滤
        :param target_user_id:用户编号
        :param top_n:推荐的书籍本数量
        :return:给当前用户推荐的书籍BookID以该书籍的评分score
        """
        # 计算和当前用户最相似的top_n个用户
        top_n_users = self._get_top_n_users(target_user_id, top_n)
        # 计算当前用户没有评分的所有书籍
        candidates_books = self._get_candidates_items(target_user_id)
        # 计算当前用户最感兴趣的10本书
        top_n_books = self._get_top_n_items(top_n_users, candidates_books, top_n)
        
        print(top_n_books)
        name = []
        values = []
        # 遍历推荐书籍列表，将其格式化为UserID、BookID和score形式
        for x in top_n_books:
            name.append(x[0])
            values.append(x[1])
        df = pd.DataFrame({'UserID': target_user_id, 'BookID': name, 'score': values})
        return df


def run(i):
    """
    run函数可以进行多线程的计算，调用calculate函数计算单个user的书籍推荐表DF，计算完成后将DF合并到res中
    :param i: 用户编号
    """
    # 全局的res
    global res
    target_user_id = users[i]
    DF = usercf.calculate(target_user_id, top_n)
    res = res.append(DF)
    

# ————————————————————————————————————————
#  ****************从这里开始阅读***************
# ---------------------------------------------------------------------------------------------------------------
#   关于协同过滤，可以阅读如下博文：https://www.cnblogs.com/NeilZhang/p/9900537.html
#   数据集下载链接（其中有对数据集详细的介绍）：http://www2.informatik.uni-freiburg.de/~cziegler/BX/
#   该数据集中，User表有278858条数据，Ratings表有1149780条数据，Book表有271360条数据


#   本程序的功能是，从100W的评分数据中，随机的挑选20个用户，通过协同过滤算法计算给这些用户推荐的10本书。
#   其中只选取20个用户是因为数据量过大，如果计算出给所有用户推荐的10本书将会耗费大量的资源和时间，后续可以根据机期的配置，调整用户数量
#   top_n = 10 表示我们推荐的书籍为计算出来推荐度的序列中的前10本书。如果在这10本书之中，存在推荐度的推荐书籍小于10.会随机拿书籍补全
# ----------------------------------------------------------------------------------------------------------------
import random
# 读取书籍评分数据，数据的三列分别是UserID, BookID, Rating
path = './data/BX-Book-Ratings.csv'
Data = pd.read_csv(path, sep=None, error_bad_lines=False)
Data.columns = ['UserID', 'BookID', 'Rating']
# 创建用于存储最终结果的DataFrame
res = pd.DataFrame(columns=['UserID', 'BookID', 'score'])
# 初始化User类，在初始化时，会调用其__init__(self)方法
usercf = UserCf()

# 随机的选取20次,set是不重复元素的集合
users = [random.choice(list(set(Data['UserID']))) for x in range(20)]
# 推荐10本书
top_n = 10
# 根据随机选取的20个用的编号，开启20个线程开始计算推荐的书籍
for x in range(len(users)):
    print(x)
    run(x)
    print(res)
# 将计算完全的数据输出为文件
res.to_csv('./data/booktuijian.csv', index=False)
