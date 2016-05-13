# -*- coding: utf-8 -*-
# Класс файл, при инициализации указать путь к файлу
import math,re, xlsxwriter

class intOcenka:
    xv = None
    t = 1.96
    q = None
    n = None
    a1 = None
    a2 = None
    s = None
    def __init__(self):
        self.xv = None
        self.t = 1.96
        self.q = None
        self.n = None
        self.a1 = None
        self.a2 = None
        self.s = None

class StateFile:
    # Путь к файлу
    fInput = ""
    def openFile(self, fPath):
        f = open(fPath, 'r')
        lineF = list(f)
        listA=[]
        for i in lineF:
            num = i[0] + '.' + i[2:4]
            listA.append(float(num))
        listA.sort()
        return listA
    def __init__(self, filename):
        self.fInput = self.openFile(filename)
        # print(type(self.fInput))
    def __str__(self):
        return str(self.fInput)

first = StateFile('f.txt')

class Laplas:
    # Словарь для таблицы Лапласа
    var_dictLaplas = None

    def __init__(self, filename):
        self.var_dictLaplas = self.func_makeLaplas(filename)

    # Создаёт словарь со значениями функции Лапласа
    def func_makeLaplas(self, fpath):
        f = open(fpath,'r')
        diction = {}
        while True:
            str = f.readline()
            if not str:
                 break
            str = re.sub("^\s+|\n|\r|\s+$", '', str)
            str = str.split('\t')
            diction[str[0]] = str[1]
            # print(diction)
        return diction

    def ziIsInFi(self,zi):
        zi = str (zi)
        dictLaplas = self.var_dictLaplas
        # print(zi)
        if zi in dictLaplas.keys():
            return True
        else:
            return False

    def getRawZi(self,zi):
        zi = str(zi)
        dictLaplas = self.var_dictLaplas
        return float(dictLaplas[zi])

    def getFzi(self,zi):
        # print("zi={}".format(zi))
        dictLaplas = self.var_dictLaplas
        if self.ziIsInFi(zi):
            otvet = self.getRawZi(zi)
            # print(otvet)
            # print(type(otvet))
            return otvet
        else:
            offset = 0.01
            minZiFound = False
            maxZiFound = False
            minZi = maxZi = zi
            maxIter = 10
            i = 0
            for i in range(0,maxIter):
                if minZiFound and maxZiFound:
                    break
                # print("i={}".format(i))
                i+=1
                if not minZiFound:
                    minZi = minZi-offset
                    minZi = round(minZi,2)
                    if self.ziIsInFi(minZi):
                        minZiFound = True
                if not maxZiFound:
                    maxZi = maxZi+offset
                    maxZi = round(maxZi,2)
                    if self.ziIsInFi(maxZi):
                        maxZiFound = True
                # print(minZi,maxZi)
                # print(minZiFound,maxZiFound)
            if maxZiFound and minZiFound:
                otvet = (self.getRawZi(minZi) + self.getRawZi(maxZi)) / 2
                # print(otvet)
                # print(type(otvet))
                return otvet
            else:
                return None


