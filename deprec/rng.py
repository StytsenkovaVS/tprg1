import argparse
import os
import random


def save_to_file(sequence, length, path, newlined=''):

    extracted_file_name = os.path.basename(path)
    previous_path = path
    path = path if extracted_file_name == path or (os.path.isdir(os.path.dirname(path)) and '.' in extracted_file_name) else "rnd.dat"

    if previous_path != path:
        print('Указанная Вами директория не может быть найдена! Последовательность будет записана в файл rnd.dat.')

    with open(path, "w") as f:
        for i in range(length):
            f.write(sequence[i] + ' ' + newlined)
        f.write('\n')


def get_input(first_string, second_string):

    value = input(first_string)
    while True:
        if value.isdigit() and int(value) > 0:
            value = int(value)
            break
        else:
            value = input(second_string)
    
    return value


def lfsr(length, path):

    nonzero_coeffs, zero_coeffs = [], []

    p = get_input('Введите натуральное число p (степень линейной булевой функции плюс один): ', 'Некорректный ввод! Введите натуральное число: ')

    nonzero_coeffs_number = input('Введите количество ненулевых коэффициентов этой функции (бит X_n всегда ненулевой и здесь не учитывается): ')
    while True:
        if nonzero_coeffs_number.isdigit() and 0 <= int(nonzero_coeffs_number) < p:
            nonzero_coeffs_number = int(nonzero_coeffs_number)
            break
        else:
            nonzero_coeffs_number = input('Некорректный ввод! Введите натуральное число, меньшее степени линейной булевой функции: ')

    w = get_input('Введите количество битов, которое надо сгенерировать: ', 'Некорректный ввод! Введите натуральное число: ')

    if nonzero_coeffs_number == p - 1:   nonzero_coeffs = [i for i in range(nonzero_coeffs_number)]
    elif nonzero_coeffs_number == 0: nonzero_coeffs.append(0)
    elif nonzero_coeffs_number < p // 2:
        nonzero_coeffs = input("Введите 'степени' битов при ненулевых кф-ах (0 < степень < p) через пробел ({} значений/е/я): ".format(nonzero_coeffs_number)).split()
        while True:
            nonzero_coeffs = list(set([int(nonzero_coeffs[i]) for i in range(len(nonzero_coeffs)) if nonzero_coeffs[i].isdigit() and 0 < int(nonzero_coeffs[i]) < p]))
            if len(nonzero_coeffs) != nonzero_coeffs_number:
                nonzero_coeffs = input('Некорректный ввод! Попробуйте снова: ')
            else:
                nonzero_coeffs.append(0)
                break
    else:
        zero_coeffs = input("Введите 'степени' битов при нулевых кф-ах (0 < степень < p) через пробел ({} значений/е/я): ".format(p - (nonzero_coeffs_number + 1))).split()
        while True:
            zero_coeffs = list(set([int(zero_coeffs[i]) for i in range(len(zero_coeffs)) if zero_coeffs[i].isdigit() and 0 < int(zero_coeffs[i]) < p]))
            if len(zero_coeffs) != p - (nonzero_coeffs_number + 1):
                zero_coeffs = input('Некорректный ввод! Попробуйте снова: ')
            else:
                nonzero_coeffs = [i for i in range(p) if i not in zero_coeffs]
                break
            
    number_sequence = lfsr_machinerie(length, p, w, nonzero_coeffs)
    save_to_file(number_sequence, length, path, '\n')            


def lfsr_machinerie(length, p, w, nonzero_coeffs):
    
    number_sequence = []

    for i in range(length):

        bit_seq = [random.randint(0, 1) for k in range(p)]
        bit_seq.reverse()

        for j in range(w):
            bit_seq.append(sum([bit_seq[j + nonzero_coeffs[k]] for k in range(len(nonzero_coeffs))]) % 2)
        current_binary = bit_seq[-w:]
        binary_converted = sum(current_binary[w - i] * 2 ** (i - 1) for i in range(w, 0, -1))
        number_sequence.append(str((current_binary, binary_converted)))

    return number_sequence


def five_p(init_vec, length, path):
    
    p, q_1, q_2, q_3, w = init_vec
    nonzero_coeffs = [0, q_1, q_2, q_3]

    number_sequence = lfsr_machinerie(length, p, w, nonzero_coeffs)
    save_to_file(number_sequence, length, path, '\n')


