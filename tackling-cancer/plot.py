import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Comic Sans MS"
fig = plt.figure()
fig.patch.set_facecolor('white')
fig.canvas.set_window_title('Cancer Chart')

blood = 1
cancer = 3
other = 1

slices = [blood, cancer, other]
activities = ['Blood', 'Cancer', 'Other']
cols = ['r', 'm', '#D3D3D3']

plt.pie(slices, labels=activities, colors = cols, startangle=90, shadow = True, explode=(0,0.15,0), autopct='%1.1f%%')
plt.title('Cancer Chart')
plt.show()