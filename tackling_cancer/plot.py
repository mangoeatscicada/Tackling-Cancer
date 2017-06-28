import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, mpld3

def plotfunc (sometuple):
    plt.rcParams["font.family"] = "Comic Sans MS"
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.canvas.set_window_title('Cancer Chart')

    blood = sometuple[0]
    cancer = sometuple[1]
    other = sometuple[2]

    slices = [blood, cancer, other]
    activities = ['Blood', 'Cancer', 'Other']
    cols = ['r', 'm', '#D3D3D3']

    plt.pie(slices, labels=activities, colors = cols, startangle=90, shadow = True, explode=(0,0.15,0), autopct='%1.1f%%')
    plt.title('Cancer Chart')
    plt.savefig('../static/images/piechart3.jpg')

def plotfunc0(sometuple):
    fig = plt.figure(figsize=5)
    fig.patch.set_facecolor('white')
    fig.canvas.set_window_title('Cancer Chart')
    blood = sometuple[0]
    cancer = sometuple[1]
    other = sometuple[2]
    slices = [blood,cancer,other]
    activities = ['Blood', 'Cancer', 'Other']
    cols = ['r', 'm', '#D3D3D3']
    plt.pie(slices, labels=activities, colors = cols, startangle=90, autopct='%1.1f%%')
    plt.axis('off')
    plt.title('Cancer Chart', color='r')
    mpld3.show()
    
    

plotfunc0((1,2,3))