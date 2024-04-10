import hashlib


def get_md5(data):
    """
    md5转换
    :param data:
    :return:
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()
