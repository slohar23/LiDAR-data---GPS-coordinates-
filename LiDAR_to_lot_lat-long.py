
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 15:31:54 2021

@author: shreyalohar
"""

import pandas as pd
import numpy as np
import sys
import os
import utm

## Read in excel file and get heading, pos_x as numpy arrays:
# note: change file path and name:
# df = pd.read_excel ('/Users/shreyalohar/Desktop/pythonprac/park_garage/lat_long.xlsx')
df = pd.read_csv ('/Users/shreyalohar/Desktop/Final_project/ERR4.csv')
# heading = pd.DataFrame(df, columns = ['heading']).to_numpy()
# dist = pd.DataFrame(df, columns = ['dist']).to_numpy()

# Get objects XYZ points in LIDAR frame
pos_x = pd.DataFrame(df, columns = ['position_x']).values
pos_y = pd.DataFrame(df, columns = ['position_y']).values
#pos_z = pd.DataFrame(df, columns = ['position_z']).values

xy_pts_lidar = np.concatenate((pos_x.T, pos_y.T), axis= 0)

print ("Shape of xy_lidar pts is: ", xy_pts_lidar.shape)

## Define constants:
R = 6378 #Radius of the Earth
lat_origin =  35.307961   # Current lat point in degrees
lon_origin = -80.732167   # Current long point in degrees

heading_lidar = np.radians(170)    # North is +90 deg, East is 0 deg

## Rotation matrix - LIDAR to UTM frame: 
R_l2u = np.matrix([[np.cos(heading_lidar) , -np.sin(heading_lidar)], 
                   [np.sin(heading_lidar) ,  np.cos(heading_lidar)]])


## Convert LIDAR origin to UTM frame: 
origin_utm = utm.from_latlon(lat_origin, lon_origin)

print (" UTM origin is: ( ", origin_utm[0] , " , ", origin_utm[1], " )")

## Rotate object points into UTM frame
xy_pts_utm = np.matmul(R_l2u, xy_pts_lidar)  + np.matrix([[origin_utm[0]], [origin_utm[1]]])

num_points = xy_pts_utm.shape[1]


## Convert XY pts from UTM to lat-lon: 
lat_out = np.zeros(num_points)
lon_out = np.zeros(num_points)

for i in range(0, num_points):
    lat_lon = utm.to_latlon(xy_pts_utm[0, i], xy_pts_utm[1, i], origin_utm[2], origin_utm[3])
    lat_out[i] = lat_lon[0]
    lon_out[i] = lat_lon[1]


## Add lat2 and lon2 to the data frame:
df['lat_out'] = np.squeeze(lat_out)
df['lon_out'] = np.squeeze(lon_out)

## Write to excel file:
df.to_csv('Parking_lot_error4.csv')




######################## OLD CODE ##########################################
# ## Calculate lat2 and lon2:
# lat2 = np.degrees(np.arcsin(np.sin(lat1) * np.cos(pos_x/R) + np.cos(lat1) * np.sin(pos_x/R) * np.cos(heading)))

# lon2 = np.degrees(lon1 +  np.arctan2( np.sin(heading) * np.sin(pos_x/R) * np.cos(lat1), np.cos(pos_x/R) - np.sin(lat1) * np.sin(lat2)))

# ## Add lat2 and lon2 to the data frame:
# df['lat2'] = np.squeeze(lat2)
# df['lon2'] = np.squeeze(lon2)

# ## Write to excel file:
# df.to_excel('lat_long_new.xls')


## Old code for ref:

#lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
             #math.cos(lat1)*math.sin(d/R)*math.cos(brng))

#lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                     #math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
#lat2 = math.degrees(lat2)
#lon2 = math.degrees(lon2)

# df['lat2'] = np.degrees(np.arcsin(np.sin(lat1)*np.cos(df['dx']/R) + np.cos(lat1)*np.sin(df['dx']/R)*np.cos(df['heading_rad'])))
# df['lat2'].astype(float)
# df['lon2'] = np.degrees(lon1 + np.arctan(np.sin(df['heading_rad'])*np.sin(df['dx']/R)*np.cos(lat1),np.cos(df['dx']/R)-np.sin(lat1)*np.sin(df['lat2'])))


