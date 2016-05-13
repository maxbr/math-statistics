#### !/usr/bin/env python
# -*- coding: utf-8 -*-

import math, re

#считывает и преобразовывает входные данные
#к отсортированному списку
def openFile():
    f = open('f.txt', 'r')
    lineF = list(f)
    listA=[]
    for i in lineF:
        num = i[0] + '.' + i[2:4]
        listA.append(float(num))
    listA.sort()
    return listA
listNumber = openFile()

def makeLaplas():
    f = open('laplas.txt','r')
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

def ziIsInFi(zi, dictLaplas):
    zi = str (zi)
    # print(zi)
    if zi in dictLaplas.keys():
        return True
    else:
        return False

def getRawZi(zi,dictLaplas):
    zi = str(zi)
    return float(dictLaplas[zi])

def getFzi(zi, dictLaplas):
    # print("zi={}".format(zi))
    if ziIsInFi(zi,dictLaplas):
        otvet = getRawZi(zi,dictLaplas)
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
                if ziIsInFi(minZi,dictLaplas):
                    minZiFound = True
            if not maxZiFound:
                maxZi = maxZi+offset
                maxZi = round(maxZi,2)
                if ziIsInFi(maxZi,dictLaplas):
                    maxZiFound = True
            # print(minZi,maxZi)
            # print(minZiFound,maxZiFound)
        if maxZiFound and minZiFound:
            otvet = (getRawZi(minZi,dictLaplas) + getRawZi(maxZi,dictLaplas)) / 2
            # print(otvet)
            # print(type(otvet))
            return otvet
        else:
            return None



#выборочное среднее
def viborSred(listN):
    return sum(listN)/len(listN)


#дисперсия2
def dispersia2(listN):
    Mo = viborSred(listN)
    chisl = 0
    for i in listN:
        chisl += (i - Mo)*(i - Mo)
    return chisl/float(len(listN))

    
#возвращает интервалы
def interval(listN, n):
    h = (max(listN) - min(listN))/n
    listH=[]
    lh = min(listN)
    for i in range(n):
        n1 = round(lh, 4)
        n2 = round(lh+h, 4)
        if i < n-1:
            listH.append((n1, n2))
        else:
            listH.append((n1, max(listN)))
        lh+=h
    return listH


#дискретный вариационный ряд с абсолютными частотами xi | ni
#сколько раз встречается каждый элемент
def varRyad(listN):
    dct = dict()
    for i in listN:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1
    print "k=", len(dct)
    for i in sorted(dct):
        print i, " : " , dct[i]
    print 
    return dct


#полигон xi | wi=ni/n    
def poligon(listN):
    dct = varRyad(listN)
    for i in dct:
        dct[i] = dct[i]/float(len(listN))

    for i in sorted(dct):
        print i, " : " , dct[i]



#интервальный вариационный ряд
#данные для построения гистограммы
#i, int, ni, wi, ni/h
def gistogramma(listN, n):
    inter=interval(listN, n)
    ni = []
    wi = []
    pi = []
    x = []
    h = (max(listN) - min(listN))/n 
    for i in inter:
        nii = 0
        for l in listN:
            if (l > i[0]) and (l <= i[1]):
                 nii+=1
            if i == inter[0] and l == min(listN):
                nii+=1

        ni.append(nii)
        wi.append(nii/100.00)
        pi.append(nii/float(h))
        x.append((i[0]+i[1])/2)

    listGist = []
    # print "h =", h
    for i in range(n):
        # print i, inter[i], ni[i], round(wi[i], 4), round(pi[i],4), round(x[i],4)
        listGist.append((i, inter[i], ni[i], round(wi[i], 4), round(pi[i],4), round(x[i],4)))
    return listGist

        
#Эксцесс
def excess(listN):
    Mo = viborSred(listN)
    chisl = 0
    for i in listN:
        ras = (i - Mo)
        chisl += ras**4
    res = chisl/float(len(listN))
    res = res/(dispersia2(listN)*dispersia2(listN))
    res = res-3
    print res


#асимметрия
def asimm(listN):
    Mo = viborSred(listN)
    chisl = 0
    for i in listN:
        ras = (i - Mo)
        chisl += ras**3
    res = chisl/float(len(listN))
    s = math.sqrt(dispersia2(listN))
    res = res/s**3
    print res, "s**3=", s**3


#интервальная оценка номер 1
def intOcenka1(listN):
    xv = viborSred(listN)
    t = 1.96
    q = math.sqrt(dispersia2(listN))
    n = float(len(listN))
    a1 = xv - t*(q/math.sqrt(n))
    a2 = xv + t*(q/math.sqrt(n))

    print "xv = ", xv
    print "t = ", t
    print "q = ", q
    print "n = ", n
    print "a1 = ", a1
    print "a2 = ", a2
    print
    print


#интервальная оценка номер 1
def intOcenka2(listN):
    xv = viborSred(listN)
    n = 100
    q = 0.143
    
    chisl = 0
    for i in listN:
        chisl += (i - xv)*(i - xv)
    s = math.sqrt(chisl/(n-1))

    a1 = s*(1-q)
    a2 = s*(1+q)
    
    print "xv = ", xv
    print "q = ", q
    print "n = ", n
    print "s = ", s
    print "a1 = ", a1
    print "a2 = ", a2
