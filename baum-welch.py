import numpy
import logging

class HMM:
    def __init__(self,A,B,Pi):
        self.A=A
        self.B=B
        self.Pi=Pi

    #前向算法
    def forward(self,O):
        row=self.A.shape[0]
        col=len(O)
        alpha=numpy.zeros((row,col))
        #初值
        alpha[:,0]=self.Pi*self.B[:,O[0]]
        #递推
        for t in range(1,col):
            for i in range(row):
                alpha[i,t]=numpy.dot(alpha[:,t-1],self.A[:,i])*self.B[i,O[t]]
        #终止
        return alpha

    #后向算法
    def backward(self,O):
        row=self.A.shape[0]
        col=len(O)
        beta=numpy.zeros((row,col))
        #初值
        beta[:,-1:]=1
        #递推
        for t in reversed(range(col-1)):
            for i in range(row):
                beta[i,t]=numpy.sum(self.A[i,:]*self.B[:,O[t+1]]*beta[:,t+1])
        #终止
        return beta

    #前向-后向算法(Baum-Welch算法):由 EM算法 & HMM 结合形成
    def baum_welch(self,O,e=0.05):

        row=self.A.shape[0]
        col=len(O)

        done=False
        while not done:
            zeta=numpy.zeros((row,row,col-1))
            alpha=self.forward(O)
            beta=self.backward(O)
            #EM算法：由 E-步骤 和 M-步骤 组成
            #E-步骤：计算期望值zeta和gamma
            for t in range(col-1):
                #分母部分
                denominator=numpy.dot(numpy.dot(alpha[:,t],self.A)*self.B[:,O[t+1]],beta[:,t+1])
                for i in range(row):
                    #分子部分以及zeta的值
                    numerator=alpha[i,t]*self.A[i,:]*self.B[:,O[t+1]]*beta[:,t+1]
                    zeta[i,:,t]=numerator/denominator
            gamma=numpy.sum(zeta,axis=1)
            final_numerator=(alpha[:,col-1]*beta[:,col-1]).reshape(-1,1)
            final=final_numerator/numpy.sum(final_numerator)
            gamma=numpy.hstack((gamma,final))
            #M-步骤：重新估计参数Pi,A,B
            newPi=gamma[:,0]
            newA=numpy.sum(zeta,axis=2)/numpy.sum(gamma[:,:-1],axis=1)
            newB=numpy.copy(self.B)
            b_denominator=numpy.sum(gamma,axis=1)
            temp_matrix=numpy.zeros((1,len(O)))
            for k in range(self.B.shape[1]):
                for t in range(len(O)):
                    if O[t]==k:
                        temp_matrix[0][t]=1
                newB[:,k]=numpy.sum(gamma*temp_matrix,axis=1)/b_denominator
            #终止阀值
            if numpy.max(abs(self.Pi-newPi))<e and numpy.max(abs(self.A-newA))<e and numpy.max(abs(self.B-newB))<e:
                done=True
            self.A=newA
            self.B=newB
            self.Pi=newPi
        return self.A, self.B, self.Pi

#将字典转化为矩阵
def matrix(X,index1,index2):
    #初始化为0矩阵
    m = numpy.zeros((len(index1),len(index2)))
    for row in X:
        for col in X[row]:
            #转化
            m[index1.index(row)][index2.index(col)]=X[row][col]
    return m

def weather_data_gene(src_path):
    fp = open(src_path, encoding="utf8").read().split("\n")
    dataset = [line.split(",")[1:] for line in fp[1:] if len(line) > 0]
    h_data_set = set([line[-2] for line in dataset])
    h_data_len = len(h_data_set)
    h_data_dict = {tag: ind for ind,tag in enumerate(h_data_set)}
    logging.debug(h_data_dict)
    h_data = [h_data_dict[line[-2]] for line in dataset]
    # o_data = [[int(num) if num != "None" else 0 for num in line] for line in dataset]
    o_data = [int((int(line[1]) - 20) / 5 ) for line in dataset]
    o_data_len = max(o_data)
    logging.debug("data range: %d"%(o_data_len))

    A = numpy.zeros([len(h_data_set), len(h_data_set)])
    for i in range(len(h_data)-1):
        A[h_data[i]-1, h_data[i+1]-1] += 1
    A = normalize(A)
    B = numpy.zeros([len(h_data_set), o_data_len])
    Pi = numpy.zeros([1, h_data_len])
    for i in range(len(o_data)):
        B[h_data[i]-1, o_data[i]-1] += 1
        Pi[0, h_data[i]-1] += 1
    B = normalize(B)
    # B = numpy.transpose(B)
    Pi = normalize(Pi)


    return numpy.array([o_data]), A, B, Pi, h_data_dict, o_data_len, h_data_len

def normalize(Mat, theta=0.1):
    max = numpy.max(Mat)
    return (Mat+theta)/max

def predict(A, B, Pi, last_O):
    B_O = [num for num in B[:, last_O]]
    print(B_O)
    I_t = B_O.index(max(B_O))
    I_nt_list = [num for num in A[I_t]]
    print(I_nt_list)
    I_nt = I_nt_list.index(max(I_nt_list))
    B_nO = [num for num in B[I_nt, :]]
    print(B_nO)
    O_nt = B_nO.index(max(B_nO))
    print(O_nt)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

    #初始化,随机的给参数A,B,Pi赋值
    # A=matrix(A,status,status)
    # B=matrix(B,status,observations)
    # print(A)
    O, A, B, Pi = weather_data_gene("dataset/sitka_weather_2014.csv")
    # print(O)
    # print(A)
    # print(Pi)
    print(A.shape)
    print(B.shape)
    hmm = HMM(A,B,Pi)
    n_A, n_B, n_Pi = hmm.baum_welch(O[-64:-1])
    print(n_A.shape)
    print(n_B.shape)
    predict(n_A, n_B, n_Pi, O[-2])
