#!/usr/bin/env python3

'''
Reaktor Orbital Challenge

A script to find a routing path for a message between two points on earth
using a network of satellites.

:Date: 04.05.2016
:Author: Neelabh Kashyap

'''
from math import cos,sin,pi,sqrt,asin
import networkx as nx

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

    endpoint_dict = {
        'src':{
            'lat':endpoints[0],
            'lon':endpoints[1]
        },
        'dst':{
            'lat':endpoints[2],
            'lon':endpoints[3]
            }
        }

    return(endpoint_dict)

def find_nearest(sat_list,sat):
    '''
    Returns the ID of the nearest satellite to sat in list of Satellite objects
    '''
    distances = [distance(sat,m) for m in sat_list]

    return(sat_list[distances.index(min(distances))].name)

def visible_sats(sat_list,sat):
    '''
    Returns logical list indicating visible satellites from sat
    '''
    #return(list(filter(lambda x:is_visible(sat,x),sat_list)))
    return([is_visible(sat,m) for m in sat_list if m.name != sat.name])

def sat_angle(ground_point,sat):
    '''
    Returns the angle between the tangent at ground_point and sat
    '''
    if round(abs(ground_point.r-earth_radius),4) != 0:
        raise ValueError('Ground point is not on the ground!')

    d = distance(ground_point,sat)

    return (180/pi)*(asin((sat.r**2 - d**2 - earth_radius**2)/(2*d*earth_radius)))

def udlink(sat_list,ground_point):
    '''
    Returns the name of the satellite which will be the entry/exit node given
    a point on the earth. This is the closest satellite to which line-of-sight
    transmission is possible.
    '''
    if round(abs(ground_point.r-earth_radius),4) != 0:
        raise ValueError('Ground point is not on the ground!')

    visible_sats = [m for m in sat_list if sat_angle(ground_point,m)>=0]

    return find_nearest(visible_sats,ground_point)

def build_graph(sat_constellation):
    '''
    Returns a NetworkX graph representing the connectivity between the various
    satellites in the constellation.
    '''
    sat_graph = nx.Graph()

    nodes = list(sat_constellation.keys())
    sat_graph.add_nodes_from(nodes)

    for ii in range(len(nodes)):
        for kk in range((ii+1),len(nodes)):
            if is_visible(sat_constellation[nodes[ii]],sat_constellation[nodes[kk]]):
                sat_graph.add_edge(nodes[ii],nodes[kk])


    return sat_graph
if __name__== '__main__':
    # Read data file
    with open('data.txt','r') as f:
        # Skip first line
        f.readline()

        lines = f.readlines()

    # Create list of Satellite objects
    sat_constellation = [read_sat_position(line) for line in lines if line[0]!='R']
    sat_constellation = {m.name:m for m in sat_constellation}
    route_str = next(filter(lambda x:x[0:5]=='ROUTE',lines))

    endpoints = parse_route(route_str)

    # Source and destination points will be treated as satellites with 0 height
    src = Satellite('src',endpoints['src']['lat'],endpoints['src']['lon'],0)
    dst = Satellite('dst',endpoints['dst']['lat'],endpoints['dst']['lon'],0)

    start_node = udlink(list(sat_constellation.values()),src)
    end_node = udlink(list(sat_constellation.values()),dst)


