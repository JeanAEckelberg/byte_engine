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

    vis_subpar.add_argument('-log', action='store', type=str, nargs='?',
                            const=-1, default="../logs/", dest="logpath", help="Specify a log path")

    vis_subpar.add_argument('-server', action='store_true', default=False,
                            dest='skip', help='Skips visualizer pause and quits on end')

    all_subpar = spar.add_parser('gen,run,vis', aliases=['grv'],
                                 help='Generate, Run, Visualize! "grv -h" shows more options')

    # Version Subparser
    update_subpar = spar.add_parser('version', help='Prints the current version of the launcher')

    # Client Parser
    client_parser = spar.add_parser('client', aliases=['c'], help='Run the client for the Byte-le Royale server')

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
    leaderboard.add_argument()

    # Parse Command Line
    par_args = par.parse_args()
    
    # Main Action variable
    action = par_args.command

    # Generate game options
    if action in ['generate', 'g']:
        if par_args.seed:
            generate(par_args.seed)
        else:
            generate()
    
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

    elif action in ['visualize', 'v']:
        visualiser = ByteVisualiser()
        visualiser.loop()

    elif action in ['gen,run,vis', 'grv']:
        generate()
        engine = Engine(False)
        engine.loop()
        visualiser = ByteVisualiser()
        visualiser.loop()

    # Print help if no arguments are passed
    if len(sys.argv) == 1:
        print("\nLooks like you didn't tell the launcher what to do!"
              + "\nHere's the basic commands in case you've forgotten.\n")
        par.print_help()
