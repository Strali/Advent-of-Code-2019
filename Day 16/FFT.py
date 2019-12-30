# Code for solving the day 16 task of Advent of Code 2019.
#
# Author:
#   Andreas Falkovén (2019-12-20)

import numpy as np
import time
from itertools import cycle, islice

def FFT(input_sequence, base_pattern, n_phases = 100, message_length = 8):
    """(Slow) naïve implementation of the FFT algorithm to solve part 1.

    Parameters
    ----------
    input_sequence : list
        List of digits in the input number.
    base_pattern : list
        Base pattern which willbe extended by the FFT.
    n_phases : int
        The number of phases to apply the FFT. Default is 100.
    message_length : int
        Length of message to return. Default is 8.

    Returns
    -------
    A string representing the output after having applied the FFT n_phases times to the input sequence.
    """

    input_length = len(input_sequence)
    next_input = np.zeros(input_length)

    # Loop over phases.
    for iPhase in range(0, n_phases):
        if iPhase > 0:
            input_sequence = list(next_input)

        # Loop over each digit in input sequence.
        for iDigit in range(0, len(input_sequence)):
            # Create pattern based on current digit.
            pattern = np.repeat(base_pattern, iDigit+1)
            digit_pattern = list(islice(cycle(pattern), input_length+1)) # +1 since we'll be skipping the first digit.
            digit_pattern = np.array(digit_pattern[1:])

            # Multiply the input by the digit pattern.
            output = abs(np.dot(input_sequence, digit_pattern)) % 10

            # Add result to input for next iteration.
            next_input[iDigit] = output

    output_sequence = [int(d) for d in next_input]

    return ''.join(map(str, output_sequence[:message_length]))


def Part_2(input_sequence, n_phases = 100, offset_length = 7, input_multiplier = 10000, message_length = 8):
    """Solves part 2 using a reverse cumulative sum.

    Parameters
    ----------
    input_sequence : list
        List of digits in the input number.
    n_phases : int
        The number of phases to run. Default is 100.
    offset_length : int
        Length of initial sequence to be used as offset. Default is 7.
    input_multiplier : int
        Number of times to replicate the input sequence. Default is 10000.
    message_length : int
        Length of message to return. Default is 8.

    Returns
    -------
    A string representing the output after having applied the FFT n_phases times to the input sequence.
    """

    # Determine the offset and extended input.
    offset = int(''.join(map(str, input_sequence[:offset_length])))
    extended_input = (input_sequence[:]*input_multiplier)[offset:]
    assert offset > len(extended_input)/2 # Safety check, our offset should put us in the second half of the input sequence.

    # Loop over phases.
    for _ in range(n_phases):
        # Initialize accumulator.
        accumulated_value = 0
        # Loop over digits in sequence. We loop backwards in order to reuse previously calculated values.
        for iDigit in range(len(extended_input)-1, -1, -1):
            # Determine next value in transformed sequence.
            accumulated_value += extended_input[iDigit]
            extended_input[iDigit] = accumulated_value % 10

    return ''.join(map(str, extended_input[:message_length]))


if __name__ == '__main__':
    # Solve both parts.

    # For part 1 only.
    base_pattern = [0, 1, 0, -1]

    # For part 2 only.
    offset_length = 7        # Length of segment that determines offset.
    input_multiplier = 10000 # Number of times to multiply input.

    # For both parts.
    n_phases = 100           # Number of phases to apply.
    message_length = 8       # Length of final message.

    input_number = 59734319985939030811765904366903137260910165905695158121249344919210773577393954674010919824826738360814888134986551286413123711859735220485817087501645023012862056770562086941211936950697030938202612254550462022980226861233574193029160694064215374466136221530381567459741646888344484734266467332251047728070024125520587386498883584434047046536404479146202115798487093358109344892308178339525320609279967726482426508894019310795012241745215724094733535028040247643657351828004785071021308564438115967543080568369816648970492598237916926533604385924158979160977915469240727071971448914826471542444436509363281495503481363933620112863817909354757361550

    input_sequence = [int(digit) for digit in str(input_number)] # Convert input number to list of digits.

    start_time_p1 = time.time()
    part_1_output = FFT(input_sequence, base_pattern, n_phases, message_length)

    print('Part 1:')
    print(part_1_output)
    print('Time to execute: %.2f' % (time.time() - start_time_p1))

    start_time_p2 = time.time()
    part_2_output = Part_2(input_sequence, n_phases, offset_length, input_multiplier, message_length)

    print('Part 2:')
    print(part_2_output)
    print('Time to execute: %.2f' % (time.time() - start_time_p2))
