import sys

from version import version
from game.engine import Engine
from game.utils.generate_game import generate
import game.config
import argparse
from visualizer.main import ByteVisualiser

if __name__ == '__main__':
    # Setup Primary Parser
    par = argparse.ArgumentParser()

    # Create Subparsers
    spar = par.add_subparsers(title="Commands", dest="command")

    # Generate Subparser
    gen_subpar = spar.add_parser('generate', aliases=['g'], help='Generates a new random game map')

    gen_subpar.add_argument('-seed', '-s', action='store', type=int, nargs='?', dest='seed',
                            help='Allows you to pass a seed into the generate function.')
    
    # Run Subparser and optionals
    run_subpar = spar.add_parser('run', aliases=['r'],
                                 help='Runs your bot against the last generated map! "r -h" shows more options')

    run_subpar.add_argument('-debug', '-d', action='store', type=int, nargs='?', const=-1, 
                            default=None, dest='debug', help='Allows for debugging when running your code')
    
    run_subpar.add_argument('-quiet', '-q', action='store_true', default=False,
                            dest='q_bool', help='Runs your AI... quietly :)')

    # Visualizer Subparser and optionals
    vis_subpar = spar.add_parser('visualize', aliases=['v'],
                                 help='Runs the visualizer! "v -h" shows more options')

    # might not be needed
    vis_subpar.add_argument('-log', action='store', type=str, nargs='?',
                            const=-1, default="../logs/", dest="logpath", help="Specify a log path")

    vis_subpar.add_argument('-server', action='store_true', default=False,
                            dest='skip', help='Skips visualizer pause and quits on end')

    all_subpar = spar.add_parser('gen,run,vis', aliases=['grv'],
                                 help='Generate, Run, Visualize! "grv -h" shows more options')

    # Version Subparser
    update_subpar = spar.add_parser('version', aliases=['ver'], help='Prints the current version of the launcher')

    # Client Parser
    client_parser = spar.add_parser('client', aliases=['s', 'c'], help='Run the client for the Byte-le Royale server')

    client_parser.add_argument('-csv',
                               help='Use csv output instead of the ascii table output (if applicable)',
                               default=False, action='store_true')

    # subparser group
    client_sub_group = client_parser.add_subparsers(title='client_subparsers', dest='subparse')
    leaderboard = client_sub_group.add_parser('leaderboard', aliases=['l'],
                                              help='Commands relating to the leaderboard')
    leaderboard.add_argument('-include_alumni', help='Include alumni in the leaderboard',
                             default=False, action='store_true')
    leaderboard.add_argument('-over_time', help='See how you have scored over time', default=False,
                             action='store_true')
    leaderboard.add_argument('-group_run_id',
                             help='pass the group_run_id you want to get run ids for. -1 is the default and most '
                                  'recent submission',
                             type=int, default=-1)

    # Stats subgroup
    stats = client_sub_group.add_parser('stats', aliases=['s'], help='View stats for your team')
    stats.add_argument('-current_run',
                       help='Get the status for the current group run (default if no flag given)',
                       default=False, action='store_true')
    stats.add_argument('-runs_for_group_run',
                       help='Pass the group_run id you want to get run ids for', type=int, default=-1)
    stats.add_argument('-runs_for_submission', help='Pass the submission_id you want to get run ids for',
                       type=int, default=-1)
    stats.add_argument('-get_submissions', help='Get all submission ids for your team', default=False,
                       action='store_true')

    # returns all ids of the group runs? need to double-check
    stats.add_argument('-get_group_runs', help='Get the group runs your team has been in', default=False,
                       action='store_true')
    stats.add_argument('-get_code_for_submission', help='Get the code file for a given submission',
                       type=int, default=-1)
    stats.add_argument('-get_errors_for_submission', help='Get the errors for a given submission',
                       type=int, default=-1)

    client_parser.add_argument('-register', help='Create a new team and return a vID', default=False,
                               action='store_true')
    client_parser.add_argument('-submit', help='Submit a client for grading', default=False,
                               action='store_true')

    # Parse Command Line
    par_args = par.parse_args()
    
    # Main Action variable
    action = par_args.command

    # Generate game options
    if action in ['generate', 'g']:
        generate()  # a random seed is already generated in the method by default
    
    # Run game options
    elif action in ['run', 'r']:
        # Additional args
        quiet = False

        if par_args.debug is not None:
            if par_args.debug >= 0:
                game.config.Debug.level = par_args.debug
            else:
                print('Valid debug input not found, using default value')
        
        if par_args.q_bool:
            quiet = True

        engine = Engine(quiet)
        engine.loop()

    # Run the visualizer
    elif action in ['visualize', 'v']:
        visualiser = ByteVisualiser()
        visualiser.loop()

    elif action in ['gen,run,vis', 'grv']:
        generate()
        engine = Engine(False)
        engine.loop()
        visualiser = ByteVisualiser()
        visualiser.loop()

    elif action in ['version', 'ver']:
        print(version, end="")

    # Print help if no arguments are passed
    if len(sys.argv) == 1:
        print("\nLooks like you didn't tell the launcher what to do!"
              + "\nHere's the basic commands in case you've forgotten.\n")
        par.print_help()
