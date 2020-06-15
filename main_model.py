import re
import logging
from hmm_model import *
import matplotlib.pyplot as plt

class HMM(object):

    # 模型初始化参数
    def __init__(self, Pi=None, A=None, B=None, Load_model=None):
        self.Pi = Pi
        self.A = A
        self.B = B
        if Load_model is not None:
            self.Pi, self.A, self.B = self.Load(Load_model)

    def ForwardAlgo(A, B, Pi, O):
        N = A.shape[0]  # 数组A的行数
        M = B.shape[1]  # 数组A的列数
        H = O.shape[1]  # 数组O的列数

        sum_alpha_1 = np.zeros((M, N))
        alpha = np.zeros((N, H))
        r = np.zeros((1, N))
        alpha_1 = np.multiply(Pi[0, :], B[:, O[0, 0] - 1])

        alpha[:, 0] = np.array(alpha_1).reshape(1,
                                                N)  # alpha_1是一维数组，在使用np.multiply的时候需要升级到二维数组。#错误是IndexError: too many indices for array

        for h in range(1, H):
            for i in range(N):
                for j in range(M):
                    sum_alpha_1[j, i] = alpha[i, h - 1] * B[i, j]
                r = sum_alpha_1.sum(0).reshape(1, N)  # 同理，将数组升级为二维数组
                alpha[i, h] = r[0, i] * B[i, O[0, h] - 1]
            # print("alpha矩阵: \n %r" % alpha)
        p = alpha.sum(0).reshape(1, H)
        P = p[0, H - 1]
        # print("观测概率: \n %r" % P)
        # return alpha
        return alpha, P

    def BackwardAlgo(A, B, Pi, O):
        N = A.shape[0]  # 数组A的行数
        M = A.shape[1]  # 数组A的列数
        H = O.shape[1]  # 数组O的列数

        # beta = np.zeros((N,H))
        sum_beta = np.zeros((1, N))
        beta = np.zeros((N, H))
        beta[:, H - 1] = 1
        p_beta = np.zeros((1, N))

        for h in range(H - 1, 0, -1):
            for i in range(N):
                for j in range(M):
                    sum_beta[0, j] = A[i, j] * B[j, O[0, h] - 1] * beta[j, h]
                beta[i, h - 1] = sum_beta.sum(1)
        # print("beta矩阵: \n %r" % beta)
        for i in range(N):
            p_beta[0, i] = Pi[0, i] * B[i, O[0, 0] - 1] * beta[i, 0]
        p = p_beta.sum(1).reshape(1, 1)
        # print("观测概率: \n %r" % p[0,0])
        return beta, p[0, 0]

    def FBAlgoAppli(A, B, Pi, O, I):
        # 计算在观测序列和模型参数确定的情况下，某一个隐含状态对应相应的观测状态的概率
        # 例题参考李航《统计学习方法》P189习题10.2
        # 输入格式：
        # I为二维数组，存放所求概率P(it = qi,O|lambda)中it和qi的角标t和i，即P=[t,i]
        alpha, p1 = ForwardAlgo(A, B, Pi, O)
        beta, p2 = BackwardAlgo(A, B, Pi, O)
        p = alpha[I[0, 1] - 1, I[0, 0] - 1] * beta[I[0, 1] - 1, I[0, 0] - 1] / p1
        return p

    def GetGamma(A, B, Pi, O):
        N = A.shape[0]  # 数组A的行数
        H = O.shape[1]  # 数组O的列数
        Gamma = np.zeros((N, H))
        alpha, p1 = ForwardAlgo(A, B, Pi, O)
        beta, p2 = BackwardAlgo(A, B, Pi, O)
        for h in range(H):
            for i in range(N):
                Gamma[i, h] = alpha[i, h] * beta[i, h] / p1
        return Gamma

    def GetXi(A, B, Pi, O):
        N = A.shape[0]  # 数组A的行数
        M = A.shape[1]  # 数组A的列数
        H = O.shape[1]  # 数组O的列数
        Xi = np.zeros((H - 1, N, M))
        alpha, p1 = ForwardAlgo(A, B, Pi, O)
        beta, p2 = BackwardAlgo(A, B, Pi, O)
        for h in range(H - 1):
            for i in range(N):
                for j in range(M):
                    Xi[h, i, j] = alpha[i, h] * A[i, j] * B[j, O[0, h + 1] - 1] * beta[j, h + 1] / p1
        # print("Xi矩阵: \n %r" % Xi)
        return Xi

    def BaumWelchAlgo(A, B, Pi, O):
        N = A.shape[0]  # 数组A的行数
        M = A.shape[1]  # 数组A的列数
        Y = B.shape[1]  # 数组B的列数
        H = O.shape[1]  # 数组O的列数
        c = 0
        Gamma = GetGamma(A, B, Pi, O)
        Xi = GetXi(A, B, Pi, O)
        Xi_1 = Xi.sum(0)
        a = np.zeros((N, M))
        b = np.zeros((M, Y))
        pi = np.zeros((1, N))
        a_1 = np.subtract(Gamma.sum(1), Gamma[:, H - 1]).reshape(1, N)
        for i in range(N):
            for j in range(M):
                a[i, j] = Xi_1[i, j] / a_1[0, i]
        # print(a)
        for y in range(Y):
            for j in range(M):
                for h in range(H):
                    if O[0, h] - 1 == y:
                        c = c + Gamma[j, h]
                gamma = Gamma.sum(1).reshape(1, N)
                b[j, y] = c / gamma[0, j]
                c = 0
        # print(b)
        for i in range(N):
            pi[0, i] = Gamma[i, 0]
        # print(pi)
        return a, b, pi

    def BaumWelchAlgo_n(A, B, Pi, O, n):  # 计算迭代次数为n的BaumWelch算法
        for i in range(n):
            A, B, Pi = BaumWelchAlgo(A, B, Pi, O)
        return A, B, Pi

    def viterbi(A, B, Pi, O):
        N = A.shape[0]  # 数组A的行数
        M = A.shape[1]  # 数组A的列数
        H = O.shape[1]  # 数组O的列数
        Delta = np.zeros((M, H))
        Psi = np.zeros((M, H))
        Delta_1 = np.zeros((N, 1))
        I = np.zeros((1, H))

        for i in range(N):
            Delta[i, 0] = Pi[0, i] * B[i, O[0, 0] - 1]

        for h in range(1, H):
            for j in range(M):
                for i in range(N):
                    Delta_1[i, 0] = Delta[i, h - 1] * A[i, j] * B[j, O[0, h] - 1]
                Delta[j, h] = np.amax(Delta_1)
                Psi[j, h] = np.argmax(Delta_1) + 1
        print("Delta矩阵: \n %r" % Delta)
        print("Psi矩阵: \n %r" % Psi)
        P_best = np.amax(Delta[:, H - 1])
        psi = np.argmax(Delta[:, H - 1])
        I[0, H - 1] = psi + 1
        for h in range(H - 1, 0, -1):
            buf_t = int(I[0, h] - 1)
            # print(buf_t)
            buf = Psi[buf_t, h]
            I[0, h - 1] = buf
        print("最优路径概率: \n %r" % P_best)
        print("最优路径: \n %r" % I)

    # 模型学习参数
    # def Learning(self, observe_data, hidden_data, observe_data_type, hidden_data_type, seq_len=16):
    def Learning(self, O, A, B, Pi, h_dict, epochs):

        # data_list_len = len(observe_data) // seq_len
        # ob_data = np.reshape(observe_data[:seq_len*data_list_len], [data_list_len, seq_len])    # O: T x 数据数量 （T = sequence length）
        # hi_data = np.reshape(hidden_data[:seq_len*data_list_len], [data_list_len, seq_len])     # I
        # self.Pi = np.random.rand(1, hidden_data_type)   # 1 x N
        # self.A = np.random.rand(hidden_data_type, hidden_data_type)    # N x N
        # self.B = np.random.rand(hidden_data_type, observe_data_type)    # N x M

        self.A, self.B, self.Pi = BaumWelchAlgo_n(A, B, Pi, O, epochs)   # EM算法对模型参数优化

        for ind, hi in enumerate(self.A):
            print(ind,end="\t")
            for num in hi:
                print("%.2f"%(num),end="\t")
            print()
        # for tag in h_dict.keys():
        #     print("{:>10}".format(tag), end="\t")
        # print()
        for ind, hi in enumerate(self.B):
            print(ind,end="\t")
            for num in hi:
                print("{:>10}".format("%.2f"%(num)),end="\t")
            print()
        return self.A, self.B, self.Pi

    def predict(self, last_O):

        B_O = [num for num in self.B[last_O, :]]
        # print(B_O)
        I_t = B_O.index(max(B_O))
        I_nt_list = [num for num in self.A[I_t]]
        # print(I_nt_list)
        I_nt = I_nt_list.index(max(I_nt_list))
        B_nO = [num for num in self.B[:, I_nt]]
        # print(B_nO)
        O_nt = B_nO.index(max(B_nO))
        # print(last_O, O_nt)
        return O_nt

