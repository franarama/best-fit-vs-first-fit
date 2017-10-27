import matplotlib.pyplot as plt
import math
import random
from scipy.stats import binom

# function to get binomial value
def get_binomial(n,p):
    return binom.rvs(n,p)

# function to return the index of the shortest queue
def get_first_fit_server(server_array):
    count = 1
    shortest_index = 0
    while count < len(server_array):
        if server_array[count] < server_array[shortest_index]:
            shortest_index = count
        count = count+1
    return shortest_index

# function to generate d based on given mu val
def generate_departure(mean):
    rand_num = random.uniform(0,1)
    if (rand_num >= mu_val):
        return 1
    return 0

# function to get vm type
def generate_vm_type():
    sum = 0
    rand_num = random.uniform(0,1)
    while sum < 1:
        sum = sum + (1/3)
        if rand_num < sum:
            if sum <= (1/3):
                return 1
            if sum <= (2/3):
                return 2
            else:
                return 3

T = 100000 # time slots
LAMBDA = 0.9 # lambda value

server_list = [0] * T # holds the servers; 0 represents a server not in use
vm_types_list = [0,0,0] * len(server_list) # works with server list, keeps track of the amount of each type the server has

# -- 3 VMs with their CPU unit requirements and mean #
VM_CPUS = [0.5,0.25,0.125]
VM_MEANS = [10,8,30]

time_slot = 0
i = 2
n = math.pow(2,i) # start with n = 2^2

while n <= math.pow(2,5):
    while time_slot < T:

        # -- GENERATE DEPARTURES FIRST -- #
        for s in range(len(server_list)):
            if server_list[s] != 0:
                vm_types = vm_types_list[s] # get the types of VMs the server has
                                            # so [#type1,#type2,#type3]

                # for each VM type generate a departure if it is non-zero
                for i in range(vm_types[0]):
                    if i != 0:
                        dep = generate_departure(VM_MEANS[0])
                        if dep == 1:
                            server_list[s] = server_list[s] - VM_CPU[0]
                            to_change = vm_types_list[s]
                            to_change[0] = to_change[0] - 1

                for i in range(vm_types[1]):
                    if i != 0:
                        dep = generate_departure(VM_MEANS[1])
                        if dep == 1:
                            server_list[s] = server_list[s] - VM_CPU[1]
                            to_change = vm_types_list[s]
                            to_change[1] = to_change[1] - 1

                for i in range(vm_types[2]):
                    if i != 0:
                        dep = generate_departure(VM_MEANS[2])
                        if dep == 1:
                            server_list[s] = server_list[s] - VM_CPU[2]
                            to_change = vm_types_list[s]
                            to_change[2] = to_change[2] - 1

        # -- GENERATE ARRIVALS -- #
        vm_arrivals = []
        num_vms = get_binomial(int(n), LAMBDA)  # get the number of VMs that arrive as binomial r.v
        # print("n= ", n, " num vms= ", num_vms)

        # get the type of VMs that arrived, 1/3 probability of each
        for s in range(len(num_vms)):
            vm_type = generate_vm_type()
            vm_arrivals.append(vm_type)

        # -- ASSIGN ARRIVALS TO SERVERS -- #
        time_slot = time_slot + 1
    i = i + 1
    n = math.pow(2,i)

## best fit function -- so far--- i think i should quit computing
# science because sometimes i can't figure out very simple things :( :(
# hope it will work
def best_fit_algorithm(server,jobs):
    server_size = len(server)
    job_size = len(jobs)
 #Stores block id of the block allocated to a process
    m=0
    k=0
    best_fit_array = []
#Initially no block is assigned to any process
    for k in range (len(best_fit_array)):
        best_fit_array [k] = -1
 #   pick each process and find suitable blocks according to its size ad assign to it
    for i in jobs:
        #Find the best fit block for current process
        index = -1
        k = k+1
        for j in  server:
            if (server[m]>=jobs[k]):
                if (index == -1):
                    index = j
                elif (server[index]>server[m]):
                    index = j
        m = m+1
        #If we could find a block for current process
        if (index !=-1):
            #allocate block j to best_fit_array[i] process
            best_fit_array [i] = index
            #Reduce available memory in this server.
            server[index] -= jobs[i]
        
    for i in job_size:
        if (best_fit_array[i] != -1):
            best_fit_array = best_fit_array[i] + 1
    return best_fit_array
             

server = [233,3333,333,333,33]
jobs = [233,222,2222,22,0]

a=best_fit_algorithm(server,jobs)

print(a)



