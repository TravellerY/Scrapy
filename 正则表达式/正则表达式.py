# coding=utf-8
import re


def metacharacters1():
    """
    数字元字符 \d
    :return:
    """
    a = 'C0C++2JAVA9PYTHON7JAVASCRIPT5'
    r = re.findall(r"\d", a)
    print(r)


def metacharacters2():
    """
    字符集
    :return:
    """
    a = r'abc,acc,adc,abc,aec,afc,ahc'
    # 匹配中间包含c f的字段
    c = re.findall(r"a[cf]c", a)
    # 匹配 c d e f 的字段
    d = re.findall(r"a[c-f]c", a)
    # 匹配中间不是c f 的字段
    e = re.findall(r"a[^cf]c", a)
    print(c)
    print(d)
    print(e)


def metacharacters3():
    """
    概括字符集:
    数字字符 \d \D
    单词字符 \w  \W
    空白字符 \s  \S
    :return:
    """
    a = 'python 11\tjava\n$php\r'
    r = re.findall(r"\s", a)
    print(r)


def metacharacters4():
    """
    数量词
    :return:
    """
    a = 'python 11\tjava\n$php\r'
    # 匹配英文字符3-6个
    r = re.findall(r"[a-z]{3,6}", a)
    print(r)


def metacharacters5():
    """
    贪婪与非贪婪
    :return:
    """
    a = "python 1111java322323$php123456'"
    # 在数量词后面加上？代表非贪婪
    r = re.findall(r"[a-z]{3,6}?", a)
    print(r)


def metacharacters6():
    """
    匹配0次或者无限多次
    *  匹配0次或者无限多次
    +  匹配1次或者无限多次
    ?  匹配0次或者1次
    :return:
    """
    a = "pytho0python1pythonn2"
    # * 匹配0次或者无限多次
    c = re.findall("python*", a)
    print(c)
    # + 匹配1次或者无限多次
    d = re.findall("python+", a)
    print(d)
    # ? 匹配0次或者1次
    e = re.findall("python?", a)
    print(e)


def metacharacters7():
    """
    边界匹配符
    :return:
    """
    qq = '1000000001'
    r = re.findall('^\d{8,10}$', qq)
    # 从开始的第一位数字开始匹配
    a = re.findall('^000', qq)
    # 从结束的最后一位进行匹配
    b = re.findall('000&', qq)
    print(r)
    print(a)
    print(b)


def metacharacters8():
    """
    组
    :return:
    """
    a = 'PythonPythonPythonPythonPythonPythonPython'
    # 括号中代表的是一组字符，后面的中括号的数字代表之前的一组字符需包含的数量
    r = re.findall('(Python){2}', a)
    print(r)


def metacharacters9():
    """
    匹配模式参数
    :return:
    """
    a = 'PythonC#\nJavaPHP'
    # re.I代表忽略大小写去匹配， re.S代表改变元字符的匹配规则 多个匹配模式需用 | 分开
    r = re.findall('c#.{1}', a, re.I | re.S)
    print(r)


def metacharacters10():
    """
    re.sub正则替换
    :return:
    """
    a = 'PythonC#PHPC#JavaC#'
    # pattern代表原字符串中需替换的字符  repl代表替换后的字符   count代表替换多少次，0代表无限次
    # re.I代表匹配模式参数
    r = re.sub('c#', '123', a, 0, re.I)
    print(r)


def metacharacters11():
    """
    把函数作为参数传递
    :return:
    """
    s = 'A8C37V8Q12'

    def convert(value):
        matched = value.group()
        if int(matched) > 5:
            return '9'
        else:
            return '0'

    r = re.sub('\d', convert, s)
    print(r)


def metacharacters12():
    """
    match函数
    :return:
    """
    s = 'A8C37V8Q12'
    # match从字符串的首个字符开始匹配如果没有匹配当相应结果，会返回None
    r = re.match('\d', s)
    print(r)


def metacharacters13():
    """
    search函数
    :return:
    """
    s = 'A8C37V8Q12'
    # 将搜索整个字符串，直到找到相应结果并返回，返回结果是对象
    r = re.search('\d', s)
    print(r)
    print(r.group())


def metacharacters14():
    """
    group分组
    :return:
    """
    s = 'life is short,i use python,i love python'
    r = re.search('life(.*)python(.*)python', s)
    # 返回的group可写多个分组
    print(r.group(0, 1, 2))
    print(r.group(0))
    print(r.group(1))
    print(r.group(2))
    # 不返回完整的直返会中间的
    print(r.groups())


if __name__ == '__main__':
    metacharacters6()
