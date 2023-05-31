import random
import sys
import strings
import math


def get_input():

    params = {}
    args = sys.argv[1:]

    for i in range(len(args)):
        params[args[i][1]] = args[i][3:]

    if len(params) == 0:
        params = {'g': 'lc', 'i': [6075, 106, 1283, random.randint(1, 1000)], 'n': 10000, 'f': 'rnd.dat'}
        return params

    keys = params.keys()

    if 'h' in keys:
        params['h'] = True

    if 'g' not in keys:
        params['g'] = 'lc'

    if 'i' in keys:
        params['i'] = list(map(int, params['i'].split(',')))
    else:
        params['i'] = [6075, 106, 1283, random.randint(1, 1000)]

    if 'n' in keys:
        params['n'] = int(params['n'])
    else:
        params['n'] = 10000

    if 'f' not in keys:
        params['f'] = 'rnd.dat'

    return params


def save_to_file(number_sequence, seq_length, path):

    with open(path, 'w') as f:
        for i in range(seq_length):
            f.write(str(number_sequence[i]) + ('\n' if i == seq_length - 1 else ','))


def percentage(i, quarter, half, three_quarters):

    if i == quarter:
        print('Генерация чисел завершена на 25%!')
    elif i == half:
        print('Генерация чисел завершена на 50%!')
    elif i == three_quarters:
        print('Генерация чисел завершена на 75%!')


def rsa_machinerie(seq_length, init_x, _pow, modulo, phi, w, is_bbs=False):

    number_sequence = list()
    quarter, half, three_quarters = seq_length // 4, seq_length // 2, seq_length // 4 * 3

    print('Генерация чисел началась!')

    for i in range(seq_length):
        bit_seq = list()
        for j in range(w):
            init_x = pow(init_x, _pow, modulo)
            bit_seq.append(init_x % 2)
        bit_seq.reverse()
        init_x = random.randint(2, modulo - 1)
        if is_bbs:
            while math.gcd(init_x, modulo) != 1:
                init_x = random.randint(2, modulo - 1)
            inix_x = (init_x * init_x) % modulo
        if not is_bbs:
            _pow = random.randint(2, phi - 1)
            while math.gcd(_pow, phi) != 1:
                _pow = random.randint(2, phi - 1)

        number_sequence.append(sum([0 if bit_seq[k] == 0 else 2 ** k for k in range(w)]))
        percentage(i, quarter, half, three_quarters)

    print('Генерация чисел завершена!')

    return number_sequence


def bbs(init_vector, seq_length, path):

    p, q, n = 127, 131, 16637
    phi = (p - 1) * (q - 1)
    x, w = init_vector

    if math.gcd(x, n) != 1:
        print(strings.invalid_init_x)
        while math.gcd(x, n) != 1:
            x = random.randint(2, n - 1)
    x = (x * x) % n

    number_sequence = rsa_machinerie(seq_length, x, 2, n, phi, w, is_bbs=True)
    save_to_file(number_sequence, seq_length, path)

#python3 prng.py /g:rsa /i:514081,99991,0,127,10
def rsa(init_vector, seq_length, path):

    number_sequence = []
    p, q, e, init_x, w = init_vector
    n, phi = p * q, (p - 1) * (q - 1)

    if not (1 < e < phi) or math.gcd(e, phi) != 1:
        print(strings.invalid_e)
        e = 0
        while math.gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)

    if not (1 < init_x < n):
        print(strings.invalid_init_x)
        init_x = random.randint(1, n - 1)

    number_sequence = rsa_machinerie(seq_length, init_x, e, n, phi, w)
    save_to_file(number_sequence, seq_length, path)


"""
stream=$(python3 -c "import random; input=''.join([str(random.randint(1, 1024)) + ('' if i == 255 else ',') for i in range(256)]); print(input)")
python3 prng.py /g:rc4 /i:$stream
"""

def rc4(init_vector, seq_length, path):

    number_sequence = []
    s_block, key, j = [i for i in range(256)], init_vector, 0
    quarter, half, three_quarters = seq_length // 4, seq_length // 2, seq_length // 4 * 3

    for i in range(256):
        j = ( j + s_block[i] + key[i] ) % 256
        s_block[i], s_block[j] = s_block[j], s_block[i]

    i, j = 0, 0

    print('Генерация чисел началась!')

    for k in range(seq_length):

        i = ( i + 1 ) % 256
        j = ( j + s_block[i] ) % 256
        s_block[i], s_block[j] = s_block[j], s_block[i]
        t = ( s_block[i] + s_block[j] ) % 256
        number_sequence.append(s_block[t])

        percentage(k, quarter, half, three_quarters)

    print('Генерация чисел завершена!')

    save_to_file(number_sequence, seq_length, path)