# laplas = Laplas('laplas.txt')
# print(laplas.var_dictLaplas)
# print(laplas.ziIsInFi(2.3))
# print(laplas.getFzi(2.3))
# print(laplas.ziIsInFi(3.36))
# print(laplas.getFzi(3.36))
# Выборочные значения
class VyborZnach:
    # Сама выборка
    var_listN = None
    # Выборочное среднее
    var_MatOz = None
    # Дисперсия
    var_Disp = None
    # Эксцесс
    var_Excess = None
    # Асимметрия
    var_Assym = None
    # Дискретный вариационный ряд
    var_VariacRyad = None
    # Самая главня переменная - интервал
    var_Interval = None
    # Количество элементов в выборке
    var_n = None
    # Количество интервалов
    var_Inter_n = None
    # Pi для интервала
    var_list_Inter_Pi = None
    # Шаг h
    var_h = None
    # Полигон
    var_polygon = None
    # Список ni
    var_listNi =None
    # Список омегаi
    var_listWi = None
    # Список pi
    var_listPi = None
    # Список Х, для гистограммы?
    var_listX = None
    # Лапласс
    var_laplass = None
    # Оценка1
    var_ocenka1 = None
    # Оценка 2
    var_ocenka2 = None


    def __init__(self, vyborka, nInterval, lplssObj):
        self.var_listN = vyborka.fInput
        self.var_laplass = lplssObj
        self.var_n = float(len(self.var_listN))
        self.var_MatOz = self.func_ViborSred()
        self.var_Disp = self.func_Dispersia()
        self.var_Excess = self.func_Excess()
        self.var_Assym = self.func_Assim()
        self.var_VariacRyad = self.func_VarRyad()
        self.var_Inter_n = nInterval
        self.var_h = (max(self.var_listN) - min(self.var_listN))/self.var_Inter_n
        self.var_Interval = self.func_Interval()
        self.var_polygon = self.func_poligon()
        self.func_makeArgs()
        self.var_ocenka1 = intOcenka()
        self.var_ocenka2 = intOcenka()
        self.intOcenka1()
        self.intOcenka2()
        self.func_HypoSt1()
        self.func_Hypo_St2()
        self.func_Hypo_St3()
        self.func_Hypo_St4()

   #выборочное среднее
    def func_ViborSred(self):
        return sum(self.var_listN)/len(self.var_listN)
    #дисперсия2
    def func_Dispersia(self):
        Mo = self.var_MatOz
        chisl = 0
        for i in self.var_listN:
            chisl += (i - Mo)*(i - Mo)
        return chisl/self.var_n
    # Эксцесс
    def func_Excess(self):
        Mo = self.var_MatOz
        chisl = 0
        for i in self.var_listN:
            ras = (i - Mo)
            chisl += ras**4
        res = chisl/self.var_n
        res = res/pow(self.var_Disp,2)
        res = res-3
        return res
        # print res

    #асимметрия
    def func_Assim(self):
        Mo = self.var_MatOz
        chisl = 0
        for i in self.var_listN:
            ras = (i - Mo)
            chisl += ras**3
        res = chisl/self.var_n
        s = math.sqrt(self.var_Disp)
        res = res/s**3
        # print(s**3)
        return res
    #дискретный вариационный ряд с абсолютными частотами xi | ni
    #сколько раз встречается каждый элемент
    def func_VarRyad(self):
        dct = dict()
        for i in self.var_listN:
            if i in dct:
                dct[i] += 1
            else:
                dct[i] = 1
        # print "k=", len(dct)
        # for i in sorted(dct):
        #     print i, " : " , dct[i]
        # print
        return dct
    #возвращает интервалы
    def func_Interval(self):
        listH=[]
        lh = min(self.var_listN)
        for i in range(self.var_Inter_n):
            n1 = round(lh, 4)
            n2 = round(lh+self.var_h, 4)
            if i < self.var_Inter_n-1:
                listH.append((n1, n2))
            else:
                listH.append((n1, max(self.var_listN)))
            lh+=self.var_h
        return listH

    #полигон xi | wi=ni/n
    def func_poligon(self):
        dct = self.var_VariacRyad
        for i in dct:
            dct[i] = dct[i]/self.var_n
        # for i in sorted(dct):
        #     print i, " : " , dct[i]
        return dct

    #данные для построения гистограммы
    #i, int, ni, wi, ni/h
    def func_makeArgs(self):
        inter=self.var_Interval
        ni = []
        wi = []
        pi = []
        x = []
        h = self.var_h
        for i in inter:
            nii = 0
            for l in self.var_listN:
                if (l > i[0]) and (l <= i[1]):
                     nii+=1
                if i == inter[0] and l == min(self.var_listN):
                    nii+=1

            ni.append(nii)
            wi.append(nii/100.00)
            pi.append(nii/float(h))
            x.append((i[0]+i[1])/2)
        self.var_listNi = ni
        self.var_listWi = wi
        # print "xv = ", xv
        # print "t = ", t
        # print "q = ", q
        # print "n = ", n
        # print "a1 = ", a1
        # print "a2 = ", a2
        self.var_list_Inter_Pi = pi
        self.var_listX = x

    # Разбил Гистограмму на 2 функции
    def func_Gist(self):
        inter=self.var_Interval
        ni = self.var_listNi
        wi = self.var_listWi
        pi = self.var_listPi
        x = self.var_listX
        h = self.var_h
        listGist = []
        # print "h =", h
        for i in range(self.var_Inter_n):
            # print i, inter[i], ni[i], round(wi[i], 4), round(pi[i],4), round(x[i],4)
            listGist.append((i, inter[i], ni[i], round(wi[i], 4), round(pi[i],4), round(x[i],4)))
        return listGist

    #интервальная оценка номер 1
    def intOcenka1(self):
        ocn = self.var_ocenka1
        ocn.xv = self.var_MatOz
        ocn.t = 1.96
        ocn.q = math.sqrt(self.var_Disp)
        ocn.n = self.var_n
        ocn.a1 = ocn.xv - ocn.t*(ocn.q/math.sqrt(ocn.n))
        ocn.a2 = ocn.xv + ocn.t*(ocn.q/math.sqrt(ocn.n))

    #интервальная оценка номер 2
    def intOcenka2(self):
        ocn = self.var_ocenka2
        ocn.xv = self.var_MatOz
        ocn.n = 100
        ocn.q = 0.143

        chisl = 0
        for i in self.var_listN:
            chisl += (i - ocn.xv)*(i - ocn.xv)
        ocn.s = s = math.sqrt(chisl/(ocn.n-1))
        # print(s)

        ocn.a1 = a1 = s*(1-ocn.q)
        ocn.a2 = a2 = s*(1+ocn.q)

        # print "xv = ", xv
        # print "q = ", q
        # print "n = ", n
        # print "s = ", s
        # print "a1 = ", a1
        # print "a2 = ", a2

    # Список X*i
    var_list_X_i_sh = None
    # X* среднее
    var_X_sh = None
    # Сигма
    var_sigma = None
    # Список Xi
    var_list_Xi = []
    # Список Xi+1
    var_list_Xi_1 = []
    def func_HypoSt1(self):
        PRINT = False
        finalint = self.var_Interval
        n = self.var_Inter_n
        # print("ПЕРВЫЙ ШАГ:")
        sigma = 0
        x_srednee = 0
        listX_ish = []
        for xs in finalint:
            xi = xs[0]
            self.var_list_Xi.append(xi)
            x_i_1 = xs[1]
            self.var_list_Xi_1.append(x_i_1)
            xi_sh = (xi+x_i_1)/2
            listX_ish.append(xi_sh)
            x_srednee += xi_sh
            # xi_sh = round(xi_sh,2)
            # print("Xi={}    Xi+1={}     Xi*={}"\
            #       .format(round(xi,2),round(x_i_1,2),round(xi_sh,2)))
        x_srednee /= n
        self.var_X_sh = x_srednee
        self.var_list_X_i_sh = listX_ish
        # print("X* среднее={}".format(round(x_srednee,2)))
        for i in listX_ish:
            sigma += pow (i - x_srednee,2)
        sigma /= n
        self.var_sigma = sigma
        # print("Сигма*={}".format(round(sigma,2)))

    # Список Zi
    var_list_Zi = []
    # Список Zi + 1
    var_list_Zi_1 = []
    # Список Fi
    var_list_Fi = []
    # Список Fi + 1
    var_list_Fi_1 = []
    def func_Hypo_St2(self):
        # print("ВТОРОЙ ШАГ:")
        # print("найдем интервалы zi и zi + 1 и функции F(zi) и F(zi+1)")

        # Словарь значений функции Лапласа из Приложения 2
        dictLaplas = self.var_laplass.var_dictLaplas
        listF = []
        finalint = self.var_Interval
        n = self.var_Inter_n
        x_srednee = self.var_X_sh
        sigma = self.var_sigma
        for i in range(0,n):
            xi = self.var_list_Xi[i]
            x_i_1 = self.var_list_Xi_1[i]
            # pre_zi = xi - x_srednee
            # pre_zi_1 = x_i_1 - x_srednee
            # print(round(pre_zi,2), round(pre_zi_1,2))
            zi = round ((xi - x_srednee)/sigma,2)
            z_i_1 = round((x_i_1 - x_srednee)/sigma,2)
            self.var_list_Zi.append(zi)
            self.var_list_Zi_1.append(z_i_1)

            # print("Zi={}    Zi+1={}".format(zi,z_i_1)),
            # print(sorted(dictLaplas))
            # print(ziIsInFi(abs(zi),dictLaplas))
            if zi < 0:
                F_zi = - self.var_laplass.getFzi(abs(zi))
            else:
                F_zi =  self.var_laplass.getFzi(abs(zi))

            if z_i_1 < 0:
                F_zi_1 = -  self.var_laplass.getFzi(abs(z_i_1))
            else:
                F_zi_1 =  self.var_laplass.getFzi(abs(z_i_1))

            self.var_list_Fi.append(F_zi)
            self.var_list_Fi_1.append(F_zi_1)
            F_zi = round(F_zi,2)
            F_zi_1 = round(F_zi_1,2)

            listF.append((F_zi,F_zi_1))
            #
            # if F_zi != None:
            #     print("    F_zi={}".format(F_zi)),
            # else:
            #     print("    ERROR!")
            #
            # if F_zi_1 != None:
            #     print("    F_zi+1={}".format(F_zi_1))
            # else:
            #     print("    ERROR!")

    # Список Pi
    var_listPi = []
    # Сумма Pi
    var_sum_Pi = 0
    # Список n*i
    var_listN_sh_i = []
    # Сумма n*i
    var_sumN_sh_i =0
    def func_Hypo_St3(self):
        # print("ТРЕТИЙ ШАГ:")
        # print("найдем теоретические вероятности P_i\n"\
        #       " и теоретический частоты n'_i = n * P_i = 100 * P_i")
        # print(listF)
        # Считаем Pi
        listPi =[]
        sumPi = 0
        n = self.var_Inter_n
        for i in range(0,n):
            Pi = self.var_list_Fi_1[i] - self.var_list_Fi[i]
            sumPi+=Pi
            Pi = round(Pi,2)
            # print(Pi)
            listPi.append(Pi)
        # print(listPi)
        self.var_listPi = listPi
        self.var_sum_Pi = sumPi
        # print("Сумма Pi={}".format(sumPi))
        # print("Считаем n'_i")
        listN_sh_i = []
        sumN_sh_i =0
        for p_i in listPi:
            n_sh_i = 100 * p_i
            sumN_sh_i += n_sh_i
            # print(n_sh_i)
            listN_sh_i.append(n_sh_i)
        # print("Сумма N_i={}".format(sumN_sh_i))
        self.var_listN_sh_i = listN_sh_i
        self.var_sumN_sh_i = sumN_sh_i

    # Стольбец 6
    var_list6 = []
    # Стольбец 8
    var_list8 = []
    # Хи квадрат наблюдаемое
    var_hi_kvedrat_nabl = None
    # Хи критическое
    var_hi_krit = 9.5
    # Проверка
    var_proverka = 0
    def func_Hypo_St4(self):
        # print("НАКОНЕЦТО ШАГ4!")
        # print("Найдём Хи^2 наблюдаемое")

        spisok = self.var_listNi
        # print(spisok)
        # Берем ni
        # i1 = 0
        # Так как у нас 100 элементов в выборке
        n = self.var_Inter_n
        hi_kvedrat_nabl = -100
        proverka = 0
        # print("6    8")
        for i in range(0, n):
            # print(ni)
            ni = self.var_listNi[i]
            n_sh_i = self.var_listN_sh_i[i]
            # СТРАНИЦА 257 УЧЕБНИКА, ТАБЛИЦА 23 СТОЛБЦЫ 6 И 8
            shesht = pow((ni - n_sh_i),2)/n_sh_i
            self.var_list6.append(shesht)

            vosem = pow((ni),2)/n_sh_i
            self.var_list8.append(vosem)

            hi_kvedrat_nabl += vosem
            proverka += shesht
        self.var_hi_kvedrat_nabl = hi_kvedrat_nabl
        self.var_proverka = proverka

        #     print("{}    {}".format(shesht,vosem))
        #     i1+=1
        # print("Хи квадрат ровно={}    Проверка={}".format(hi_kvedrat_nabl,proverka))
        # hi_krit = 9.5
        # print("Хи критичексое равно={} (на стр257 в учебнике, или найти самим по приложению 5)".format(hi_krit))
        # print("Проверяем гипотезы, ответ: "),
        # if hi_kvedrat_nabl > hi_krit:
        #     print("данные наблюдений НЕ СОГЛАСУЮТСЯ с гипотезой о нормальном распределении генеральной совокупности.")
        #     print("Так как Хи.квадрат.наблюдаемое БОЛЬШЕ Хи.квадрат.критического, гипотеза о нормальном распределении генеральной совокупности ОТВЕРГАЕТСЯ")
        # elif hi_kvedrat_nabl < hi_krit:
        #     print("данные наблюдений СОГЛАСУЮТСЯ с гипотезой о нормальном распределении генеральной совокупности.")
        #     print("Так как Хи.квадрат.наблюдаемое МЕНЬШЕ Хи.квадрат.критического, гипотеза о нормальном распределении генеральной совокупности ПРИНИМАЕТСЯ")

#
# a = VyborZnach(first,7, laplas)
# print a.var_MatOz,
# print a.var_Disp
# print a.var_VariacRyad
# print a.var_Interval
# print a.var_polygon
# print a.var_listPi
# a.func_Gist()
# a.intOcenka1()
# print
# a.intOcenka2()
# xv =  1.0558
# t =  1.96
# q =  0.429986464903
# n =  100.0
# a1 =  0.971522652879
# a2 =  1.14007734712
#
#
# xv =  1.0558
# q =  0.143
# n =  100
# s =  0.432152657277
# a1 =  0.370354827287
# a2 =  0.493950487268
# print(a.var_list_Zi)
# print(a.var_list_Fi)
# print a.var_list_Zi_1
# print a.var_hi_kvedrat_nabl
# print a.var_proverka