/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80036
 Source Host           : localhost:3306
 Source Schema         : spark

 Target Server Type    : MySQL
 Target Server Version : 80036
 File Encoding         : 65001

 Date: 05/06/2024 00:10:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `students` json NULL,
  `teacher` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `teacher`(`teacher`) USING BTREE,
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`teacher`) REFERENCES `teacher` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------

-- ----------------------------
-- Table structure for error_questions
-- ----------------------------
DROP TABLE IF EXISTS `error_questions`;
CREATE TABLE `error_questions`  (
  `username` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `q_id` int(0) NOT NULL,
  `course` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `analysis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `knowledge` json NULL,
  `create_time` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`username`, `q_id`) USING BTREE,
  INDEX `q_id`(`q_id`) USING BTREE,
  CONSTRAINT `error_questions_ibfk_1` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `error_questions_ibfk_2` FOREIGN KEY (`q_id`) REFERENCES `question` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of error_questions
-- ----------------------------
INSERT INTO `error_questions` VALUES ('Admin', 11, '机器学习', '{\"Q\": \".一个正例（3,2),一个负例（-1,-2),下面哪个是SVM超平面？()\", \"A\": \".3x+y-6=0\", \"B\": \".4y+X-7=0\", \"C\": \".2x+3y-5=0\", \"D\": \".无法计算\", \"answer\": \"A\", \"course\": \"机器学习\", \"mu\": 37.06394678485648, \"sigma\": 3.177776021112566, \"leve\": 8, \"create_time\": 1716257421.0}', '智能分析', '{\"1\": \"知识点\"}', '2024-06-01 13:18:46');
INSERT INTO `error_questions` VALUES ('Admin', 24, '机器学习', '{\"Q\": \".假设有5个二维数据点：D={(2,3),(4,5),(6,7),(8,9),(10,11)},第一次切分时候，切分线为（)。\", \"A\": \".x=4\", \"B\": \".x=6\", \"C\": \".y=4\", \"D\": \".y=6\", \"answer\": \"A\", \"course\": \"机器学习\", \"mu\": 27.641219030256458, \"sigma\": 2.224925089562339, \"leve\": 10, \"create_time\": 1716257421.0}', '智能分析', '{\"1\": \"知识点\"}', '2024-06-01 13:20:40');
INSERT INTO `error_questions` VALUES ('Admin', 26, '机器学习', '{\"Q\": \".以下哪种机器学习算法是基于树结构的？()\", \"A\": \".支持向量机(SVM)\", \"B\": \".随机森林\", \"C\": \".K-近邻算法\", \"D\": \".朴素贝叶斯\", \"answer\": \"B\", \"course\": \"机器学习\", \"mu\": 31.63192747483757, \"sigma\": 1.8546858037128076, \"leve\": 9, \"create_time\": 1716257421.0}', '智能分析', '{\"1\": \"知识点\"}', '2024-06-01 13:20:38');

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `Q` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `A` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `B` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `C` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `D` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `answer` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `course` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `mu` double NULL DEFAULT NULL,
  `sigma` double NULL DEFAULT NULL,
  `leve` int(0) NULL DEFAULT NULL,
  `create_time` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP(0),
  `knowledge` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 39 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of question
-- ----------------------------
INSERT INTO `question` VALUES (1, '.数据科学家可能会同时使用多个算法（模型）进行预测，并且最后把这些算法的结果集成起来进行最后的预测（集成学习）,以下对集成学习说法正确的是', '.单个模型之间有高相关性', '.单个模型之间有低相关性', '.在集成学习中使用“平均权重”而不是“投票”会比较好', '.单个模型都是用的一个算法', 'B', '机器学习', 34.72679253609176, 1.453404880764821, 6, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (2, '.在以下不同的场景中，使用的分析方法不正确的有（）', '.根据商家最近一年的经营及服务数据，用聚类算法判断出天猫商家在各自主营类目下所属的商家层级', '.根据商家近几年的成交数据，用聚类算法拟合出用户未来一个月可能的消费金额公式', '.用关联规则算法分析出购买了汽车坐垫的买家，是否适合推荐汽车脚垫', '.根据用户最近购买的商品信息，用决策树算法识别出淘宝买家可能是男还是女', 'B', '机器学习', 20, 8.334, 22, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (3, '.假设有6个二维数据点：D={(2,3),(5,7),(9,(4,5),(6,4),(7,2)},第一次切分时候，切分线为（)。', '.x=5', '.x=6', '.y=5', '.y=6', 'B', '机器学习', 15, 8.334, 28, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (4, '.LightGBM与XGBoost相比，主要的优势不包括（)', '.更快的训练速度', '.更低的内存消耗', '.更好的准确率', '.采用二阶泰勒展开加快收敛', 'D', '机器学习', 52.66150977605738, 6.189756292189565, 1, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (5, '.SVM算法的最小时间复杂度是O(n^2)。基于这一点，以下哪种规格的数据集并不适用于该算法？()', '.大数据集', '.小数据集', '.中数据集', '.不受数据集大小的影响', 'A', '机器学习', 5, 8.334, 29, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (6, '.一个正例（2,3),一个负例（0,-1),下面哪个是SVM超平面？()', '.2x+y-4=0', '.2y+X-5=0', '.x+2y-3=0', '.无法计算', 'C', '机器学习', 36.71384770619153, 2.038462298160634, 5, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (8, '.下列关于Kmeans聚类算法的说法错误的是（)。', '.对大数据集有较高的效率并且具有可伸缩性', '.是一种无监督学习方法', '.K值无法自动获取，初始聚类中心随机选择', '.初始聚类中心的选择对聚类结果影响不大', 'D', '深度学习', 29.2457725226483, 3.9164989764810825, 3, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (9, '.在以下不同的场景中，使用的分析方法不正确的有（）', '.根据用户的历史购买记录和浏览行为，用分类算法预测用户未来的消费类别', '.根据商家近几年的销售数据，用时间序列分析预测商家未来一年的销售趋势', '.用关联规则算法分析出购买了电脑的用户，是否适合推荐打印机', '.根据用户最近观看的电影类型，用聚类算法识别出用户的喜好类别', 'B', '机器学习', 23, 9.5, 27, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (10, '.在以下不同的场景中，使用的分析方法不正确的有（）', '.根据用户的历史搜索记录和点击行为，用协同过滤算法推荐用户可能感兴趣的新闻文章', '.根据社交媒体上的实时动态，用情感分析算法预测公众对于某一事件的情绪倾向', '.用关联规则算法分析出购买了运动鞋的用户，是否适合推荐运动服装', '.根据用户最近在线学习的课程内容，用决策树算法识别出用户的学习兴趣领域', 'A', '机器学习', 22, 8.7, 21, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (11, '.一个正例（3,2),一个负例（-1,-2),下面哪个是SVM超平面？()', '.3x+y-6=0', '.4y+X-7=0', '.2x+3y-5=0', '.无法计算', 'A', '机器学习', 35.321836245002984, 2.7655541734386615, 8, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (12, '.LightGBM与XGBoost相比，以下哪项不是其主要优势（)', '.更优的并行处理能力', '.更少的参数调整需求', '.支持类别不平衡的数据集', '.使用GPU进行模型训练', 'D', '机器学习', 42.74817322133547, 3.2042641063005894, 3, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (13, '.在使用随机森林时，以下哪项不是其主要优点（)', '.更快的训练速度', '.更好的内存使用效率', '.更适合处理大规模数据', '.无需进行特征工程', 'D', '机器学习', 52.44656184119641, 6.389441354908508, 2, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (14, '.LightGBM与XGBoost相比，以下哪项不是其主要优势（)', '.更快的训练速度', '.更高的模型精度', '.更好的处理缺失值', '.支持大规模数据集', 'B', '机器学习', 34.44075040616326, 1.7450750957586623, 7, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (16, '.一个正例（4,5),一个负例（1,-2),下面哪个是SVM超平面？()', '.3x+y-6=0', '.2y+x-8=0', '.x+3y-7=0', '.无法计算', 'B', '深度学习', 30.290386507260173, 4.133153541954755, 2, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (17, '.在以下不同的场景中，使用的分析方法不正确的有（)', '.根据用户的历史浏览记录和购买行为，用回归算法预测他们未来可能会购买的商品类别', '.根据商家近几年的销售数据，用聚类算法判断出哪些月份是销售淡季', '.用关联规则算法分析出购买了电脑的用户，是否适合推荐打印机', '.根据用户最近在社交平台上的活动信息，用决策树算法识别出可能对某款新产品感兴趣的用户群体', 'B', '深度学习', 28.450614916477157, 4.630198812332638, 5, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (18, '.在机器学习中，以下哪种方法可以用于处理高维数据？', '.主成分分析（PCA）', '.线性回归', '.决策树', '.神经网络', 'A', '深度学习', 23.931777352642754, 4.082892021890196, 7, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (19, '.下列关于决策树的说法错误的是（)。', '.是一种监督学习方法', '.可以处理数值型和类别型数据', '.容易理解，可解释性强', '.对缺失值不敏感', 'D', '深度学习', 42.08283252668985, 6.954689526783441, 1, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (20, '.假设有5个二维数据点：D={(1,2),(3,4),(5,6),(7,8),(9,10)},第一次切分时候，切分线为（)。', '.x=3', '.x=5', '.y=3', '.y=5', 'B', '深度学习', 25.199097988191347, 3.9967439310469595, 6, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (21, '.以下哪种排序算法在最坏情况下的时间复杂度为O(n^2)？()', '.快速排序', '.归并排序', '.选择排序', '.堆排序', 'C', '深度学习', 26.727355020903516, 3.6070463000483817, 4, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (22, '.在深度学习中，以下哪一项不是卷积神经网络（CNN）的主要特性？', '.可以处理时序数据', '.具有平移不变性', '.需要大量标记数据', '.可以有效降低参数数量和计算复杂度', 'C', '机器学习', 20, 8.334, 23, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (23, '.一个正例（1,2),一个负例（-1,0),下面哪个是SVM超平面？()', '.2x+y-3=0', '.2y+X-4=0', '.x+2y-1=0', '.无法计算', 'C', '机器学习', 40.25892937326523, 2.386292706908026, 4, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (24, '.假设有5个二维数据点：D={(2,3),(4,5),(6,7),(8,9),(10,11)},第一次切分时候，切分线为（)。', '.x=4', '.x=6', '.y=4', '.y=6', 'A', '机器学习', 28.127771415494717, 2.0534844227773803, 10, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (25, '.以下哪种排序算法的平均时间复杂度是O(n log n)？()', '.快速排序', '.冒泡排序', '.选择排序', '.插入排序', 'A', '机器学习', 22.871324896773817, 4.705054670468528, 12, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (26, '.以下哪种机器学习算法是基于树结构的？()', '.支持向量机(SVM)', '.随机森林', '.K-近邻算法', '.朴素贝叶斯', 'B', '机器学习', 31.526285394059713, 1.7505516925169844, 9, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (27, '在深度学习中，与卷积神经网络(CNN)相比，循环神经网络(RNN)不擅长处理的是（）', '.时间序列数据', '.图像识别', '.自然语言处理', '.音频分类', 'B', '机器学习', 21.147382058270416, 6.727892462242914, 16, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (28, '.在以下不同的场景中，使用的分析方法不正确的有（)', '.根据用户在社交平台上的互动数据，用决策树算法判断出用户可能的兴趣类别', '.根据网站用户的浏览记录，用关联规则算法预测用户未来可能点击的页面', '.用聚类算法分析出购买了特定商品的买家，是否适合推荐相关商品', '.根据用户最近一年的购物信息，用线性回归算法预测用户未来的消费趋势', 'B', '机器学习', 22.117118444522017, 5.348742283400675, 13, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (29, '.一监狱人脸识别准入系统用来识别待进入人员的身份，此系统一共包括识别4种不同的人员：狱警，小偷，送餐员，其他。下面哪种学习方法最适合此种应用需求：', '.回归问题', '.二分类问题', '.多分类问题', '.K-means', 'C', '机器学习', 25, 8.334, 17, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (30, '.一种用于识别不同种类的植物的系统，可以识别4种不同的植物：玫瑰，百合，郁金香，其他。下面哪种学习方法最适合此种应用需求：', '.回归问题', '.二分类问题', '.多分类问题', '.K-means', 'C', '机器学习', 25, 8.334, 18, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (31, '.以下哪种技术对于减少数据集的维度会更好', '.删除缺少值太多的列', '.删除数据差异较大的列', '.删除不同数据趋势的列', '.都不是', 'A', '机器学习', 20.925767182550977, 5.608896394664086, 15, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (32, '.以下哪种方法对于机器学习模型的过拟合有更好的抑制效果', '.增大训练数据量', '.减小模型复杂度', '.增大正则化参数', '.都不是', 'B', '机器学习', 24.542043726537514, 6.400537925894924, 14, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (33, '.将原始数据进行集成、变换、维度规约、数值规约是在以下哪个步骤的任务？', '.频繁模式挖掘', '.分类和预测', '.数据预处理', '.数据流挖掘', 'C', '机器学习', 20, 8.334, 24, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (34, '.在数据挖掘中，以下哪个步骤的任务是将原始数据进行集成、变换、维度规约、数值规约？', '.频繁模式挖掘', '.分类和预测', '.数据预处理', '.数据流挖掘', 'C', '机器学习', 20, 8.334, 25, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (35, '.下列不是SVM核函数的是（)', '.多项式核函数', '.逻辑核函数', '.径向基核函数', '.线性核函数', 'B', '机器学习', 25, 8.334, 19, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (36, '.在SVM中，下列哪项不是常见的核函数（）', '.线性核函数', '.多项式核函数', '.径向基核函数', '.高斯核函数', 'D', '机器学习', 25, 8.334, 20, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (37, '.在机器学习中，以下哪种方法可以用于处理多分类问题？', '.使用逻辑回归模型', '.使用支持向量机模型', '.使用决策树模型', '.使用神经网络模型', 'A', '机器学习', 20, 8.334, 26, '2024-05-21 10:10:21', NULL);
INSERT INTO `question` VALUES (38, '.在以下不同的场景中，使用的分析方法不正确的有（)', '.根据用户的网页浏览行为数据，用聚类算法对用户进行细分，以实现个性化推荐', '.根据历史天气数据和农作物产量记录，用关联规则算法预测未来一年的农作物产量', '.用决策树算法分析出购买特定健康食品的用户可能感兴趣的其他健康产品', '.根据用户过去一周的搜索关键词，用聚类算法预测用户未来可能的搜索兴趣', 'B', '机器学习', 29.80440322919629, 5.727830096570735, 11, '2024-05-28 19:53:48', NULL);

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `username` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nickname` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `age` int(0) NULL DEFAULT NULL,
  `class` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('Admin', 'e10adc3949ba59abbe56e057f20f883e', '小红', '女', 25, '3班');

-- ----------------------------
-- Table structure for student_answer_history
-- ----------------------------
DROP TABLE IF EXISTS `student_answer_history`;
CREATE TABLE `student_answer_history`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `username` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `history` json NULL,
  `create_time` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP(0),
  `course` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `accuracy` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `username`(`username`) USING BTREE,
  CONSTRAINT `student_answer_history_ibfk_1` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 171 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_answer_history
-- ----------------------------
INSERT INTO `student_answer_history` VALUES (145, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"4\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"23\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"B\"}, \"24\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}}', '2024-05-24 10:49:37', '机器学习', 0.5);
INSERT INTO `student_answer_history` VALUES (146, 'Admin', '{\"1\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"B\"}, \"13\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"26\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-05-24 15:12:12', '机器学习', 0.5);
INSERT INTO `student_answer_history` VALUES (147, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"B\"}, \"13\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"14\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}}', '2024-05-24 15:12:37', '机器学习', 0.5);
INSERT INTO `student_answer_history` VALUES (148, 'Admin', '{\"1\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"11\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"12\": {\"right\": true, \"answer\": \"D\", \"user_answer\": \"D\"}, \"13\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"23\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"B\"}, \"24\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"25\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}}', '2024-05-24 15:13:16', '机器学习', 0.5);
INSERT INTO `student_answer_history` VALUES (149, 'Admin', '{\"1\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"4\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"11\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"13\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"23\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"B\"}, \"24\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"25\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"26\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-05-24 15:13:53', '机器学习', 0.5);
INSERT INTO `student_answer_history` VALUES (150, 'Admin', '{\"8\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"16\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"18\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"20\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"21\": {\"right\": true, \"answer\": \"C\", \"user_answer\": \"C\"}}', '2024-05-24 15:14:18', '深度学习', 0.5);
INSERT INTO `student_answer_history` VALUES (151, 'Admin', '{\"8\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"16\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"17\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"18\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"19\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"20\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"21\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}}', '2024-05-24 15:14:50', '深度学习', 0.5);
INSERT INTO `student_answer_history` VALUES (152, 'Admin', '{\"8\": {\"right\": true, \"answer\": \"D\", \"user_answer\": \"D\"}, \"16\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"18\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"D\"}, \"20\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"21\": {\"right\": true, \"answer\": \"C\", \"user_answer\": \"C\"}}', '2024-05-24 15:15:30', '深度学习', 0.5);
INSERT INTO `student_answer_history` VALUES (153, 'Admin', '{\"8\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"16\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"17\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"19\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"21\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}}', '2024-05-24 15:15:53', '深度学习', 0.5);
INSERT INTO `student_answer_history` VALUES (154, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"6\": {\"right\": true, \"answer\": \"C\", \"user_answer\": \"C\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"14\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"23\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}}', '2024-05-24 19:34:49', '机器学习', 0.5);
INSERT INTO `student_answer_history` VALUES (155, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"4\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"6\": {\"right\": true, \"answer\": \"C\", \"user_answer\": \"C\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"13\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"C\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"23\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}}', '2024-05-27 00:46:07', '机器学习', 0.125);
INSERT INTO `student_answer_history` VALUES (156, 'Admin', '{\"8\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"16\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"17\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"18\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"19\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"20\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"21\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}}', '2024-05-27 00:49:47', '深度学习', 0);
INSERT INTO `student_answer_history` VALUES (157, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"6\": {\"right\": true, \"answer\": \"C\", \"user_answer\": \"C\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}}', '2024-05-27 10:19:09', '机器学习', 0.2);
INSERT INTO `student_answer_history` VALUES (158, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"B\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}, \"14\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-05-27 15:33:57', 'undefined', 0.25);
INSERT INTO `student_answer_history` VALUES (159, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}}', '2024-05-27 15:35:21', 'undefined', 0);
INSERT INTO `student_answer_history` VALUES (160, 'Admin', '{\"1\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}}', '2024-05-27 15:36:13', 'undefined', 0.5);
INSERT INTO `student_answer_history` VALUES (161, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"A\"}}', '2024-05-27 15:37:14', 'undefined', 0);
INSERT INTO `student_answer_history` VALUES (162, 'Admin', '{\"1\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"12\": {\"right\": false, \"answer\": \"D\", \"user_answer\": \"B\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"-1\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"-1\"}}', '2024-05-27 15:46:50', 'undefined', 0.2);
INSERT INTO `student_answer_history` VALUES (163, 'Admin', '{\"1\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"23\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"26\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-05-27 15:50:05', 'undefined', 0.4);
INSERT INTO `student_answer_history` VALUES (164, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"11\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"C\"}, \"14\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}}', '2024-05-27 15:53:32', '机器学习', 0.2);
INSERT INTO `student_answer_history` VALUES (165, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"B\"}, \"11\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"26\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-05-28 19:26:21', '机器学习', 0.4);
INSERT INTO `student_answer_history` VALUES (166, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"11\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"D\"}, \"26\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-05-28 19:52:16', '机器学习', 0.2);
INSERT INTO `student_answer_history` VALUES (167, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"11\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"24\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"26\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-05-29 23:17:50', '机器学习', 0.4);
INSERT INTO `student_answer_history` VALUES (168, 'Admin', '{\"1\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"11\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"24\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"C\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}}', '2024-05-30 22:37:08', '机器学习', 0);
INSERT INTO `student_answer_history` VALUES (169, 'Admin', '{\"6\": {\"right\": false, \"answer\": \"C\", \"user_answer\": \"A\"}, \"11\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"14\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"C\"}, \"24\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"26\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-06-03 18:37:17', '机器学习', 0.4);
INSERT INTO `student_answer_history` VALUES (170, 'Admin', '{\"11\": {\"right\": true, \"answer\": \"A\", \"user_answer\": \"A\"}, \"14\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}, \"24\": {\"right\": false, \"answer\": \"A\", \"user_answer\": \"B\"}, \"26\": {\"right\": false, \"answer\": \"B\", \"user_answer\": \"A\"}, \"38\": {\"right\": true, \"answer\": \"B\", \"user_answer\": \"B\"}}', '2024-06-04 10:53:58', '机器学习', 0.6);

-- ----------------------------
-- Table structure for student_skill
-- ----------------------------
DROP TABLE IF EXISTS `student_skill`;
CREATE TABLE `student_skill`  (
  `username` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `course` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mu` double NULL DEFAULT NULL,
  `sigma` double NULL DEFAULT NULL,
  PRIMARY KEY (`course`, `username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_skill
-- ----------------------------
INSERT INTO `student_skill` VALUES ('Admin', '机器学习', 30.883860661632603, 0.9111409238175983);
INSERT INTO `student_skill` VALUES ('Admin', '深度学习', 21.32083711763636, 2.034914513576511);

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `username` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nickname` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `age` int(0) NULL DEFAULT NULL,
  `class` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` int(0) NULL DEFAULT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES ('Admin', '827ccb0eea8a706c4c34a16891f84e7b', '特朗普', '男', 77, '空', 0);

SET FOREIGN_KEY_CHECKS = 1;