# Проверка гипотезы по критерию порсона
def checkHypo(inter, n):
    PRINT = False
    finalint = interval(inter,n)
    print("ПЕРВЫЙ ШАГ:")
    sigma = 0
    x_srednee = 0
    listX_ish = []
    for xs in finalint:
        xi = xs[0]
        x_i_1 = xs[1]
        xi_sh = (xi+x_i_1)/2
        listX_ish.append(xi_sh)
        x_srednee += xi_sh
        # xi_sh = round(xi_sh,2)
        print("Xi={}    Xi+1={}     Xi*={}"\
              .format(round(xi,2),round(x_i_1,2),round(xi_sh,2)))
    x_srednee /= n
    print("X* среднее={}".format(round(x_srednee,2)))
    for i in listX_ish:
        sigma += pow (i - x_srednee,2)
    sigma /= n
    print("Сигма*={}".format(round(sigma,2)))

    print("ВТОРОЙ ШАГ:")
    print("найдем интервалы zi и zi + 1 и функции F(zi) и F(zi+1)")

    # Словарь значений функции Лапласа из Приложения 2
    dictLaplas = makeLaplas()
    listF = []
    for xs in finalint:
        xi = xs[0]
        x_i_1 = xs[1]
        # pre_zi = xi - x_srednee
        # pre_zi_1 = x_i_1 - x_srednee
        # print(round(pre_zi,2), round(pre_zi_1,2))
        zi = round ((xi - x_srednee)/sigma,2)
        z_i_1 = round((x_i_1 - x_srednee)/sigma,2)
        print("Zi={}    Zi+1={}".format(zi,z_i_1)),
        # print(sorted(dictLaplas))
        # print(ziIsInFi(abs(zi),dictLaplas))
        if zi < 0:
            F_zi = - getFzi(abs(zi),dictLaplas)
        else:
            F_zi = getFzi(abs(zi),dictLaplas)

        if z_i_1 < 0:
            F_zi_1 = - getFzi(abs(z_i_1),dictLaplas)
        else:
            F_zi_1 = getFzi(abs(z_i_1),dictLaplas)

        F_zi = round(F_zi,2)
        F_zi_1 = round(F_zi_1,2)

        listF.append((F_zi,F_zi_1))

        if F_zi != None:
            print("    F_zi={}".format(F_zi)),
        else:
            print("    ERROR!")

        if F_zi_1 != None:
            print("    F_zi+1={}".format(F_zi_1))
        else:
            print("    ERROR!")

    print("ТРЕТИЙ ШАГ:")
    print("найдем теоретические вероятности P_i\n"\
          " и теоретический частоты n'_i = n * P_i = 100 * P_i")
    # print(listF)
    # Считаем Pi
    listPi =[]
    sumPi = 0
    for F in listF:
        Pi = F[1] - F[0]
        sumPi+=Pi
        Pi = round(Pi,2)
        print(Pi)
        listPi.append(Pi)
    # print(listPi)
    print("Сумма Pi={}".format(sumPi))
    print("Считаем n'_i")
    listN_sh_i = []
    sumN_sh_i =0
    for p_i in listPi:
        n_sh_i = 100 * p_i
        sumN_sh_i += n_sh_i
        print(n_sh_i)
        listN_sh_i.append(n_sh_i)
    print("Сумма N_i={}".format(sumN_sh_i))
    print("НАКОНЕЦТО ШАГ4!")
    print("Найдём Хи^2 наблюдаемое")

    spisok = gistogramma(listNumber,n)
    # print(spisok)
    # Берем ni
    i1 = 0
    # Так как у нас 100 элементов в выборке
    hi_kvedrat_nabl = -100
    proverka = 0
    print("6    8")
    for sp in spisok:
        ni = sp[2]
        # print(ni)
        n_sh_i = listN_sh_i[i1]
        # СТРАНИЦА 257 УЧЕБНИКА, ТАБЛИЦА 23 СТОЛБЦЫ 6 И 8
        shesht = pow((ni - n_sh_i),2)/n_sh_i

        vosem = pow((ni),2)/n_sh_i
        hi_kvedrat_nabl += vosem

        proverka += shesht
        print("{}    {}".format(shesht,vosem))
        i1+=1
    print("Хи квадрат ровно={}    Проверка={}".format(hi_kvedrat_nabl,proverka))
    hi_krit = 9.5
    print("Хи критичексое равно={} (на стр257 в учебнике, или найти самим по приложению 5)".format(hi_krit))
    print("Проверяем гипотезы, ответ: "),
    if hi_kvedrat_nabl > hi_krit:
        print("данные наблюдений НЕ СОГЛАСУЮТСЯ с гипотезой о нормальном распределении генеральной совокупности.")
        print("Так как Хи.квадрат.наблюдаемое БОЛЬШЕ Хи.квадрат.критического, гипотеза о нормальном распределении генеральной совокупности ОТВЕРГАЕТСЯ")
    elif hi_kvedrat_nabl < hi_krit:
        print("данные наблюдений СОГЛАСУЮТСЯ с гипотезой о нормальном распределении генеральной совокупности.")
        print("Так как Хи.квадрат.наблюдаемое МЕНЬШЕ Хи.квадрат.критического, гипотеза о нормальном распределении генеральной совокупности ПРИНИМАЕТСЯ")




if __name__ == "__main__":
    #получаем список значений
    dictLaplas = makeLaplas()
    
    #данные для построения полигона
    poligon(listNumber)
    
    #данные для построения гисторгаммы
    #интервальный вариационный ряд
    # gistogramma(listNumber, 7)

    #выборочное среднее
    #print viborSred(listNumber)

    #дисперсия
    #print dispersia2(listNumber)

    #выриационный ряд
    # varRyad(listNumber)

    #эксцесс
    # excess(listNumber)

    #асимметрия
    # asimm(listNumber)

    intOcenka1(listNumber)
    intOcenka2(listNumber)
    # checkHypo(listNumber,7)
    # F_zi = getFzi(3.4,dictLaplas)
    # print(F_zi)
    # F_zi = - F_zi
    # print(F_zi)
    # print getRawZi(2.44,dictLaplas)