mt = [0 for i in range(624)]
def twist(mt):

    lower_mask, upper_mask, reg_len = 0x7fffffff, 0x80000000, 624

    for i in range(reg_len):
        x = (mt[i] & upper_mask) + (mt[(i + 1) % reg_len] & lower_mask)
        xA = x >> 1
        if (x % 2) != 0:
            xA ^= 0x9908b0df
        mt[i] = mt[(i + 397) % reg_len] ^ xA


def extract_number(index, mt):

    if index >= 624:
        twist(mt)
        index = 0

    y = mt[index]
    y ^= ((y >> 11) & 0xffffffff)
    y ^= ((y <<  7) & 0x9d2c5680)
    y ^= ((y << 15) & 0xefc60000)
    y ^=  (y >> 18)

    index += 1

    return index, y & 0xffffffff


def MT(init_vector, seq_length, path):

    modulus, seed = init_vector
    register_len, number_sequence = 624, []
    index, gen_num = register_len, 1812433253
    mt[0] = seed
    quarter, half, three_quarters = seq_length // 4, seq_length // 2, seq_length // 4 * 3

    for i in range(1, register_len):
        temp = gen_num * (mt[i - 1] ^ (mt[i - 1] >> 30)) + i
        mt[i] = temp & 0xffffffff

    print('Генерация чисел началась!')

    for i in range(seq_length):

        index, y = extract_number(index, mt)
        number_sequence.append(y % modulus)
        percentage(i, quarter, half, three_quarters)

    print('Генерация чисел завершена!')

    save_to_file(number_sequence, seq_length, path)


def bit_array_conversion(input_register):

    input_register = list(map(int, str(input_register)))
    input_register.reverse()

    return input_register


def bitwise_or(fb_rev, sb_rev):

    fb_rev_s, sb_rev_s = len(fb_rev), len(sb_rev)
    min_size = min(fb_rev_s, sb_rev_s)

    return [1 if fb_rev[i] == 1 or sb_rev[i] == 1 else 0 for i in range(min_size)] + (fb_rev[min_size:] if fb_rev_s > sb_rev_s else sb_rev[min_size:])


def xor(fb_rev, sb_rev):

    fb_rev_s, sb_rev_s = len(fb_rev), len(sb_rev)
    min_size = min(fb_rev_s, sb_rev_s)

    return [(fb_rev[i] + sb_rev[i]) % 2 for i in range(min_size)] + (fb_rev[min_size:] if fb_rev_s > sb_rev_s else sb_rev[min_size:])


def nfsr(init_vector, seq_length, path):

    R1, R2, R3 = init_vector[:3]
    reg_R1, reg_R2, reg_R3, w = init_vector[3:]
    R1, R2, R3 = list(map(bit_array_conversion, [R1, R2, R3]))
    reg_R1, reg_R2, reg_R3 = list(map(bit_array_conversion, [reg_R1, reg_R2, reg_R3]))
    R = bitwise_or( bitwise_or( xor(R1, R2), xor(R2, R3) ), R3 )
    reg_R = bitwise_or( bitwise_or( xor(reg_R1, reg_R2), xor(reg_R2, reg_R3) ), reg_R3 )

    number_sequence = lfsr_machinerie(seq_length, 0, w, [i for i in range(len(R)) if R[i] == 1], reg_R)
    save_to_file(number_sequence, seq_length, path)


def lfsr_machinerie(seq_length, p, w, nonzero_coeffs, init_register=[]):

    number_sequence, bit_seq = [], []
    quarter, half, three_quarters = seq_length // 4 * w, seq_length // 2 * w, seq_length // 4 * 3 * w

    print('Генерация чисел началась!')

    if len(init_register) == 0:
        bit_seq = [random.randint(0, 1) for k in range(p)]
        bit_seq.reverse()
    else:
        bit_seq = init_register

    for i in range(seq_length * w):

        bit_seq.append(sum(bit_seq[i + nonzero_coeffs[k]] for k in range(len(nonzero_coeffs))) % 2)
        if i % (w - 1) == 0 and i != 0:
            current_binary = bit_seq[-w:]
            binary_converted = sum([0 if current_binary[i] == 0 else 2 ** i for i in range(w)])
            number_sequence.append(binary_converted)

        percentage(i, quarter, half, three_quarters)

    print('Генерация чисел завершена!')

    return number_sequence


def lfsr(init_vector, seq_length, path):

    coef_vec, init_register, w = init_vector
    coef_vec, init_register = list(map(int, str(coef_vec))), list(map(int, str(init_register)))
    coef_vec.reverse(), init_register.reverse()
    nonzero_coeffs = [i for i in range(len(coef_vec)) if coef_vec[i] == 1]

    number_sequence = lfsr_machinerie(seq_length, 0, w, nonzero_coeffs, init_register)
    save_to_file(number_sequence, seq_length, path)


