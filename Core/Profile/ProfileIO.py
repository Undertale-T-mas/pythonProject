import _io
import json
import os.path
from typing import *

__valMem__: Dict[str, Any] = dict()
__memFileSeek__: Set[str] = set()


def __memFileAnalyze__(file: BinaryIO) -> dict:
    content = file.read()
    x = len(content)
    if x == 0:
        return dict()
    real = bytearray(x)
    for i in range(x):
        real[x - i - 1] = content[i] ^ 101
    dat = real.decode()
    objs = dat.split(';')
    result = dict()
    for obj in objs:
        tup = obj.split(':')
        result[tup[0]] = tup[1]
    return result


def __memBufferFetch__(path: str):
    if path in __memFileSeek__:
        return
    __memFileSeek__.add(path)
    path = 'data\\' + path
    if not os.path.exists(path):
        # create dir
        folder = path.split('\\')
        cur = ''
        for i in range(len(folder) - 1):
            cur += folder[i] + '\\'
            if not os.path.exists(cur):
                os.mkdir(cur)

        file = open(path, 'w')
        file.close()

    file = open(path, 'rb')
    result = __memFileAnalyze__(file)
    for key in result:
        __valMem__[key] = result[key]
    file.close()


def __memBufferFetchAll__():
    raise NotImplementedError()


def __memPushBuffer__():
    dir_dicts: Dict[str, Dict[str, Any]] = dict()
    for key in __valMem__:
        root = key.split('.', 1)[0]
        if root not in dir_dicts.keys():
            dir_dicts[root] = dict()
        dir_dicts[root][key] = __valMem__[key]
    for d in dir_dicts:
        file = open('data\\' + d, 'wb')
        content = ''
        cur_d = dir_dicts[d]
        for obj in cur_d:
            content += obj + ':' + str(cur_d[obj]) + ';'
        content = content.removesuffix(';')
        source = content.encode()
        n = len(source)
        arr = bytearray(n)
        for i in range(n):
            arr[i] = source[n - i - 1] ^ 101
        file.write(arr)
        file.close()
    print('Game Saved!')


def __memPathAnalyze__(path: str) -> Tuple[str, str]:
    res = path.split('.', 1)
    if len(res) != 2:
        raise Exception()
    return res[0], res[1]


def __typGetVal__(inp):
    if not isinstance(inp, str):
        return inp
    sg = 1
    if inp[0] == '-':
        sg = -1
        inp = inp[1:]
    if str.isdigit(inp):
        return int(inp) * sg
    try:
        return float(inp) * sg
    except ValueError:
        return inp


class ProfileIO:
    @staticmethod
    def get(path_with_obj: str):
        if path_with_obj not in __valMem__:
            path, obj = __memPathAnalyze__(path_with_obj)
            __memBufferFetch__(path)
            if path_with_obj not in __valMem__:
                return None
        res = __valMem__[path_with_obj]

        return __typGetVal__(res)

    @staticmethod
    def set(path_with_obj: str, val: Any):
        __valMem__[path_with_obj] = val

    @staticmethod
    def save():
        __memPushBuffer__()

    @staticmethod
    def load():
        __memBufferFetchAll__()
