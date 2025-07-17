from fsm import FSM
import argparse
import logging

logger = logging.getLogger('FSM for mod three')

def readfile(file):
    """
    Read a given .txt file and return its contents.

    Args:
        file (str): Path to text file.

    Returns:
        list of strings.
    
    Raises:
        Exception: Invlaid file type if a given files is not a .txt file.
    """
    if file.split('.')[-1]!='txt':
        raise Exception(f"Invalid file type {file}. Only .txt files are supported")
    
    logger.info(f'Reading {file} file')
    with open(file) as f:
        lines = f.read()
        
    return lines.split('\n')


def modthree(binary_string_or_file,verbose=True):
    """
    Get mod three of a given binary integer.

    Args:
        binary_string (str): Binary integer.
        file (str): Path to .txt file for list of binary integers
        verbose (bool): True to Print the integers and reminders

    Returns:
        list of tuples with integer and their reminders.
    
    """

    logger.info('Initializing FSM...')
    states = {'S0', 'S1', 'S2'}  # Finite set of states
    alphabets = {'0', '1'}  # Finite input alphabet 
    initial_state = 'S0'  # Initial state 
    final_states = {'S0', 'S1', 'S2'}  # Set of accepting/final states 
    transitions = {
        ('S0', '0'): 'S0',
        ('S0', '1'): 'S1',
        ('S1', '0'): 'S2',
        ('S1', '1'): 'S0',
        ('S2', '0'): 'S1',
        ('S2', '1'): 'S2',
    }

    fsm = FSM(states,alphabets,initial_state,final_states,transitions)
    reminders = {'S0':'0','S1':'1','S2':'2'}

    if '.' in binary_string_or_file:
        strings_to_check = readfile(binary_string_or_file)
    else:
        strings_to_check = [binary_string_or_file]

    logger.info('Checking Strings')

    return_result = []
    
    for string in strings_to_check:
        end_state = fsm.run(string)
        if verbose:
            print(string,' --> ',reminders.get(end_state,'Final state unreachable'))
        return_result.append((string,reminders.get(end_state,'Final state unreachable')))
        fsm.reset()

    return return_result



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find modulos of three for a given binary integer using finite state machine approach')
    parser.add_argument('-s','--string_or_file', type=str,help='Binary string to check or path to file',required=True)
    args = parser.parse_args()
    logger.info(f'Running mod three FSM for: {args.string_or_file}')
    _ = modthree(args.string_or_file)

    