def weather_data_gene(src_text=None, src_path=None):
    if src_text is not None:
        fp = src_text.split("\n")
    else:
        fp = open(src_path, encoding="utf8").read().split("\n")
    dataset = [line.split(",")[1:] for line in fp[1:] if len(line) > 0]
    h_data_set = set([line[-1] for line in dataset])
    h_data_len = len(h_data_set)
    h_data_dict = {tag: ind for ind,tag in enumerate(h_data_set)}
    logging.debug(h_data_dict)
    h_data = [h_data_dict[line[-1]] for line in dataset]
    o_data = [int((int(line[1]) - 20) / 5 ) for line in dataset]
    o_data_len = max(o_data) + 2
    logging.debug("data range: %d"%(o_data_len))

    A = np.zeros([len(h_data_set), len(h_data_set)])
    for i in range(len(h_data)-1):
        A[h_data[i]-1, h_data[i+1]-1] += 1
    A = normalize(A)
    B = np.zeros([len(h_data_set), o_data_len])
    Pi = np.zeros([1, h_data_len])
    for i in range(len(o_data)):
        B[h_data[i]-1, o_data[i]-1] += 1
        Pi[0, h_data[i]-1] += 1
    B = normalize(B)
    # B = numpy.transpose(B)
    Pi = normalize(Pi)


    return np.array([o_data]), A, B, Pi, h_data_dict, o_data_len, h_data_len


