from Network import BAModel
import numpy as np
import logbin230119 as lb
import matplotlib.pyplot as plt
import pickle
from scipy import stats
'''
Generate data'''
def generate_data_repeatall_fix_points():
    times = 5
    m = [1,2,3,4,5,6]
    initial = 16
    add_points = 100000

    for i in m:
        print(i)
        t = 0
        k = []
        for j in range(times):
            print(t)
            t += 1
            model = BAModel(initial,add_points, i)
            model.add_points()
            k.extend(model.degrees)

        f = open("m=%d,init=20,add=100000,repeat5.txt" %(i),"wb")
        pickle.dump(k,f)
        f.close()
# generate_data_repeatall_fix_points()

def generate_data_repeat_k():
    times = 15
    m = 6
    initial = 16
    add_points = [100, 1000, 10000, 100000]
    for pt in add_points:
        print(pt)
        k_max = []
        t = 0
        for i in range(times):
            print(t)
            t += 1
            model = BAModel(initial, pt, m)
            model.add_points()
            k_max.append(max(model.degrees))

        f = open("m=6,init=20,add=%d,kmax.txt" %(pt),"wb")
        pickle.dump(k_max,f)
        f.close()
# generate_data_repeat_k()


def generate_data_k6():
    times = 15
    m = 6
    initial = 16
    add_points = [100, 1000, 10000, 100000]
    for pt in add_points:
        print(pt)
        k = []
        for j in range(times):
            model = BAModel(initial,pt, m)
            model.add_points()
            k.append(model.degrees)
        f = open("m=6,init=16,add=%d,k8,Ldiff.txt" %(pt),"wb")
        pickle.dump(k,f)
        f.close()
# generate_data_k6()


'''
----------------------------------------------------------------------------
Data analyse
'''

def plot_figure_binned():    # plot binned figure
    m = [1,2,3,4,5,6]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for m_val in m:
        val = pickle.load(open("m=%d,init=20,add=100000,repeat5.txt"%(m_val), "rb"))
        print(len(val))
        x, y = lb.logbin(np.array(val), scale=1.25, zeros=False)
        x_un, y_un = lb.logbin(np.array(val), scale=1, zeros=False)
        plt.loglog(x, y,'-', label='m = %d'%(m_val))
    x1 = np.linspace(1,max(x),500)
    y1 = 1/x1**3
    plt.loglog(x1, y1, '--',label=r'$p(k)\propto k^{-3}$')
    plt.legend()
    plt.xlabel('Degree k', fontsize=13)
    plt.ylabel('Probability of degree P(k)', fontsize=13)
    plt.show()
# plot_figure_binned()

def plot_figure_unbinned():   # plot unbinned figure
    m = [1, 2, 3, 4, 5, 6]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for m_val in m:
        val = pickle.load(open("m=%d,init=20,add=100000,repeat5.txt" % (m_val), "rb"))
        x_un, y_un = lb.logbin(np.array(val), scale=1, zeros=False)
        plt.loglog(x_un, y_un, '.', label='m = %d' % (m_val))
    plt.legend()
    plt.xlabel('Degree k', fontsize=13)
    plt.ylabel('Probability of degree P(k)', fontsize=13)
    plt.show()
# plot_figure_unbinned()

def p_k(m,k):
    return (2*m*(m+1))/(k*(k+1)*(k+2))

def plot_theory():
    m = [1,2,3,4,5,6]
    for m_val in m:
        y_theory = []
        val = pickle.load(open("m=%d,init=20,add=100000,repeat5.txt"%(m_val), "rb"))
        x, y = lb.logbin(np.array(val), scale=1.25, zeros=False)
        x_un, y_un = lb.logbin(np.array(val), scale=1, zeros=False)
        x_theory = np.logspace(min(x),max(x),200)
        for i in x:
            y_theory.append(p_k(m_val,i))
        D, p_val = stats.ks_2samp(y_theory, y)
        print(D,p_val)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect(aspect=0.2)

        plt.loglog(x_un, y_un, '.', label='Unbinned data, m = %d' % (m_val))
        plt.loglog(x, y, '--', label='Binned data, m = %d' % (m_val))
        plt.loglog(x, y_theory, '-', label=r'Theoretical plot'+'\n'+r'$D$ = %.4f, $p-value$ = %.4g'%(D,p_val))

        plt.xlabel('Degree k', fontsize=13)
        plt.ylabel('Probability of degree P(k)', fontsize=13)
        plt.legend()
        plt.show()
# plot_theory()


k_mean_list = []
k_std_mean = []
for i in [100,1000,10000,100000]:
    k = pickle.load(open("m=6,init=20,add=%d,kmax.txt"%(i),"rb"))
    k_mean_list.append(np.mean(k))
    k_std_mean.append(np.std(k))


def analyse_maxk():
    x = [100, 1000, 10000, 100000]
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(np.array(x)), np.log10(k_mean_list))
    print(slope,intercept,std_err)
    x1 = np.linspace(90,110000)
    y1 = 10**(slope * np.log10(x1) + intercept)
    fig, ax = plt.subplots()
    ax.errorbar(x, k_mean_list,yerr=k_std_mean,fmt='.',label = 'Largest degree k with error bar')
    ax.plot(x1,y1, label=r'Linear fit with slope = $ %.3f \pm %.3f $'%(slope,std_err))
    ax.set_xlabel('Number of nodes N',fontsize=13)
    ax.set_ylabel('Largest degree k1',fontsize=13)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.legend()
    plt.show()
# analyse_maxk()

def plot_k6():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for i in range(4):
        l = [100,1000,10000,100000]
        k = pickle.load(open("m=6,init=16,add=%d,k8,Ldiff.txt" %(l[i]), "rb"))[0]
        x, y = lb.logbin(np.array(k), scale=1.19, zeros=False)
        yl = (2*6*7)/(np.array(x)*(np.array(x)+1)*(np.array(x)+2))
        y_new = np.array(y)/yl
        x_new = np.array(x)/k_mean_list[i]
        ax.plot(x,y,'o',label='N = %d'%(l[i]))
        ax.plot(x, y, '-', label='N = %d' % (l[i]))
        # ax.plot(x_new,y_new,label='N = %d'%(l[i]))
        ax.set_xlabel(r'Degree $k$',fontsize=13)
        ax.set_ylabel(r'Probability of degree $p(k)$',fontsize=13 )
        ax.set_xscale('log')
        ax.set_yscale('log')
        plt.legend()
    plt.show()
plot_k6()
