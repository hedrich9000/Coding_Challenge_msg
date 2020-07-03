import logging
import argparse

from utils.load_csv import loadcsv
from utils.tsp import solvetsp


def get_args():
    """
    Setup possible arguments for command line execution.

    :return:
    parser object
    """
    parser = argparse.ArgumentParser(description='Import CSV-File and get a solution for the TSP problem.\n'
                                                 'If nothing is set, the program will set the csv-path to '
                                                 '"msg_standorte_deutschland.csv" and the iterations to 5.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--load', dest='load', type=str, default=False,
                        help='Load CSV-File in the stated form')
    parser.add_argument('-i', '--iterations', dest='iterations', type=int, default=False,
                        help='Set the wanted iterations with random initial routes for the algorithm')
    parser.add_argument('-s', '--score', dest='score', type=float, default=False,
                        help='[OPTIONAL] Set score, where the algorithms ends the optimization.')

    return parser.parse_args()


def load_args():
    """
    Helper function to setup and interpret command line arguments for further algorithms.
    :return:
    path: str
    iter: int
    score: float
    """
    args = get_args()

    path = args.load
    iter = args.iterations
    score = args.score

    if not path:
        path = "msg_standorte_deutschland.csv"
        logging.warning("Path set to {p}".format(p=path))

    if not iter:
        iter = 5
        logging.warning("Iterations set to {i}.".format(i=iter))

    if not score:
        score = 0.00001

    return path, iter, score


if __name__ == "__main__":
    # Set logging level according to your needs:
    logging.basicConfig(level=logging.WARNING)

    # Setup Argumentparser:
    path, iter, score = load_args()

    # Load file:
    csvloader = loadcsv(path)
    data_frame, dist_frame = csvloader.get_data()

    # Solve problem:
    tspsolver = solvetsp(dist_frame)
    tspsolver.set_init(rand=True)  # Possibility to set specific initial tour
    tspsolver.solve_opt2(scorethresh=score, iterations=iter)  # This function executes the algorithm
    sequence, dist = tspsolver.get_result()

    # Print output:-----------------------------------------------
    output = "######################################\n" \
             "Solved problem with following Results: \n" \
             "Total Distance in kilometer: {d}\n\n" \
             "Best found order of cities: \n".format(d=dist)
    for s in sequence:
        output = output + "{c}\n".format(c=data_frame["msg Standort"][s])
    print(output)
