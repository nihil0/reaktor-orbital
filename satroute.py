#!/usr/bin/env python3

'''
Reaktor Orbital Challenge

A script to find a routing path for a message between two points on earth
using a network of satellites.

:Date: 04.05.2016
:Author: Neelabh Kashyap

'''
from math import cos,sin,pi

earth_radius = 6371

class Satellite:
    '''
    Satellite orbiting earth

    '''
    def __init__(self,name,h,lat,lon):

        self.name = name

        # Convert angles to radians
        theta = (pi/180)*lat
        phi = (pi/180)*lon

        # Position in Cartesian coordinates
        self.x = (earth_radius+h)*cos(theta)*cos(phi)
        self.y = (earth_radius+h)*cos(theta)*sin(phi)
        self.z = (earth_radius+h)*sin(theta)



if __name__== '__main__':
    print('boo')