def normalize(Mat, theta=0.1):
    max = np.max(Mat)
    return (Mat+theta)/max


def predict(A, B, Pi, last_O):
    B_O = [num for num in B[last_O, :]]
    # print(B_O)
    I_t = B_O.index(max(B_O))
    I_nt_list = [num for num in A[I_t]]
    # print(I_nt_list)
    I_nt = I_nt_list.index(max(I_nt_list))
    B_nO = [num for num in B[:, I_nt]]
    # print(B_nO)
    O_nt = B_nO.index(max(B_nO))
    # print(last_O, O_nt)
    return O_nt

def find_map(new, src, length):
    map_list = [0] * 9
    for i in range(length):
        counter_buf = 0
        for j in range(length):
            counter = 0
            for k in range(len(src)):
                if(new[k] == i and src[k] == j and j not in map_list):
                    counter += 1
            if counter > counter_buf:
                map_list[i] = j
                counter_buf = counter
    print(map_list)
    return [map_list[i] for i in new]

def plot_line(A, B, Pi, O, epoch):
    pred_O_list = [O[0]]
    for i in range(len(O)-1):
        pred_O = predict(A, B, Pi, O[i])
        pred_O_list.append(pred_O)

    pred_O_list = find_map(pred_O_list, O, 9)
    fig = plt.figure(dpi=128, figsize=(10, 6))

    plot1 = plt.plot([i for i in range(len(O))], pred_O_list, c='red', alpha=0.5)  # alpha指定颜色透明度
    plot2 = plt.plot([i for i in range(len(O))], O, c='blue', alpha=0.5)  # 注意dates和highs 以及lows是匹配对应的
    plt.fill_between([i for i in range(len(O))], pred_O_list, O, facecolor='blue', alpha=0.1)  # facecolor指定了区域的颜色

    # 设置图形格式
    plt.title("Predict Daily Weather, 2014", fontsize=24)
    plt.xlabel('', fontsize=14)
    fig.autofmt_xdate()  # 让x轴标签斜着打印避免拥挤
    plt.ylabel('Weather', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)

    plt.legend()
    plt.savefig(str(epoch) + ".png")

def main():
    O, A, B, Pi, h_dict, o_len, h_len = weather_data_gene("dataset/sitka_weather_2014.csv")
    epoch = 64
    print(O.shape)
    print(A.shape)
    print(B.shape)
    print(Pi.shape)
    model2 = HMM()
    n_A, n_B, n_Pi = model2.Learning(O, A, B, Pi, h_dict, epoch)
    print_alg(n_A, n_B)
    plot_line(A, B, Pi, O[0], epoch)
    # print(O.shape)
    # print(A.shape)
    # print(B.shape)
    # print(Pi.shape)
    # print_alg(A, B)
    # pred_o = np.array([O[0, 40:56]]).T
    # get_pred = model.predict(O.T)
    # print(get_pred)

def print_alg(A, B):
    for ind, hi in enumerate(A):
        print(ind, end="\t")
        for num in hi:
            print("%.2f" % (num), end="\t")
        print()
    # for tag in h_dict.keys():
    #     print("{:>10}".format(tag), end="\t")
    # print()
    for ind, hi in enumerate(B):
        print(ind, end="\t")
        for num in hi:
            print("{:>10}".format("%.2f" % (num)), end="\t")
        print()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    # observe_src, hidden_src, observe_data, hidden_data, observe_data_len\
    #     = RMRB_data_clean("dataset/RMRB-1998.txt")
    # observe_data, hidden_data, observe_data_len, hidden_data_len \
    #     = weather_data_gene("dataset/sitka_weather_2014.csv")
    # SEQ_LEN = 16
    # # logging.debug(list(observe_src[:SEQ_LEN]))
    # logging.debug(observe_data[:SEQ_LEN])
    # # logging.debug(list(hidden_src[:SEQ_LEN]))
    # logging.debug(hidden_data[:SEQ_LEN])
    # logging.debug("total observe data set scope: %d"%observe_data_len)
    # O, A, B, Pi, h_dict = weather_data_gene("dataset/sitka_weather_2014.csv")
    # print(np.shape(Pi))
    # model = HMM()
    # model.Learning(observe_data, hidden_data, observe_data_len, hidden_data_len, SEQ_LEN)
    # model.Learning(O, A, B, Pi, h_dict)
    main()