import pandas as pd
import numpy as np
import math
import random
import time

'''
Vehicle Routing Problem

    In the Vehicle Routing Problem (VRP), the goal is to find optimal routes for multiple vehicles visiting a set of locations. (When there's only one vehicle, it reduces to the Traveling Salesperson Problem.)

    But what do we mean by "optimal routes" for a VRP? One answer is the routes with the least total distance. However, if there are no other constraints, the optimal solution is to assign just one vehicle to visit all locations, and find the shortest route for that vehicle. This is essentially the same problem as the TSP.

    A better way to define optimal routes is to minimize the length of the longest single route among all vehicles. This is the right definition if the goal is to complete all deliveries as soon as possible. The VRP example below finds optimal routes defined this way.

Capacited Vehicle Routing Problem

    The capacitated vehicle routing problem (CVRP) is a VRP in which vehicles with limited carrying capacity need to pick up or deliver items at various locations. The items have a quantity, and the vehicles have a maximum capacity that they can carry. The problem is to pick up or deliver the items for the least cost, while never exceeding the capacity of the vehicles.

Selected Search Algorithms: Hill Climbing Search Algorithm

    Hill climbing algorithm is a local search algorithm which continuously moves in the direction of increasing elevation/value to find the peak of the mountain or best solution to the problem. It terminates when it reaches a peak value where no neighbor has a higher value.
'''


'''
importing to csv data files
'''
# df_delivery= pd.read_csv("deneme_del.csv",index_col=[0],names=["Costumers", "Items"]).values
# df_distance= pd.read_csv("deneme_dist.csv",index_col=[0]).values
df_delivery= pd.read_csv("deliveries.csv",index_col=[0],names=["Costumers", "Items"]).values
df_distance= pd.read_csv("distances.csv",index_col=[0]).values



'''
definition of const values 
'''
num_vehicle = 2 #count of vehicle
capacity_vehicle = 900 # capacity of each vehicle
baseOf_Route = len(df_distance)-1 # route where does start from


'''
definition iterastion count (how many times program compile)

bigger iterastion count gives to you better route
'''
# iterastion = int(math.factorial(len(df_distance)-1))
iterastion = 9999


def routeLength(data, result):
    '''
    This function is calculating the sum of the route lenths. this function working with ONE route

    parameters:
        data : all distances between cities
        result : selected route
    
    return:
        routeLenght: sum of the selected route lenght (int)
    '''
    routeLength = 0
    for i in range(len(result)):
        routeLength += data[result[i - 1]][result[i]]
        #sum of length of the all path
        
    return routeLength

def sumOfrouteLenght(Iterationroutes):
    '''
    This function is calculating the sum of the all vehicle routes lenght.

    parameters:
        Iterationroutes: all vehicles routes (list)
    
    return:
        sums: sum of the all vehicle routes lenght (int)
    '''
    sums = 0
    for i in range(len(Iterationroutes)):
        sums+=Iterationroutes[i]['vehicleRouteLength']
    
    return sums

def capacityCheck(result):
    '''
    This function is calculating the how much capacity we need for the selected route. this function working with ONE route
    
    parameters:
        result: selected route
    
    return:
        capacity: total capacity of selected route (int)
    '''
    capacity = 0
    for i in range(len(result)):
        capacity += df_delivery[result[i]][0]

    return capacity

def isCapacityOkay(routes):
    '''
    This function is checking the capacities of all routes. This function working with ALL routes

    parameters:
        routes: ALL vehicles Infos
    returns:
        capacityOkay: if there is any over capacity vehicle, function returning False; if there isn't any over capacity vehicle, it return True. (Bool)
    '''
    capacityOkay = True
    for i in range(len(routes)):
        if(routes[i]['capacity'] > capacity_vehicle):
            capacityOkay = False


    return capacityOkay



def randomResult(data):
    #create random route
    result = []

    '''
    This function is recursive function. This function is creating as many vehicle object as num_vehicle number. Those vehicle objects have got own vehicleIds, own random routes, lenght of this route and capacity of this route. After creating vehicle objects, function checking is vehicles capacities okay . If it is okay, its returning those objects; if it is not, function run again.

    parameters:
        data : all distances between cities 
    returns:
        result: created vehicle object list
            Vehicle:
                vehicleId: spesific vehicle ids (primary number) (int)
                vehicleRandomRoute: created random route (city list) (array)
                vehicleRouteLenght: created random route's lenght (int)
                capacity: total capacity of selected route (int)


    !!!! Eğer Tek ise çalışır düzelt onu
    '''
    possibleCities = list(range(len(data)))
    routeCityCount = int((len(possibleCities)-1)/num_vehicle)
    possibleCities.pop(baseOf_Route)
    
    for carCount in range(num_vehicle):
        appendenObject={}
        appendenObject['vehicleId'] = carCount
        vehicleRoute = []
        vehicleRoute.append(baseOf_Route)
        for i in range(routeCityCount):
            randomCity = possibleCities[random.randint(0, len(possibleCities)-1)]
            #pick random number in the numbers of cities
            vehicleRoute.append(randomCity)
            possibleCities.remove(randomCity)
            #by removing selectd random city, repeat prevented
        vehicleRoute.append(baseOf_Route)
        appendenObject['vehicleRandomRoute'] = vehicleRoute
        appendenObject['vehicleRouteLength'] = routeLength(data, appendenObject["vehicleRandomRoute"])
        appendenObject['capacity']= capacityCheck(vehicleRoute)
        result.append(appendenObject)
    
    if(isCapacityOkay(result)):
        return result
    else: 
        return randomResult(df_distance)



