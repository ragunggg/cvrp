import numpy as np
import osmnx as ox
import networkx as nx
import folium
import pulp
import itertools
import random

# function for plotting on google maps
def _plot_on_maps(latitude, longitude, name_list):
    m = folium.Map(location=[-6.9133, 107.6068], zoom_start=13, zoom_control=False, top=50)
    folium.Marker([latitude[0], longitude[0]], popup="<b>Depot {}</b>".format(name_list[0]), tooltip="Tekan!", icon=folium.Icon(color="red", icon="home")).add_to(m)
    
    for i in range(1,len(latitude)):
        folium.Marker([latitude[i], longitude[i]], popup="<b>Klien {}</b>".format(name_list[i]), tooltip="Tekan!", icon=folium.Icon(icon="users", prefix='fa')).add_to(m)

    return m

class FoliumRoute:
    def __init__(self,G,start,end):
        self.H = G.copy()
        self.start_ID = ox.distance.nearest_nodes(self.H, start[1], start[0])
        self.end_ID = ox.distance.nearest_nodes(self.H, end[1], end[0])
        self.shortest_route = ox.shortest_path(self.H, self.start_ID, self.end_ID, weight = 'length')
        self.shortest_route_length = nx.path_weight(self.H, self.shortest_route, weight="length")

def feature_route(G,m,fg,shortest_route,total_distance,color='blue'):
    ox.folium.plot_route_folium(G, shortest_route, route_map=fg, zoom = 14,tiles='OpenStreetMap',color=color,tooltip='<b>Jarak Tempuh : {} m</b>'.format(round(total_distance,2))).add_to(m)

# function for calculating distance between two pins
def _distance_calculator(G,latitude,longitude):
    H = G.copy()
    _distance_result = np.zeros((len(latitude),len(longitude)))
    
    for i in range(len(latitude)):
        for j in range(len(longitude)):
            
            # calculate distance of all pairs
            start = (latitude[i], longitude[i])
            end = (latitude[j], longitude[j])
            folium_route = FoliumRoute(G,start,end)

            # append distance to result list
            _distance_result[i][j] = folium_route.shortest_route_length
    
    return _distance_result

# solve with pulp
class cvrp_solver:
    def __init__(self,courier_count,courier_capacity,client_count,demand,distance):
        self.courier_count = courier_count
        self.courier_capacity = courier_capacity
        self.client_count = client_count
        self.distance = distance
        self.demand = demand

    def run(self):
        for courier_count in range(1,self.courier_count+1):
            
            # definition of LpProblem instance
            problem = pulp.LpProblem("CVRP", pulp.LpMinimize)

            # definition of variables which are 0/1
            x = [[[pulp.LpVariable("x%s_%s,%s"%(i,j,k), cat="Binary") if i != j else None
                    for k in range(courier_count)]
                    for j in range(self.client_count)]
                    for i in range(self.client_count)]

            # add objective function
            problem += pulp.lpSum(self.distance[i][j] * x[i][j][k] if i != j else 0
                                for k in range(courier_count) 
                                for j in range(self.client_count) 
                                for i in range (self.client_count))

            # constraints
            # equation (2)
            for j in range(1, self.client_count):
                problem += pulp.lpSum(x[i][j][k] if i != j else 0 
                                    for i in range(self.client_count) 
                                    for k in range(courier_count)) == 1 

            # equation (3)
            for k in range(courier_count):
                problem += pulp.lpSum(x[0][j][k] for j in range(1,self.client_count)) == 1
                problem += pulp.lpSum(x[i][0][k] for i in range(1,self.client_count)) == 1

            # equation (4)
            for k in range(courier_count):
                for j in range(self.client_count):
                    problem += pulp.lpSum(x[i][j][k] if i != j else 0 
                                        for i in range(self.client_count)) -  pulp.lpSum(x[j][i][k] for i in range(self.client_count)) == 0

            # equation (5)
            for k in range(courier_count):
                problem += pulp.lpSum(self.demand[j] * x[i][j][k] if i != j else 0 for i in range(self.client_count) for j in range (1,self.client_count)) <= self.courier_capacity[k]


            # equation (6)
            subtours = []
            for i in range(2,self.client_count):
                subtours += itertools.combinations(range(1,self.client_count), i)

            for s in subtours:
                problem += pulp.lpSum(x[i][j][k] if i !=j else 0 for i, j in itertools.permutations(s,2) for k in range(courier_count)) <= len(s) - 1

            
            # print courier_count which needed for solving problem
            # print calculated minimum distance value
            if problem.solve() == 1:
                break
        
        if problem.solve() == -1:
            return False
            
        # find solution
        solution = []
        for k in range(courier_count):
            arcs = []
            for i in range(self.client_count):
                for j in range(self.client_count):
                    if i != j and pulp.value(x[i][j][k]) == 1:
                        arcs.append((i,j))

            solution.append(arcs)

        return solution

# visualization : plotting on google maps
class visualization(cvrp_solver):
    def __init__(self,G,map,latitude,longitude,solution,couriers_name):
        self.G = G
        self.map = map
        self.latitude = latitude
        self.longitude = longitude
        self.solution = solution
        self.couriers_name = couriers_name

    def cvrp_map(self):
        m = self.map
        solution = self.solution
        color = ["%06x" % random.randint(0, 0xFFFFFF) for _ in solution]

        for k, courier in enumerate(solution):
            fg = folium.FeatureGroup(name='Kurir {}'.format(self.couriers_name[k]))
            total_distance = 0
            routes = []
            for arc in courier:
                startID = arc[0]
                endID = arc[1]
                start = (self.latitude[startID], self.longitude[startID])
                end = (self.latitude[endID], self.longitude[endID])
                folium_route = FoliumRoute(self.G, start, end)
                total_distance += folium_route.shortest_route_length
                routes.append(folium_route.shortest_route)

            for route in routes:
                feature_route(self.G,m,fg,route,total_distance,'#{}'.format(color[k]))

        return m