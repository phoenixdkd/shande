# coding=utf-8
class PinYin():
    def __init__(self, data_path='.Mandarin.dat'):
        self.dict = {}
        for line in open(data_path):
            k, v = line.split('\t')
            self.dict[k] = v
        self.splitter = ''

    def get_py(self, chars=u'你好'):
        result = []
        for char in chars:
            key = "%x" % ord(char)
            try:
                result.append(self.dict[key].split(" ")[0].strip()[:-1].lower())
            except Exception as e:
                result.append(char)
        return self.splitter.join(result)

    def get_initials(self, char=u'你好'):
        try:
            return self.dict["%x" % ord(char)].split(" ")[0][0]
        except Exception as e:
            return  char