def add(length, path):

    word_list = ['модуля', 'запаздывания', 'запаздывания', 'ответа']
    letter_list, params, sequence = ['m', 'k', 'j', 'ans'], [], []

    for i in range(4):

        if i == 0 or i == 1:
            user_input = input('Введите значение {} {} ({} > 0): '.format(word_list[i], letter_list[i], letter_list[i]))
            while True:
                if user_input.isdigit() and int(user_input) > 0 and (True if i == 0 else int(user_input) < length - 1):
                    params.append(int(user_input))
                    break
                else:
                    user_input = input('Ошибка! Введите положительное целое число' + 
                                       (': ' if i == 0 else ', которое меньше длины последовательности как минимум на один: '))
        elif i == 2:
            user_input = input('Введите значение {} {} ({} > k): '.format(word_list[i], letter_list[i], letter_list[i]))
            while True:
                if user_input.isdigit() and params[1] < int(user_input) <= length:
                    params.append(int(user_input))
                    break
                else:
                    user_input = input('Введите целое положительное число, которое больше параметра запаздывания k и меньше длины последовательности: ')
        else:
            user_input = input("""Вы хотите автоматически сгенерировать первые {} члена/членов последовательности или ввести их вручную? 
Введите утвердительное значение {} {} для автоматической генерации (Yy/Nn; Дда/Ннет; Yyes/Nno): """.format(params[2], word_list[i], letter_list[i]))
            while True:
                lowered = user_input.lower()
                if lowered in ('y', 'yes', 'да'):
                    params.append('y')
                    break
                elif lowered in ('n', 'no', 'нет'):
                    params.append('n')
                    break
                else:
                    user_input = input('Введите корректный ответ на вопрос: ')

    modulus, k_delay, j_delay, ans = params

    if ans == 'y':
        print("""Вы выбрали автоматическую генерацию первых {} членов последовательности. 
Им будут присвоены произвольные неотрицательные целочисленные значения из диапазона [0, модуль).""".format(j_delay))
                      
        for i in range(j_delay):
            sequence.append(random.randint(0, modulus - 1))
        print('Автоматически сгенерированные первые {} членов последовательности: {}.'.format(min(25, j_delay), sequence[:min(25, j_delay)]))
    else:
        print("""Вы выбрали самостоятельный ввод первых {} членов последовательности.
Начинайте ввод, числа разделяются пробелом: """.format(j_delay), end='')
        
        user_input = input().split()

        while True:
            user_input = [int(user_input[i]) for i in range(len(user_input)) if 0 <= user_input[i].isdigit() < modulus]
            if len(user_input) != j_delay:
                user_input = input('Вы ввели неправильную последовательность чисел! Попробуйте снова: ')
            else:
                sequence += user_input
                break

    for i in range(length - j_delay):
        #print('Это новый элемент последовательности с номером {}: X_{} = X_{} + X_{} mod {} = {}.'.format(
        #    j_delay + i, j_delay + i, j_delay - k_delay + i, i, modulus, (sequence[j_delay - k_delay + i] + sequence[i]) % modulus))
        sequence.append((sequence[j_delay - k_delay + i] + sequence[i]) % modulus)
        
    sequence = [str(sequence[i]) for i in range(length)]
    save_to_file(sequence, length, path)


def lc(length, path):
    
    word_list = ['модуля', 'множителя', 'приращения', 'начального значения']
    letter_list, params, sequence = ['m', 'a', 'c', 'X_0'], [], []

    for i in range(4):
        
        if i == 0:
            user_input = input('Введите значение {} {} ({} > 0): '.format(word_list[i], letter_list[i], letter_list[i]))
            while True:
                if user_input.isdigit() and int(user_input) > 0:
                    params.append(int(user_input))
                    break
                else:
                    user_input = input('Ошибка! Введите положительное целое число: ')
        else:
            user_input = input('Введите значение {} {} (0 <= {} <= m): '.format(word_list[i], letter_list[i], letter_list[i]))
            while True:
                if user_input.isdigit() and 0 <= int(user_input) <= params[0]:
                    params.append(int(user_input))
                    break
                else:
                    user_input = input('Ошибка! Введите положительное целое число в диапазоне от 0 до значения модуля включительно: ')

    modulus, multiplier, increment, init_value = params
    accum = init_value
    sequence.append(str(init_value))
        
    for i in range(1, length):
        accum = (multiplier * accum + increment) % modulus
        sequence.append(str(accum))
    
    save_to_file(sequence, length, path)

    
def main():
    
    parser = argparse.ArgumentParser(description='Программа для генерации псевдослучайных величин.')
    parser.add_argument('-g', choices=['lc', 'add', '5p', 'lfsr', 'nfsr', 'mt', 'rc4', 'rsa', 'bbs'], 
                        help="""
        -g <код_метода> -- параметр указывает на метод генерации ПСЧ, при этом код_метода может быть
        одним из следующих:                                 
        1) lc – линейный конгруэнтный метод;                
        2) add – аддитивный метод;                          
        3) 5p – пятипараметрический метод;                  
        4) lfsr – регистр сдвига с обратной связью (РСЛОС); 
        5) nfsr – нелинейная комбинация РСЛОС;              
        6) mt – вихрь Мерсенна;                             
        7) rc4 – RC4;                                       
        8) rsa – ГПСЧ на основе RSA;                        
        9) bbs – алгоритм Блюма-Блюма-Шуба;                 
                             """, default='5p')
    parser.add_argument('-i', nargs='+', help='-i <число> -- инициализационный вектор генератора.', type=int, default=[89, 20, 40, 60, 16])
    parser.add_argument('-n', type=int, default=10000, 
                        help="""
        -n <длина> -- количество генерируемых чисел. Если параметр не указан, -- генерируется 10000 чисел.
                             """)
    parser.add_argument('-f', default='rnd.dat', 
                        help="""
        -f <полное_имя_файла> -- полное имя файла, в который будут выводиться данные. 
        Если параметр не указан, данные должны записываться в файл с именем rnd.dat.')
                             """)

    args = parser.parse_args()
    method_code, init_vec, length, path = args.g, args.i, args.n, args.f

    if method_code == 'lc':
        lc(length, path)
    elif method_code == 'add':
        add(length, path)
    elif method_code == '5p':

        if init_vec is not None:
            init_vec = [str(init_vec[i]) for i in range(min(len(init_vec), 5)) if init_vec[i] > 0]
        else:
            init_vec = input('Инициализационный вектор не был введён! Попробуйте снова, вводя параметры через пробел: ').split()

        while True:
            init_vec = [int(init_vec[i]) for i in range(min(len(init_vec), 5)) if init_vec[i].isdigit()]
            p = init_vec[0]
            if len(init_vec) != 5 or p < init_vec[1] or p < init_vec[2] or p < init_vec[3]:
                init_vec = input('Вы ввели неправильное значение параметров! Попробуйте снова: ').split()
            else:
                break

        five_p(init_vec, length, path)
    
    elif method_code == 'lfsr':
        lfsr(length, path)


if __name__ == '__main__':
    main()
