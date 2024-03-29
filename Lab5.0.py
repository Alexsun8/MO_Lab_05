import copy
from math import *
import random
import matplotlib.pyplot as plt


def FormA(r):
    M = floor((r - 1) / 2)
    a = [0] * r
    sum_a = 0
    sum_s = 0
    a[M] = random.uniform(0, 1)
    sum_a += a[M]
    sum_s += a[M]
    for m in range(M - 1, 0, -1):
        a[m] = 0.5 * random.uniform(0, 1 - sum_s)
        sum_s += a[m]
        a[r - 1 - m] = a[m]
        sum_a += 2 * a[m]
    a[0] = 0.5 * (1 - a[M])
    a[r - 1] = 0.5 * (1 - a[M])
    sum_a += 2 * a[0]
    for l in range(r):
        a[l] /= sum_a
    return a;


def FormFAv(r, K, f_real, a):
    f_av = []
    M = floor((r - 1) / 2)
    for k in range(M, K - M + 1):
        # f_av.append(0)
        sum = 0
        for j in range(k - M, k + M + 1):
            # f_av[k-M] += f_real[j] * a[j + M + 1 - k]
            sum += f_real[j] * a[j + M - k]
        f_av.append(sum)
    return f_av


def WO(r, K, f_av, f_real):
    M = floor((r - 1) / 2)
    w_list = []
    o_list = []
    o_list.append(abs(f_av[0] - f_real[0]))
    for i in range(1, K - M - 1):
        w_list.append(abs(f_av[i] - f_av[i - 1]))
        o_list.append(abs(f_av[i] - f_real[i]))
    w = max(w_list)
    o = max(o_list)
    w_o = [w, o]
    return w_o


def countAlfa(r, K, f_real):
    a = FormA(r)
    f_av = FormFAv(r, K, f_real, a)
    w_o = WO(r, K, f_av, f_real)
    w_o_a = []
    w_o_a.append(w_o[0])
    w_o_a.append(w_o[1])
    w_o_a.append(a)
    w_o_a.append(f_av)
    return w_o_a


def main():
    x_min = 0
    x_max = pi
    K = 100
    A = 0.25
    r = 3
    e = 0.01
    P = 0.95
    x = []
    f = []
    f_real = []
    noise = []
    L = 10
    M = floor((r - 1) / 2)
    print("%-3s%7s%7s%7s%7s" % ("k", "x", "f", "noise", "f_real"))
    for k in range(K + 1):
        x.append(x_min + k * (x_max - x_min) / K)
        f.append(sin(x[k]) + 2 * A)
        noise.append(random.uniform(-A, A))
        f_real.append(f[k] + noise[k])
        print("%-3d%7.3f%7.3f%7.3f%7.3f" % (k, x[k], f[k], noise[k], f_real[k]))
    print("  ")
    info_min = []
    dmin = 8
    lambda_min = 8
    N = floor(log(1 - P) / log(1 - e / (x_max - x_min)))
    plt.title("Омега-Дельта")
    for l in range(L + 1):
        lam = l / L
        print("Для Лямбда = ", lam)
        w_o_a = countAlfa(r, K, copy.deepcopy(f_real))
        for i in range(0, N):
            # dist = max(lam * w_o_a[0], (1 - lam) * w_o_a[1])
            dist = max(w_o_a[0], w_o_a[1])
            if i == 0:
                dist_min = dist
                w_o_a_min = w_o_a
            else:
                if dist < dist_min:
                    dist_min = dist
                    w_o_a_min = w_o_a
        print("J( ", w_o_a_min[0], "; ", w_o_a_min[1], ") = ", lam * w_o_a_min[0] + (1 - lam) * w_o_a_min[1])
        print("dist =  ", dist_min)
        plt.plot(w_o_a_min[0], w_o_a_min[1], linestyle=":", marker='o', label=lam)
        if l == 0:
            info_min = w_o_a_min
            dmin = dist_min
            lambda_min = l / L
        else:
            if dist_min < dmin:
                info_min = w_o_a_min
                dmin = dist_min
                lambda_min = l / L

    plt.legend(loc='upper left')
    plt.savefig('/home/alexsun8/MO/lab5/w-del1_r3.png', format='png')
    plt.show()
    plt.plot(range(0, K + 1), f_real, color='g', label="f_real")
    plt.plot(range(0, K + 1), f, color='b', label="f_ideal")
    if r == 5:
        plt.plot(range(K - M - 1), info_min[3], color='r', label="result")
    if r == 3:
        plt.plot(range(K - M), info_min[3], color='r', label="result")
    plt.savefig('/home/alexsun8/MO/lab5/plot1_r3.png', format='png')
    plt.legend(loc='upper left')
    plt.show()
    plt.title("Noise")
    plt.plot(x, noise, color='y')
    plt.savefig('/home/alexsun8/MO/lab5/noise1_r3.png', format='png')
    plt.show()
    print("   ")
    print("   ")
    print("   ")
    print("Результат")
    print("J = ", lambda_min * info_min[0] + (1 - lambda_min) * info_min[1])
    print("w = ", info_min[0])
    print("o = ", info_min[1])
    print("alfa = ", info_min[2])
    print("lambda = ", lambda_min)


main()
