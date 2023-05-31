import random


class Generator:
    def __init__(self, links=None):
        self.p = 89
        self.w = 10
        self.links = (0, 20, 40, 69)
        self.buffer = []
 
        self.__init_buffer()
 
 
    def next(self):
        self.__shift_bits()
        return self.__convert_to_int()
 
 
    def __shift_bits(self):
        value = self.__form_bit()
        del self.buffer[0]
        self.buffer.insert(self.p - 1, value)
 
 
    def __convert_to_int(self):
        value = "".join(map(str, self.buffer[0:self.w + 1]))
        return int(value, 2)
 
 
    def __form_bit(self):
        # возвращает значение следующего бита
        value = 0
 
        for index in self.links:
            value += self.buffer[index]
 
        return value % 2
 
 
    def __init_buffer(self):
        # предзаполнение буфера
        for _ in range(self.p):
            self.buffer.append(random.randint(0, 1))


def main():

    gen = Generator()
    print(gen.next())


if __name__ == "__main__":
    main()