import _io
import copy
import json
import os.path
from typing import *

__valMemOld__: Dict[str, Any] | None = None
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
    __fileChanged__: set[str] = set()
    if __valMemOld__ is None:
        for key in __valMem__:
            root = key.split('.', 1)[0]
            if root not in dir_dicts.keys():
                dir_dicts[root] = dict()
                __fileChanged__.add(root)
            dir_dicts[root][key] = __valMem__[key]
    else:
        for key in __valMem__:
            root = key.split('.', 1)[0]

            if root not in __fileChanged__:
                if key not in __valMemOld__:
                    __fileChanged__.add(root)
                elif __valMem__[key] != __valMemOld__[key]:
                    __fileChanged__.add(root)
            if root not in dir_dicts.keys():
                dir_dicts[root] = dict()
            dir_dicts[root][key] = __valMem__[key]

    for d in dir_dicts:
        if d not in __fileChanged__:
            continue
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


def __memStoreBuffer__():
    global __valMem__, __valMemOld__
    __valMemOld__ = copy.deepcopy(__valMem__)


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
        if inp == 'True':
            return True
        elif inp == 'False':
            return False
        return inp


def __restoreOld__():
    global __valMem__
    if __valMemOld__ is None:
        return
    __valMem__ = copy.deepcopy(__valMemOld__)


class ProfileIO:
    @staticmethod
    def restore_old():
        __restoreOld__()

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
        ProfileIO.store()

    @staticmethod
    def store():
        __memStoreBuffer__()

    @staticmethod
    def load():
        __memBufferFetchAll__()
