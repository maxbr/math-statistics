# -*- coding: utf-8 -*-
import xlsxwriter
from  contraClasses import StateFile, Laplas, VyborZnach, intOcenka


# Открываем наш файл со значениями
first = StateFile('f.txt')

# Создаём таблицу лапласа
laplas = Laplas('laplas.txt')

# Создаём, объект со всеми готовыми значениями
kontra = VyborZnach(first, 7, laplas)

# Создаём файл xls для вывода
resultXLS = xlsxwriter.Workbook('result.xlsx')

# Создаём новый лист для задания 1
zad1 = resultXLS.add_worksheet(name='zadanie1')

# Выводим интервальный вариационный ряд, для зад1
# Инициализируем Строки и Столбцы
row = 0
col = 0

zad1.write(row,col,'Interval')

# print(kontra.var_Interval)

zad1.write(1,0,'Xi')
zad1.write(1,1,'Xi+1')
zad1.write(1, 2, 'Ni')
zad1.write(1,3,'Wi')
zad1.write(1,4,'Pi')
zad1.write(1,5,'Xcp')
zad1.write(1,6,'h')
zad1.write(2,6,kontra.var_h)
zad1.write(0,8,'Gistogramma dlya YOTX')

row = 2
col = 0
# Проходимся по Интервалу и выбираем значения
inter_n = kontra.var_Inter_n
# print(kontra.var_listPi)
for i in range(0,inter_n):
    # print(item[1])
    # Xi
    zad1.write(row, col, kontra.var_list_Xi[i])
    # Xi+1
    zad1.write(row, col + 1, kontra.var_list_Xi_1[i])
    #Ni
    zad1.write(row, col + 2, kontra.var_listNi[i])
    # Wi
    zad1.write(row, col + 3, kontra.var_listWi[i])
    # Pi
    zad1.write(row, col + 4, kontra.var_list_Inter_Pi[i])
    # Xсреднее
    zad1.write(row, col + 5, kontra.var_list_X_i_sh[i])

    yotxOutXi0 = "({};0)".format(kontra.var_list_Xi[i])
    yotxOutXi = "({};{})".format(kontra.var_list_Xi[i],kontra.var_listNi[i])
    yotxOutXi_10 = "({};{})".format(kontra.var_list_Xi_1[i],kontra.var_listNi[i])
    yotxOutXi_1 = "({};0)".format(kontra.var_list_Xi_1[i])

    zad1.write(row, col + 8, "{} {} {} {}".format(yotxOutXi0,yotxOutXi,yotxOutXi_10,yotxOutXi_1,))
    row += 1

# ЗАДАНИЕ 2
zad2 = resultXLS.add_worksheet(name='zadanie2')

# ЗАДАНИЕ 3
zad3 = resultXLS.add_worksheet('zadanie3')

# Строим полигон для Worda
zad2.write(0, 0, "Poligon WORD \
 On zhe discrtniy variac ryad \
 On zhe viborochnaja sl velichina")
zad2.write(1, 0, 'Xi')
zad2.write(1, 1, 'Ni')

zad3.write(0, 0, "Viborochnaja sl velichina")
zad3.write(1, 0, 'Xi')
zad3.write(1, 1, 'Ni')


# Сортируем
polKeys = sorted(kontra.var_polygon)
samPoligon = kontra.var_polygon
# Начальные позиции
row = 2
col = 0
# Вывод
for i in range(0, len(kontra.var_polygon)):
    currKey = polKeys[i]
    zad2.write(row, col,     currKey)
    zad2.write(row, col + 1, samPoligon[currKey])
    zad3.write(row, col,     currKey)
    zad3.write(row, col + 1, samPoligon[currKey])
    row += 1



# И для сайта yotx.ru
zad2.write(0, 3, 'Poligon YOTX')
zad2.write(1, 3, '(Xi;Ni)')

# Начальная позиция
row = 2
col += 3

# Вывод
for i in range(0, len(kontra.var_polygon)):
    currKey = polKeys[i]
    # currKeyWithComma = str(currKey).replace('.',',')
    # samPoligonWithComma = str(samPoligon[currKey]).replace('.',',')
    # strOut = "({}:{})".format(currKeyWithComma, samPoligonWithComma)
    strOut = "({};{})".format(currKey, samPoligon[currKey])
    # print(strOut)
    zad2.write(row, col,     strOut)
    row += 1

# ЗАДАНИЕ 4
zad4 = resultXLS.add_worksheet('zadanie4')
col = 0
row = 0

zad4.write(row,col,'Cpednee')
zad4.write(row+1,col,kontra.var_MatOz)

zad4.write(row,col+1,'Dispersiya')
zad4.write(row+1,col+1,kontra.var_Disp)

