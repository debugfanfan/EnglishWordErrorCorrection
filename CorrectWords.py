import re, collections


# 获取所有单词并转为小写形式,text示例："The Project Gutenberg EBook of The Adventures of Sherlock Holmes\nby Sir Arthur Conan Doyle"
def tokens(text):
    return re.findall("[a-z]+", text.lower())


# 打开语料库文件
with open('big.txt', 'r') as f:
    words = tokens(f.read())
# 统计语料库中每个单词的个数
word_counts = collections.Counter(words)


def correct_text_generic(text):
    """
    在匹配中纠正所有拼写错误的单词
    """
    return re.sub('[a-zA-Z]+', correct_match, text)


def correct_match(match):
    """
    替换的回调函数
    """

    word = match.group()

    def case_of(text):
        """
            返回小写
        """
        return (str.upper if text.isupper() else
                str.lower if text.islower() else
                str.title if text.istitle() else
                str)

    return case_of(word)(correct(word.lower()))


def correct(word):
    """
        获得输入单词的最佳正确拼写
    """
    # 1.是否在语料库中出现

    # 2.单词的优先顺序：编辑距离为0的单词（即该单词本身） > 编辑距离为1的单词 > 编辑距离为2的单词

    # 3.在语料库中的出现次数

    candidates = (known(edits0(word)) or
                  known(edits1(word)) or
                  known(edits2(word)) or
                  {word})
    return max(candidates, key=word_counts.get)


def known(words):
    """
        判断words中的每一个单词是否在语料库中出现，若出现就返回此单词
    """
    return {w for w in words if w in word_counts}


def edits0(word):
    """
        返回跟输入单词是0距离的单词,也就是自己
    """
    return {word}


def edits1(word):
    """
        返回跟输入单词是1距离的单词
    """
    # 26个英文字母   ord():获取'a'的码  chr():通过码还原对应的字符
    alphabet = ''.join([chr(ord('a') + i) for i in range(26)])

    def splits(word):
        """
            分割单词    以cat为例：  ("","cat")  ("c","at")  ("ca","")   ("cat","")
        """
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

    # 分割好的单词
    pairs = splits(word)

    # 删除某个字符
    deletes = [a + b[1:] for (a, b) in pairs if b]
    # 两个字符换位置
    transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
    # 替换某个字符
    replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
    # 插入某个字符
    inserts = [a + c + b for (a, b) in pairs for c in alphabet]
    # 返回集合
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """
        返回跟输入单词是2距离的单词
        寻找跟word编辑距离为1的单词的编辑距离为1的单词就是编辑距离为2的单词
    """

    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}


if __name__ == '__main__':
    original_word = 'fianlly'
    correct_word = correct_text_generic(original_word)
    print('Original word:%s\nCorrect word:%s' % (original_word, correct_word))
