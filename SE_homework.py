# --//                            _ooOoo_
# --//                           o8888888o
# --//                           88" . "88
# --//                           (| -_- |)
# --//                            O\ = /O
# --//                        ____/`---'\____
# --//                      .   ' \\| |// `.
# --//                       / \\||| : |||// \
# --//                     / _||||| -:- |||||- \
# --//                       | | \\\ - /// | |
# --//                     | \_| ''\---/'' | |
# --//                      \ .-\__ `-` ___/-. /
# --//                   ___`. .' /--.--\ `. . __
# --//                ."" '< `.___\_<|>_/___.' >'"".
# --//               | | : `- \`.;`\ _ /`;.`/ - ` : | |
# --//                 \ \ `-. \_ __\ /__ _/ .-` / /
# --//         ======`-.____`-.___\_____/___.-`____.-'======
# --//                            `=---='
# --//
# --//         .............................................
# --//                  佛祖保佑             永无BUG

# 登录日志
class LogForm(object):

    def __init__(self):
        self.LogInfo = None

    def LoadLog(self, MaxLength):
        pass

    def PushLog(self, NewLogInfo):
        pass

class User(object):

    # 用户基础信息
    def __init__(self):
        self.Userinfos = None
        self.ReadForm = ReaderLog()

    # 用户登录
    def UserLogin(self, UserID, base64code):
        LogForm.PushLog()
        pass

    # 用户注册
    def UserRegster(self, UserID, base64code):
        pass

    # 用户找回密码
    def FindLostKey(self, UserID, ConfirmParams):
        pass

    # 设置阅读模式
    def SetReadingMode(self, UserID, ArticleID, ReadingModeParams):
        self.ReadForm.SetUserReadMode()
        pass


class Article(object):

    # 文章基础信息
    def __init__(self):
        self.ArticleInfo = None

    # 获取文本数据
    def GetPlantText(self):
        pass

    # plant text/pdf 转 标准格式
    def Text2Standard(self):
        pass

    # 载入
    def LoadFile(self, FilePath):
        pass

    # 保存
    def SaveFile(self, FilePath):
        pass


class Notes(object):

    def __init__(self):
        self.NotesInfo = None

    # 构建注释文件
    def BuildNoteFile(self, SavePath, BuildParams):
        pass

    # 载入注释文件
    def LoadNoteFiles(self, LoadPath):
        pass

    # 存储注释文件
    def SaveNoteFiles(self, SavePath):
        pass

    # 追加注释文件
    def AppendNote(self, SavePath, NewNote):
        pass


class ReaderLog(LogForm):

    def __init__(self):
        super(LogForm, ReaderLog).__init__()

    # 更新最后一次阅读模式
    def RefreshLastPatten(self, UserID):
        pass

    # 记录阅读操作
    def RecordUserOprate(self, UserID):
        pass

    # 保存阅读模式
    def SaveReadMode(self, UseID):
        pass

    # 设置阅读模式
    def SetUserReadMode(self, UseID):
        pass


class Words(object):

    # 单词数据
    def __init__(self):
        self.WordInfo = None
        self.UserInfo = None

    def FindWord(self):
        pass

    def LoadWord(self):
        pass

    def SaveWord(self):
        pass

    # 词频统计
    def WordFreq(self):
        pass

    # 单词卡
    def GeneWordCard(self):
        pass

    # 单词测验
    def WordTest(self):
        pass

class Reader(object):

    # 阅读器基本设定
    def __init__(self):
        self.ReadParams = None
        self.Article = Article()
        self.Note = Notes()
        self.ReadLog = ReaderLog()
        self.Words = Words()

    # 载入上次阅读记录
    def LoadLastRead(self):
        self.ReadLog.LoadLog()
        self.Article.LoadFile()
        self.Note.LoadNoteFiles()
        pass

    # 载入阅读模式
    def LoadReadMode(self, UserID):
        self.ReadLog.RefreshLastPatten()
        pass

    # 记录注释
    def WriteDownNote(self, UserID):
        pass

    # 单词及文本查询翻译
    def TextTrans(self):
        pass

    # 生词记录
    def RecordNewWords(self):
        self.Words.SaveWord()
        pass


class EvaluateSystem(object):

    def __init__(self):
        self.EvalInfo = None
        self.UserInfo = None
        self.Article = Article()

    def Eval(self, SrcPath, SavePath):
        self.Article.LoadFile(SrcPath)
        self.SaveEval(SavePath)
        pass

    def SaveEval(self, SavePath):
        pass


class TextAnalysisSystem(object):

    def __init__(self):
        self.UserInfo = None
        self.Note = Notes()
        self.Article = Article()
        self.Word = Words()

    # 翻译模块
    def TranslateBlocks(self):
        pass

    # 注释处理
    def NoteDataOperate(self, NoteText, NotePos):
        self.Note.AppendNote(self.UserInfo, NoteText, NotePos)
        pass

    # 生词处理
    def NewWordOperate(self):
        self.Word.WordFreq()
        self.Word.SaveWord()
        pass