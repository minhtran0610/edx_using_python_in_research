# 4.2.2. Simple data visualizations
import pandas as pd
import matplotlib.pyplot as plt
birddata = pd.read_csv("bird_tracking.csv")
bird_names = pd.unique(birddata.bird_name)
plt.figure(figsize=(7,7))
for bird_name in bird_names:
    ix = birddata.bird_name == bird_name
    x,y = birddata.longitude[ix], birddata.latitude[ix]
    plt.plot(x,y,".", label = bird_name)
plt.xlabel("Longtitude")
plt.ylabel("Latitube")
plt.legend(loc="lower right")
plt.savefig("3traj.pdf")


# 4.2.3. Examining flight speed
import numpy as np
ix = birddata.bird_name == 'Eric'
speed = birddata.speed_2d[ix]
ind = np.isnan(speed)
plt.hist(speed[~ind])
plt.savefig("hist.pdf")

plt.figure(figsize=(8,4))
speed = birddata.speed_2d[birddata.bird_name == 'Eric']
ind = np.isnan(speed)
plt.hist(speed[~ind], bins=np.linspace(0,30,20), normed=True)
plt.xlabel("2D speed (m/s)")
plt.ylabel("Frequency")

birddata.speed_2d.plot(kind='hist', range=[0,30])
plt.xlabel("2D speed (m/s)")
plt.ylabel("Frequency")


# 4.2.4. Using datetime
import datetime
timestamps = []
for k in range(len(birddata)):
    timestamps.append(datetime.datetime.strptime(birddata.date_time.iloc[k][:-3], "%Y-%m-%d %H:%M:%S"))

birddata["timestamp"] = pd.Series(timestamps, index = birddata.index)

data = birddata[birddata.bird_name== "Eric"]
times = data.timestamp
elapsed_time = [time - times[0] for time in times]
elapsed_day = np.array(elapsed_time) / datetime.timedelta(days=1)

plt.plot(np.array(elapsed_time) / datetime.timedelta(days=1))
plt.xlabel('Observation')
plt.ylabel('Elapsed time (days)')
plt.savefig("timeplot.pdf")


# 4.2.5. Calculating mean speed
data = birddata[birddata.bird_name== "Eric"]
times = data.timestamp
elapsed_time = [time - times[0] for time in times]
elapsed_day = np.array(elapsed_time) / datetime.timedelta(days=1)

next_day = 1
inds = []
daily_mean_speed = []
for (i,t) in enumerate(elapsed_day):
    if t < next_day:
        inds.append(i)
    else:
        # compute mean speed
        daily_mean_speed.append(np.mean(data.speed_2d[inds]))
        next_day += 1
        inds = []

plt.figure(figsize=(8,6))
plt.plot(daily_mean_speed)
plt.xlabel("Day")
plt.ylabel("Mean speed (m/s)")
plt.savefig("dms.pdf")


# 4.2.6. Using the Cartopy library
import cartopy.crs as ccrs
import cartopy.feature as cfeature

proj = ccrs.Mercator()

plt.figure(figsize=(10,10))
ax = plt.axes(projection = proj)
ax.set_extent((-25.0, 20.0, 52.0, 10.0 ))
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.RIVERS)

for name in bird_names:
    ix = birddata.bird_name == name
    x,y = birddata.longitude[ix], birddata.latitude[ix]
    ax.plot(x, y, '.', transform = ccrs.Geodetic(), label = name)

plt.legend(loc = "upper left")
plt.savefig("map.pdf")