def neighbours(result):
    '''
    This function is creating alternative routes that selected cities. 

    parameters:
        result: Route that we created randomly. (list(int))
    returns:
        neighbour_list: Creating alternative routes for cities that we passed on result (list(routes))
    
    '''
    neighbour_lists = []
    for i in range(1,len(result)-1):
        # It is start without changing start point "DEPOT"
        for j in range(i + 1, len(result)-1):
            # It will end without changing end point "DEPOT"
            neighbour_Routes = result.copy()
            neighbour_Routes[i] = result[j]
            neighbour_Routes[j] = result[i]
            neighbour_lists.append(neighbour_Routes)
            
            
            
    return neighbour_lists



def getBestNeighbour(data, neighbour_list, currentPath, currentLenght):
    '''
    This function is comparing all routes that we created.

    parameters:
        data : all distances between cities 
        neighbour_list: Alternative routes for cities
        currentPath: Route that we created randomly.
        currentLenght: Route length that we created randomly.
    returns:
        bestNeighbour: best route of all comperation
        bestRouteLength: Best routes lenght
    
    '''
    bestRouteLength = currentLenght
    bestNeighbour = currentPath
    
    
    for i in range(len(neighbour_list)):
        if(bestRouteLength > routeLength(data, neighbour_list[i])):
            bestRouteLength = routeLength(data, neighbour_list[i])
            bestNeighbour = neighbour_list[i]
        
    return bestNeighbour, bestRouteLength


def hillClimbing(data):

    currentSolution = randomResult(data)
    currentRouteLength = []
    neighbour_list = []
    
    # print(currentSolution)
    for i in range(len(currentSolution)):
        currentRouteLength.append(currentSolution[i]['vehicleRouteLength'])
        neighbour_list.append(neighbours(currentSolution[i]['vehicleRandomRoute']))
    
    for i in range(len(currentSolution)):
        bestNeighboursInfo = getBestNeighbour(data, neighbour_list[i], currentSolution[i]['vehicleRandomRoute'], currentSolution[i]['vehicleRouteLength'])
        currentSolution[i]['vehicleRandomRoute'] = bestNeighboursInfo[0]
        currentSolution[i]['vehicleRouteLength'] = bestNeighboursInfo[1]


    return currentSolution


def repeatIteration(firstIteration):
    '''
    this function is main function for running this script. It repeats iterastion times that we defined. At the begining, function accepts that first iteration is best iteration. If the next iterations are better, it is assigned as the best iteration. End of the iteration, it returns best routes of all iteration and their vehicles all route lenghts.


    '''
    bestIteration = firstIteration
    bestSumOfRouteLenght = sumOfrouteLenght(bestIteration)
    for i in range(iterastion):
        newIteration = hillClimbing(df_distance)
        if(bestSumOfRouteLenght> sumOfrouteLenght(newIteration)):
            bestIteration = newIteration
            bestSumOfRouteLenght = sumOfrouteLenght(newIteration)

    return bestIteration, bestSumOfRouteLenght








if __name__ == "__main__":
    start_time = time.time()

    bestRoutesofAllIteration = repeatIteration(hillClimbing(df_distance))

    for i in range(len(bestRoutesofAllIteration[0])):
        print('\n Vehicle No: %s' %bestRoutesofAllIteration[0][i]['vehicleId'])
        print('-----------------------------')
        print('\n Vehicle Route: %s' %bestRoutesofAllIteration[0][i]['vehicleRandomRoute'])
        print('\n Vehicle Route Lenght: %s' %bestRoutesofAllIteration[0][i]['vehicleRouteLength'])
        print('\n Vehicle Vehicle Capacity: %s \n' %bestRoutesofAllIteration[0][i]['capacity'])

    print('All vehicle total route lenghts : %s' %bestRoutesofAllIteration[1])
    print('Iterastion Count : %s' %iterastion)
    print("Execution Time : --- %s seconds ---" % (time.time() - start_time))
