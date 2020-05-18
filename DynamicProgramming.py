# 计算编辑距离
def edit_distance(s1, s2):
    print("---------------------------------------")
    print("s1的值:", s1)
    print("s2的值:", s2)
    # s1 长度m
    m = len(s1)
    # s2 长度n
    n = len(s2)
    # 如果m = 0，则至少还需要操作n次，即在s1中逐个添加s2的字符
    if m == 0:
        if n > 0:
            return n
        else:
            return 0
    # 如果n = 0，则至少还需要操作m次，即在s1中逐个删除字符
    # 如果m =0，n = 0，则不需要再操作
    if n == 0:
        if m > 0:
            return m
        else:
            return 0

    # s1和s2最后一个字符一样
    if s1[-1] == s2[-1]:
        return edit_distance(s1[:-1], s2[:-1])
    else:  # 最后一个字符不一样
        # 插入    删除      替换
        return 1 + min(edit_distance(s1, s2[:-1]), edit_distance(s1[:-1], s2), edit_distance(s1[:-1], s2[:-1]))


if __name__ == '__main__':
    string1 = "Sunday"
    string2 = "Saturday"
    distance = edit_distance(string1, string2)
    print("编辑距离：", distance)
