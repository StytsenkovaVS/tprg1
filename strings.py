help = """
/g:<код_метода> -- параметр указывает на метод генерации ПСЧ, при этом код_метода может быть
одним из следующих:                                 
1) lc – линейный конгруэнтный метод; /i: модуль, множитель, приращение, начальное значение;               
2) add – аддитивный метод; /i: модуль, младший индекс, старший индекс, последовательность начальных значений;
3) 5p – пятипараметрический метод; /i: p, q_1, q_2, q_3, w;
4) lfsr – регистр сдвига с обратной связью (РСЛОС); /i: двоичное представление вектора коэффициентов, начальное значение регистра;
5) nfsr – нелинейная комбинация РСЛОС; /i: двоичные представления векторов коэффициентов для R1, R2, R3, скомбинированных функцией R1^R2 + R2^R3 + R3
6) mt – вихрь Мерсенна; /i: модуль, начальное значение x;
7) rc4 – RC4; /i: 256 начальных значений;
8) rsa – ГПСЧ на основе RSA; /i: модуль n, число e, начальное значение x. e удовлетворяет: 1 < e < (p - 1) * (q - 1), НОД(e, (p - 1) * (q - 1)) = 1, p * q = n, x из [1, n];
9) bbs – алгоритм Блюма-Блюма-Шуба; /i: начальное значение x (взаимно простое с n). При генерации используются параметры: p=127, q=131, n=p*q=16637.

/n:<длина> -- количество генерируемых чисел. Если параметр не указан, -- генерируется 10000 чисел.

/f:<полное_имя_файла> -- полное имя файла, в который будут выводиться данные. Если параметр не указан, данные будут записаны в файл с именем rnd.dat.

/h -- информация о допустимых параметрах командной строки программы.
"""

invalid_e = 'Некорректное значение e! Этот параметр будет сгенерирован автоматически.'

invalid_init_x = 'Некорректное начальное значение x! Этот параметр будет сгенерирован автоматически.'
