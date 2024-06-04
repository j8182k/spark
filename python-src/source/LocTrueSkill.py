from trueskill import rate, TrueSkill
import User
import Question


# 创建Rating()对象
def createRating(mu, sigma):
    env = TrueSkill(mu=mu, sigma=sigma, tau=10)
    return env.create_rating()


def createPlayers(dic):
    #     dic格式｛index:{name:'',mu:0.0,sigma:0.0},.....｝
    group = {}
    for i in range(len(dic)):
        play_dic = dic[i]
        play = createRating(play_dic['mu'], play_dic['sigma'])
        group[play_dic['name']] = play
    #   输出格式：  {用户名：Rating()对象,....}
    return group


# 根据能力和不确定度计算排名
def calculate_rank(player_rating):
    # player_rating格式｛index:{name:'',mu:0.0,sigma:0.0},.....｝
    player_rating = createPlayers(player_rating)
    # 转换成 {用户名：Rating()对象,....}
    rank = [(key, player_rating[key].mu - player_rating[key].sigma * 3) for key in player_rating]
    rank = sorted(rank, key=lambda x: -x[1])
    rank_dic = {}
    i = 0
    for item in rank:
        rank_dic[item[0]] = i + 1
        i += 1
    # 返回一个字典 {用户名：排名}
    return rank_dic


def upDate(user_rating, rank_dic):
    # 参数类型是字典 {用户1：Rating()对象,....}
    # rank为字典 {用户1:位次，用户2:位次，。。。}
    play_list = []
    rank_list = []
    for key in user_rating:
        # 放入玩家
        play_list.append((user_rating[key],))
        # 放入该玩家的名次
        rank_list.append(rank_dic[key])
    rs = rate(play_list, ranks=rank_list)
    k = 0
    for j in user_rating:
        user_rating[j] = rs[k][0]
        k += 1
    # 每个玩家的Rating()对象参数已更新
    return user_rating


def s_vs_q(student_name, question_id, right):
    question_id = int(question_id)
    question = Question.queryQuestionById(question_id)[question_id]
    # print(question,question_id)
    course = question['course']
    # 获取学生能力与不确定度
    stu_skill = User.getSkills(student_name, course)

    # print("学生更新前的参数")
    # print(stu_skill['mu'], stu_skill['sigma'])

    player_dic = {0: {'name': student_name, 'mu': stu_skill['mu'], 'sigma': stu_skill['sigma']},
                  1: {'name': question_id, 'mu': question['mu'], 'sigma': question['sigma']}}
    # 创建用于更新参数的对象
    ratings = createPlayers(player_dic)
    rank_dic = {student_name: 0, question_id: 0}
    if right:
        rank_dic[student_name] = 1
        rank_dic[question_id] = 2
    else:
        rank_dic[student_name] = 2
        rank_dic[question_id] = 1
    user_rating = upDate(ratings, rank_dic)
    student_mu = user_rating[student_name].mu
    student_sigma = user_rating[student_name].sigma
    q_mu = user_rating[question_id].mu
    q_sigma = user_rating[question_id].sigma
    # 学生能力更新
    User.setSkill(student_name, student_mu, student_sigma, course)
    # 题目难度更新
    Question.updateQmu(question_id, q_mu, q_sigma)
    # print('学生更新后的参数')
    # print(student_mu, student_sigma)


if __name__ == '__main__':
    s_vs_q("Admin", 1, False)







