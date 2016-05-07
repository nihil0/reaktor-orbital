#!/usr/bin/env python3

'''
Reaktor Orbital Challenge

A script to find a routing path for a message between two points on earth
using a network of satellites.

:Date: 04.05.2016
:Author: Neelabh Kashyap

'''
from math import cos,sin,pi,sqrt

earth_radius = 6371

class Satellite:
    '''
    Satellite orbiting earth

    '''
    def __init__(self,name,lat,lon,h):

        self.name = name

        # distance from centre of earth
        self.r = h+earth_radius

        # Convert angles to radians
        theta = (pi/180)*lat
        phi = (pi/180)*lon

        # Position in Cartesian coordinates
        self.x = (earth_radius+h)*cos(theta)*cos(phi)
        self.y = (earth_radius+h)*cos(theta)*sin(phi)
        self.z = (earth_radius+h)*sin(theta)

def distance(sat1,sat2):
    '''
    Distance between two satellites
    '''
    return sqrt( (sat2.x-sat1.x)**2 +  (sat2.y-sat1.y)**2 +
            (sat2.z-sat1.z)**2 )

def is_visible(sat1,sat2):
    '''
    Check if line of sight link exists between sats 1 and 2. Returns TRUE if yes
    and FALSE if no.
    '''
    dist = distance(sat1,sat2)

    # height of triangle formed by sat1, sat2 and centre of earth.
    p = sqrt( sat1.r**2 - ((dist**2 + sat1.r**2 - sat2.r**2)/(2*dist))**2)

    return p > earth_radius

def read_sat_position(position_str):
    '''
    Returns a Satellite object. Takes a formatted input string as input.
    See challenge details for input format.

    TODO: Sanitize input strings.

    '''
    var = [float(m) if m[0:3] != 'SAT' else m for m in position_str.split(',')]
    return Satellite(*var)

def parse_route(route_str):
    '''
    Returns a dictionary with information about the source and destination
    '''
    endpoints=[float(m) for m in route_str.split(',')[1:]]

    endpoint_dict = {'src':{
        'lat':endpoints[0],
        'lon':endpoints[1]
        },
        'dst':{
            'lat':endpoints[2],
            'lon':endpoints[3]
            }
        }

    return(endpoint_dict)


if __name__== '__main__':

    with open('data.txt','r') as f:
        # Skip first line
        f.readline()

        # Create list of Satellite objects
        sat_constellation = list()
        sat_constellation = [read_sat_position(line) for line in f if line[0]!='R']

    print(sat_constellation)