def five_p(init_vector, seq_length, path):

    p, q_1, q_2, q_3, w = init_vector
    nonzero_coeffs = [0, q_1, q_2, q_3]

    number_sequence = lfsr_machinerie(seq_length, p, w, nonzero_coeffs)
    save_to_file(number_sequence, seq_length, path)


def add(init_vector, seq_length, path):

    modulus, k_delay, j_delay, number_sequence = init_vector[0], init_vector[1], init_vector[2], init_vector[3:]
    quarter, half, three_quarters = seq_length // 4, seq_length // 2, seq_length // 4 * 3

    print('Генерация чисел началась!')

    for i in range(seq_length):
        number_sequence.append((number_sequence[j_delay - k_delay + i] + number_sequence[i]) % modulus)
        percentage(i, quarter, half, three_quarters) 

    print('Генерация чисел завершена!')

    save_to_file(number_sequence[-seq_length:], seq_length, path)


def lc(init_vector, seq_length, path):

    number_sequence = []
    modulus, multiplicator, increment, init_value = init_vector
    number_sequence.append(init_value)
    accum = init_value

    quarter, half, three_quarters = seq_length // 4, seq_length // 2, seq_length // 4 * 3

    print('Генерация чисел началась!')

    for i in range(1, seq_length):
        
        accum = (multiplicator * accum + increment) % modulus
        number_sequence.append(accum)
        percentage(i, quarter, half, three_quarters)

    print('Генерация чисел завершена!')

    save_to_file(number_sequence, seq_length, path)


def main():

    params = get_input()
    method, init_vector, seq_length, path = params['g'], params['i'], params['n'], params['f']

    if 'h' in params.keys():
        print(strings.help)
        return

    if method=='lc':
        lc(init_vector, seq_length, path)
    elif method=='add':
        add(init_vector, seq_length, path)
    elif method=='5p':
        five_p(init_vector, seq_length, path)
    elif method=='lfsr':
        lfsr(init_vector, seq_length, path)
    elif method=='nfsr':
        nfsr(init_vector, seq_length, path)
    elif method=='mt':
        MT(init_vector, seq_length, path)
    elif method=='rc4':
        rc4(init_vector, seq_length, path)
    elif method=='rsa':
        rsa(init_vector, seq_length, path)
    elif method=='bbs':
        bbs(init_vector, seq_length, path)
    else:
        print('Такого генератора нет!')
        return

if __name__ == '__main__':
    main()

#prng.py /g:lc /i:1223,7,11,3
#prng.py /g:add /i:100,24,55,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55
#prng.py /g:5p /i:89,20,40,69,10
#prng.py /g:lfsr /i:1000010001,1010101110100011100010101010,10
#prng.py /g:nfsr /i:10101,1000011001,10101000000001,10101001,10101000111001,1010010101010000101011100001,10
#prng.py /g:mt /i:2048,113

"""
import random
input=''.join([str(random.randint(1, 1024)) + ('' if i == 255 else ',') for i in range(256)])
print(input)
"""
#prng.py /g:rc4 /i:281,27,38,169,475,248,398,1,213,431,570,782,743,565,560,427,36,679,321,947,45,141,537,297,498,812,510,824,206,232,266,789,712,473,750,699,731,965,1010,53,97,400,754,597,56,330,462,723,116,30,646,621,64,982,64,77,767,311,464,256,599,647,945,886,825,823,1004,508,576,266,704,977,767,503,116,674,105,994,904,1013,399,535,606,414,1015,165,951,958,52,769,17,1014,952,987,481,772,389,435,1022,998,171,36,159,579,218,174,102,715,898,834,790,888,34,187,1001,108,474,856,365,60,983,144,437,155,270,674,905,334,111,945,380,775,917,792,995,829,855,848,274,645,156,539,11,556,895,980,658,62,81,244,592,89,948,1017,787,749,202,413,840,200,223,92,385,59,725,723,113,1010,490,635,677,729,178,472,124,448,776,624,314,534,379,622,508,471,509,504,428,385,482,174,590,134,920,437,816,301,31,682,471,692,83,342,46,938,647,20,542,647,609,850,888,394,71,700,691,298,1016,146,675,50,701,567,740,692,946,161,675,781,533,485,146,670,236,736,72,626,837,986,935,786,164,922,798,275,601,43,965,737,910,743,117,280,562,944,618,928
"""
#prng.py /g:rsa /i:514081,99991,0,127,10
#prng.py /g:bbs /i:113,10
"""