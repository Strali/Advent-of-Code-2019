# Code for solving the dat 12 task of Advent of Code 2019.
#
# Author:
#   Andreas Falkovén (2019-12-12)

import numpy as np
import time

def update_all_velocities(current_position, current_velocity):
    """Update all system velocity components (x, y, and z) based positions.

    Parameters
    ----------
    current_position : array
        Array of current (x,y,z) positions for each moon.
    current_velocity : array
        Array of current (x,y,z) velocities for each moon.

    Returns
    -------
    new_velocities : array
        Array of new velocities for the moons.
    """

    new_velocities = current_velocity.copy()
    num_moons = new_velocities.shape[0]
    num_dimensions = new_velocities.shape[1]

    # Loop over coordinates.
    for k in range(0, num_dimensions):
        # Loop over moons.
        for i in range (0, num_moons):
            # We don't need to recheck earlier moons.
            for j in range(i+1, num_moons):
                if current_position[i][k] < current_position[j][k]:
                    new_velocities[i][k] += 1
                    new_velocities[j][k] -= 1
                elif current_position[i][k] > current_position[j][k]:
                    new_velocities[i][k] -= 1
                    new_velocities[j][k] += 1

    return new_velocities


def update_single_velocity_component(positions, velocities):
    """Update system velocities for only one component (x, y, or z).

    Parameters
    ----------
    positions : array
        Array of positions for one component.
    velocities : array
        Array of velocities for one component.

    Returns
    -------
    new_velocities : array
        Array of updated velocities for the given velocity component.
    """

    new_velocities = velocities.copy()
    num_moons = new_velocities.shape[0]

    # Loop over moons.
    for i in range (0, num_moons):
        # We don't need to recheck earlier moons.
        for j in range(i+1, num_moons):
            if positions[i] < positions[j]:
                new_velocities[i] += 1
                new_velocities[j] -= 1
            elif positions[i]> positions[j]:
                new_velocities[i] -= 1
                new_velocities[j] += 1

    return new_velocities


def get_system_energies(positions, velocities):
    """Determine the total energy of each moon.
    The total energy is the potential energy multiplied by the kinetic energy of each moon. The potential energy is the sum of the absolute positions of the moon, while the kinetic energy is the sum of the absolute velocities of the moon.

    Parameters
    ----------
    positions : array
        Array of moon positions.
    velocities : array
        Array of moon velocities.

    Returns
    -------
    array
        Array of the total energy (potential*kinetic) of each moon.
    """

    # Sum positions and energies row-wise.
    potential_energies = np.sum(np.absolute(positions), 1)
    kinetic_energies = np.sum(np.absolute(velocities), 1)

    return potential_energies*kinetic_energies


def run_simulations(nTimesteps, initial_positions, initial_velocities):
    """Run moon trajectory simulatios for n timesteps.

    Parameters
    ----------
        nTimesteps : int
            The number of timesteps to run the simulations.
        initial_positions : array
            Array of starting positions for the moons.
        initial_velocities : array
            Array of starting velocities for the moons.

    Returns
    -------
        system_energy : int
            Total energy of the moon system.
    """
    current_position = initial_positions.copy()
    current_velocity = initial_velocities.copy()

    iTimestep = 0
    # Simulate for the given number of timesteps.
    while iTimestep < nTimesteps:

        # Update velocity and position.
        current_velocity = update_all_velocities(current_position, current_velocity)
        current_position += current_velocity

        iTimestep += 1

    # Determine final system energy.
    system_energy = get_system_energies(current_position, current_velocity)
    total_energy = sum(system_energy)

    return total_energy


def determine_period_length(initial_positions, initial_velocities):
    """Determine the period length (i.e. time until it returns to the initial state) of the four moon system.
    
    Parameters
    ----------
    initial_positions : array
        Array of initial positions of all moons.
    initial_velocities : array
        Array of initial velocities for all moons.

    Returns
    -------
    num_iterations : int
        The number of timesteps/iterations in a system cycle.
    """

    num_iterations = [0, 0, 0] # Keep track of the number of iterations.

    # Loop over coordinate components.
    for iDim in range(0, 3):
        # Get initial states for the current component.
        positions = initial_positions[:, iDim].copy()
        velocities = initial_velocities[:, iDim].copy()

        # Loop until we return to our original state.
        print('Looking for cycle length for coordinate %d' % (iDim+1))
        while True:
            num_iterations[iDim] += 1

            velocities = update_single_velocity_component(positions, velocities)
            positions += velocities 

            # Check if we are back at the original state.
            if all(velocities == 0) & all(positions == initial_positions[:, iDim]):
                print('Found a cycle for coordinate %d after %d iterations' % ((iDim+1), num_iterations[iDim]))
                break

    return num_iterations

# Helper functions.
def gcd(a, b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)


if __name__ == '__main__':
    """Run moon simulations with either test or real input."""

    # Test input:
    # initial_positions = np.array([[-8,  -10,  0],
    #                               [5, 5, 10],
    #                               [2,  -7,  3],
    #                               [9,  -8, -3]])

    # Real input:
    initial_positions = np.array([[  5,   4,  4],
                                  [-11, -11, -3],
                                  [  0,   7,  0],
                                  [-13,   2, 10]])

    # Velocity always starts as 0 in all directions.
    initial_velocities = np.array([[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]])

    num_simulation_steps = 1000 # Run for 1000 steps.

    # Task 1
    # Determine total energy of the moon system after 1000 updates.
    print('\nTASK 1:')
    print('='*43)
    print('\nRunning moon simulations for %d timesteps' % num_simulation_steps)

    start_time = time.time()
    system_energy = run_simulations(num_simulation_steps, initial_positions, initial_velocities)

    print('Total system energy: %d' % system_energy)
    print('Execution time: %.3f seconds\n' % (time.time() - start_time))

    # Task 2
    # Find period of system, i.e. time until it returns to the initial state.
    print('TASK 2:')
    print('='*43)
    print('Finding period of system')
    start_time = time.time()
    num_iterations = determine_period_length(initial_positions, initial_velocities)
    print('\nCycle lengths for each position component: %s' % num_iterations)

    # Determine lowest common multiplier for all component cycles.
    lcm_1 = lcm(num_iterations[0], num_iterations[1]) # LCM for first two components.
    lcm_2 = lcm(lcm_1, num_iterations[2]) # LCM for third component.
    print('Period length of moon system: %d' % lcm_2)
    print('Execution time: %.3f seconds\n' % (time.time() - start_time))
