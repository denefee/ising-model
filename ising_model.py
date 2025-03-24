import numpy as np
import os

# general variables
# temperature = 1
grid_size = 100
ncycles = 1500000

# output characteristics
output_freq = 50
output_start = 1000000

def MK_step(lattice, grid_size, temperature, E, M, N):
    x, y = np.random.randint(0, grid_size, 2)

    delta_E = lattice[x][y] * (lattice[(x + grid_size - 1) % grid_size][y] + 
                lattice[(x + 1) % grid_size][y] + lattice[x][(y + grid_size - 1) % grid_size] + 
                lattice[x][(y + 1) % grid_size])
    
    ksi = np.random.sample()
    if (ksi < np.exp(- delta_E / temperature)):
        lattice[x][y] *= -1
        return E + delta_E, M + 2.0 * lattice[x][y] / N
    return E, M

def xyz_dump(N, lattice, n, temperature):
    file_path = os.path.join(str(temperature), f"{n}.xyz")
    with open(file_path, 'w') as xyz:
        xyz.write(f"{N}\n")
        xyz.write(f"Time = {n}\n")
        for i in np.arange(grid_size):
            for j in np.arange(grid_size):
                xyz.write(f"{i} {j} {lattice[i][j]}\n")


def ising(temperature, grid_size, ncycles):
    N = grid_size * grid_size # Number of spins
    E = -2 * N # Full energy
    M = 1 # Average magnetic moment
    lattice = np.ones((grid_size, grid_size))

    # Data dump block
    # os.makedirs(str(temperature), exist_ok=True)
    # os.makedirs('data', exist_ok=True)
    data = open('new_curie_data'+str(temperature)+'.csv', 'w')
    data.write(str('n,E,M') + '\n')
    # data.write('0,' + str(E) + ',' + str(M) + '\n')

    # Main loop
    for n in np.arange(1, ncycles+1):
        E, M = MK_step(lattice, grid_size, temperature, E, M, N)

        if (n % output_freq == 0)and(n >= output_start):
            data.write(str(n) + ',' + str(E) + ',' + str(M) + '\n')
            # xyz_dump(N, lattice, n, temperature)
    
    data.close()

if __name__ == "__main__":
    for T in np.arange(1.0, 1.55, 0.05):
        ising(round(T, 2), grid_size, ncycles)