zad4.write(row,col+2,'Assimetriya')
zad4.write(row+1,col+2,kontra.var_Assym)

zad4.write(row,col+3,'Excess')
zad4.write(row+1,col+3,kontra.var_Excess)

zad4.write(row,col+4,'Empir func sami sdelaem? tam prosto')


# ЗАДАНИЕ 6
zad6 = resultXLS.add_worksheet('zadanie6')
row = 0
col = 0
zad6.write(row,col,'Intervalniye ocenki')
row += 1
zad6.write(row,col,'Ocenka1')

zad6.write(row,col+3,'Ocenka2')

row += 1
zad6.write(row,col,'X vibor')
zad6.write(row,col+1,kontra.var_ocenka1.xv)
zad6.write(row,col+3,kontra.var_ocenka2.xv)


zad6.write(row+1,col,'T')
zad6.write(row+1, col+1, kontra.var_ocenka1.t)
zad6.write(row+1, col+3, kontra.var_ocenka2.t)

zad6.write(row+2,col,'Q')
zad6.write(row+2, col+1, kontra.var_ocenka1.q)
zad6.write(row+2, col+3, kontra.var_ocenka2.q)

zad6.write(row+3,col,'N')
zad6.write(row+3, col+1, kontra.var_ocenka1.n)
zad6.write(row+3, col+3, kontra.var_ocenka2.n)

zad6.write(row+4,col,'A1')
zad6.write(row+4, col+1, kontra.var_ocenka1.a1)
zad6.write(row+4, col+3, kontra.var_ocenka2.a1)

zad6.write(row+5,col,'A2')
zad6.write(row+5, col+1, kontra.var_ocenka1.a2)
zad6.write(row+5, col+3, kontra.var_ocenka2.a2)

zad6.write(row+6,col,'S')
zad6.write(row+6, col+1, kontra.var_ocenka1.s)
zad6.write(row+6, col+3, kontra.var_ocenka2.s)




# ЗАДАНИЕ 7
row = 0
col = 0
zad7 = resultXLS.add_worksheet('zadanie7')

zad7.write(row,col,'N')
zad7.write(row,col+1,' ')
zad7.write(row,col+2,'Xi')
zad7.write(row,col+3,'Xi+1')
zad7.write(row,col+4,'Ni')
zad7.write(row,col+5,'Xi - (X srednee *)')
zad7.write(row,col+6,'Xi+1 - (X srednee *)')
zad7.write(row,col+7,'Zi')
zad7.write(row,col+8,'Zi+1')
zad7.write(row,col+9,'F(Zi)')
zad7.write(row,col+10,'F(Zi+1)')
zad7.write(row,col+11,'Pi')
zad7.write(row,col+12,'N\'i')
zad7.write(row,col+13,'X srednee *')
zad7.write(row,col+14,'Shestoy')
zad7.write(row,col+15,'Vosmoy')
zad7.write(row,col+16,'Hi^2 nabl')
zad7.write(row,col+17,'Hi^2 krit')
row = 1
for i in range(0,kontra.var_Inter_n):
    zad7.write(row+i,col,i)
    zad7.write(row+i,col+2,kontra.var_list_Xi[i])
    zad7.write(row+i,col+3,kontra.var_list_Xi_1[i])
    zad7.write(row+i,col+4,kontra.var_listNi[i])
    zad7.write(row+i,col+5,kontra.var_list_Xi[i] - kontra.var_X_sh)
    zad7.write(row+i,col+6,kontra.var_list_Xi_1[i] - kontra.var_X_sh)
    zad7.write(row+i,col+7,kontra.var_list_Zi[i])
    zad7.write(row+i,col+8,kontra.var_list_Zi_1[i])
    zad7.write(row+i,col+9,kontra.var_list_Fi[i])
    zad7.write(row+i,col+10,kontra.var_list_Fi_1[i])
    zad7.write(row+i,col+11,kontra.var_listPi[i])
    zad7.write(row+i,col+12,kontra.var_listN_sh_i[i])
    zad7.write(row+i,col+14,kontra.var_list6[i])
    zad7.write(row+i,col+15,kontra.var_list8[i])

zad7.write(row,col+13,kontra.var_X_sh)
zad7.write(row,col+16,kontra.var_hi_kvedrat_nabl)
zad7.write(row,col+17,kontra.var_hi_krit)

sumStr = '=SUM(E{}:E{})'.format(2,kontra.var_Inter_n+1)
zad7.write(kontra.var_Inter_n+1, 4, sumStr)
# zad7.write(0,10,'dadasdasdasd')

# zad7.write(row+1,col+18,'N')
resultXLS.close()