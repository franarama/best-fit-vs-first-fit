import matplotlib.pyplot as plt
import math
import random
from scipy.stats import binom

# function to get binomial value
def get_binomial(n,p):
    return binom.rvs(n,p)

# function to return the index of the server with the
# shortest queue - to be used with first fit
def get_first_fit_server(server_array,cpu):
    count = 0
    while count < len(server_array):
        if (server_array[count]+cpu <= 1):
            return count
        count = count+1

# function to return the index of the server with the
# best fit for the given CPU Val
def get_best_fit_server(server_arr, job_size):
    best_fit_index = 0
    best_difference = 1 - (server_arr[0] + job_size)
    # if the first best index doesnt have room make it the max, 1
    if best_difference < 0:
        best_difference = 1
    for s in range(len(server_arr)):
        difference = 1 - (server_arr[s] + job_size)
        # we want to minimize the difference as much as possible
        # without it getting to be less than 0
        if (difference < best_difference) and (difference >= 0):
            best_difference = difference
            best_fit_index = s
    return best_fit_index

def assign_to_servers(vm_arrivals,server_arr,str):
    for s in range(len(vm_arrivals)):

        # -- assign to server with corresponding CPU requirements -- #
        if vm_arrivals[s] == 1:
            if str == "bf":
                index = get_best_fit_server(server_arr,VM_CPUS[0])
            if str == "ff":
                index = get_first_fit_server(server_arr,VM_CPUS[0])
            server_arr.insert(index, VM_CPUS[0])

        if vm_arrivals[s] == 2:
            if str == "bf":
                index = get_best_fit_server(server_arr,VM_CPUS[1])
            if str == "ff":
                index = get_first_fit_server(server_arr,VM_CPUS[1])
            server_arr.insert(index, VM_CPUS[1])

        if vm_arrivals[s] == 3:
            if str == "bf":
                index = get_best_fit_server(server_arr,VM_CPUS[2])
            if str == "ff":
                index = get_first_fit_server(server_arr,VM_CPUS[2])
            server_arr.insert(index, VM_CPUS[2])

# function to do departures
def do_departures(server_list,vm_types_list):
    for s in range(T):
        if server_list[s] != 0:
            vm_types = vm_types_list[s]  # get the types of VMs the server has
            # so [#type1,#type2,#type3]
            # for each VM type generate a departure if it is non-zero
            if vm_types[0] != 0:
                for i in range(vm_types[0]):
                    dep = generate_departure(VM_MEANS[0])
                    if dep == 1:
                        server_list[s] = server_list[s] - VM_CPU[0]
                        to_change = vm_types_list[s]
                        to_change[0] = to_change[0] - 1
            if vm_types[1] != 0:
                for i in range(vm_types[1]):
                    dep = generate_departure(VM_MEANS[1])
                    if dep == 1:
                        server_list[s] = server_list[s] - VM_CPU[1]
                        to_change = vm_types_list[s]
                        to_change[1] = to_change[1] - 1
            if vm_types[2] != 0:
                for i in range(vm_types[2]):
                    dep = generate_departure(VM_MEANS[2])
                    if dep == 1:
                        server_list[s] = server_list[s] - VM_CPU[2]
                        to_change = vm_types_list[s]
                        to_change[2] = to_change[2] - 1

def get_server_count(server_arr):
    count = 0
    for s in range(len(server_arr)):
        if s!= 0:
            count = count + 1
    return count

def get_array_of_arrivals():
    vm_arrivals = []
    num_vms = get_binomial(int(n), LAMBDA)  # get the number of VMs that arrive as binomial r.v
    # print("n= ", n, " num vms= ", num_vms)

    # get the type of VMs that arrived, 1/3 probability of each
    for s in range(num_vms):
        vm_type = generate_vm_type()
        vm_arrivals.append(vm_type)
    return vm_arrivals

# function to generate departure based on given mu val
def generate_departure(mean):
    mu_val = 1.0 / mean
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

T = 101 # time slots
LAMBDA = 0.9 # lambda value

server_list_ff = [0] * T # holds the servers; 0 represents a server not in use
vm_types_list_ff = [[0,0,0]] * len(server_list_ff) # works with server list, keeps track of the amount of each type the server has

server_list_bf = [0] * T
vm_types_list_bf = [[0,0,0]] * len(server_list_bf)

# -- 3 VMs with their CPU unit requirements and mean -- #
VM_CPUS = [0.5,0.25,0.125]
VM_MEANS = [10,8,30]

i = 2
n = math.pow(2,i) # start with n = 2^2

x_axis = []
y_axis_ff = []
y_axis_bf = []

while n <= math.pow(2,5):
    print(n)
    # keep track of the servers to get the average for both
    # best fit and first fit
    server_count_ff = 0
    server_count_bf = 0

    avg_count_ff = 0
    avg_count_bf = 0

    time_slot = 0

    while time_slot < T:

        # -- GENERATE DEPARTURES FIRST -- #
        do_departures(server_list_ff,vm_types_list_ff)
        do_departures(server_list_bf,vm_types_list_bf)

        # -- GENERATE ARRIVALS -- #
        arrivals_ff = get_array_of_arrivals()
        arrivals_bf = get_array_of_arrivals()

        # -- ASSIGN ARRIVALS TO SERVERS -- #
        assign_to_servers(arrivals_ff,server_list_ff,"ff")
        assign_to_servers(arrivals_bf,server_list_bf,"bf")

        # -- GET THE COUNTS OF BOTH FIRST FIT AND BEST FIT -- #
        server_count_ff = server_count_ff + get_server_count(server_list_ff)
        server_count_bf = server_count_bf + get_server_count(server_list_bf)

        time_slot = time_slot + 1

    avg_count_bf = float(server_count_bf) / T
    print(avg_count_bf)
    avg_count_ff = float(server_count_ff) / T
    print(avg_count_ff)
    x_axis.append(n)
    y_axis_bf.append(avg_count_bf)
    y_axis_ff.append(avg_count_ff)

    i = i + 1
    n = math.pow(2,i)

plt.xlabel("N")
plt.ylabel("Average number of servers")
plt.title("Average number of servers vs. N for best fit and first fit policies")
plt.legend(('Best fit policy', 'First fit policy'), loc='upper left')

plt.grid(True)

plt.plot(x_axis, y_axis_bf)
plt.plot(x_axis, y_axis_ff)

plt.show()




