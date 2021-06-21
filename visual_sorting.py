import matplotlib; matplotlib.use("TkAgg")          # To be added while running in PyCharm
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Below is a helper class to make things easier while performing the sort operation on arr object.
# __len__, __getitem__ and __setitem__ are the magic methods which gets called internally during array operations.
class TrackedArray():
    def __init__(self, arr):
        self.arr = np.copy(arr)
        self.reset()

    def reset(self):
        self.indices = []
        self.values = []
        self.access_type = []       # to contain the access types i.e. get or set
        self.full_copies = []       # To create a copy(snapshot) on every array modification

    def track(self,key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))

    def GetActivity(self, idx = None):
        if (isinstance(idx, type(None))):
            return [(i,op) for (i,op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[idx], self.access_type[idx])

    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        self.arr.__setitem__(key,value)
        self.track(key, "set")

    def __len__(self):
        return self.arr.__len__()
        

plt.rcParams["figure.figsize"] = (12,8)
plt.rcParams["font.size"] = 16

N = 30
FPS = 60.0


arr = np.round(np.linspace(0,1000,N),0)
np.random.seed(0)
np.random.shuffle(arr)
arr = TrackedArray(arr)


# We don't have to display the Unsorted first then Sorted, So I am disabling 1st plot.
# fig, ax = plt.subplots()
# ax.bar(np.arange(0,len(arr),1),arr, align="edge", width=0.8)
# ax.set_xlim([0,N])
# ax.set(xlabel="Index",ylabel="Value",title="Unsorted Array")
"""
##################################
######## DEMO 1 - Insertion Sort
################################
t0 = time.perf_counter()
sorter = "Insertion"
i = 1
while i < len(arr):
    j = i
    while j > 0 and arr[j-1] > arr[j]:
        arr[j],arr[j-1] = arr[j-1],arr[j]
        j = j - 1
    i = i + 1
dt = time.perf_counter() - t0
##################################
print(f"----------- {sorter} Sort ----------")
print(f" Array was sorted in {dt*1E3:.1f} ms")
"""
##################################
######## DEMO 2 - Quick Sort
################################
sorter = "Quick"
def quicksort(A, lo, hi):
    if lo < hi :
        p = partition(A, lo, hi)
        quicksort(A, lo, p - 1)
        quicksort(A, p + 1, hi)

def partition(A, lo, hi):
    pivot = A[hi]
    i = lo
    for j in range(lo,hi):
        if A[j] < pivot:
            A[i],A[j] = A[j],A[i]
            i = i + 1
    A[i],A[hi] = A[hi],A[i]
    return i

t0 = time.perf_counter()
quicksort(arr, 0, len(arr)-1)
dt = time.perf_counter() - t0
##################################
print(f"----------- {sorter} Sort ----------")
print(f" Array was sorted in {dt*1E3:.1f} ms")

fig, ax = plt.subplots(figsize=(16, 8))
container = ax.bar(np.arange(0,len(arr),1),arr, align="edge", width=0.8)
# fig.suptitle(f"{sorter} sort")
ax.set_xlim([0,N])
ax.set(xlabel="Index",ylabel="Value",title=f"{sorter} sort")
txt = ax.text(0.01, 0.99, "", ha="left", va="top", transform=ax.transAxes)

def update(frame):
    for (rectangle, height) in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("#850f34")
    idx, op = arr.GetActivity(frame)
    if op=="get":
        container.patches[idx].set_color("#7ffc03")
    elif op=="set":
        container.patches[idx].set_color("#4ae8d8")
    # fig.savefig(f"frames/{sorter}_frame{frame:05.0f}.png")    # In order to save the snapshot at each operation
    return (*container,txt)         # these changes will be returned to fig animation every framee.

# Below function takes "fig" object for plotting, and calls the update function with the frames ranging from 0 to length of arr, in an interval of 1000/60 frames per second. Repetition has been set to False intensionally.
ani = FuncAnimation(fig, func=update, frames=range(len(arr.full_copies)), blit=True, interval=1000./FPS, repeat=False)
plt.show()          # This line is added for running in PyCharm only