import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BBox = (-6.1898, -5.9724, 37.3748, 37.5829)

df = pd.DataFrame()

df["longitude"] = 0

df["latitude"] = 0

df.loc[0,"longitude"] = -6.189

df.loc[0,"latitude"] = 37.38

df.loc[1,"longitude"] = -6.1

df.loc[1,"latitude"] = 37.41

print (df)
ruh_m = plt.imread('C:/GitHub/TFG-TriTruth/src_W10/base.png')
                   
fig, ax = plt.subplots(figsize = (20,20))

ax.scatter(df.longitude, df.latitude, zorder=1, alpha= 0.9, c='b', s=100)

ax.set_xlim(BBox[0],BBox[1])

ax.set_ylim(BBox[2],BBox[3])

ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')

fig.savefig('C:/GitHub/TFG-TriTruth/src_W10/base2.png')