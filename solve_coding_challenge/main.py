import logging
import argparse

from utils.load_csv import loadcsv
from utils.tsp import solvetsp
from utils.visualization import visualize_map, visualize_graph

def get_args():
    """
    Setup possible arguments for command line execution.

    :return:
    parser object
    """
    parser = argparse.ArgumentParser(description='Import CSV-File and get a solution for the TSP problem.\n'
                                                 'If nothing is set, the program will set the csv-path to '
                                                 '"msg_standorte_deutschland.csv" and the iterations to 10.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--load', dest='load', type=str, default=False,
                        help='Load CSV-File in the stated form')
    parser.add_argument('-i', '--iterations', dest='iterations', type=int, default=False,
                        help='[OPTIONAL] Set the wanted iterations with random initial routes for the algorithm')
    parser.add_argument('-s', '--score', dest='score', type=float, default=False,
                        help='[OPTIONAL] Set score, where the algorithms ends the optimization.')
    parser.add_argument('-m', '--vis_map', dest='vis_map', default=False, action="store_true",
                        help='[OPTIONAL] Enable visualization of the cities on a map using your webbrowser.')
    parser.add_argument('-g', '--vis_graph', dest='vis_graph', default=False, action="store_true",
                        help='[OPTIONAL] Enable visualization of the algorithm steps as a graph using your webbrowser.')
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
    iterate = args.iterations
    score = args.score
    vis_map = args.vis_map
    vis_graph = args.vis_graph

    if not path:
        path = "msg_standorte_deutschland.csv"
        logging.warning("Path set to {p} by default".format(p=path))

    if not iterate:
        iterate = 10
        logging.warning("Iterations set to {i} by default".format(i=iterate))

    if not score:
        score = 0.00001

    return path, iterate, score, vis_map, vis_graph


if __name__ == "__main__":
    # Set logging level according to your needs:
    logging.basicConfig(level=logging.WARNING)

    # Setup Argumentparser:
    path, iter, score, vis_map, vis_graph = load_args()

    # Load file:
    csvloader = loadcsv(path)
    data_frame, dist_frame = csvloader.get_data()

    # Solve problem:
    tspsolver = solvetsp(dist_frame)
    tspsolver.set_init(rand=True)  # Possibility to set specific initial tour
    tspsolver.solve_opt2(scorethresh=score, iterations=iter)  # This function executes the algorithm
    sequence, dist = tspsolver.get_result()

    # Print output:-----------------------------------------------
    output = "\n### Result ######################################################\n" \
             "Solved problem with following Results: \n" \
             "-- Total Distance in kilometer: {d}\n\n" \
             "-- Best found order of cities: \n".format(d=dist)
    for s in sequence:
        output = output + "       {c}\n".format(c=data_frame["msg Standort"][s])
    output = output + "#################################################################\n"
    print(output)

    if vis_map:
        logging.debug("Visualizing the cities on a map as html in the default webbrowser")
        map = visualize_map(data_frame)
        map.visualize_sequence_on_map(sequence)

    if vis_graph:
        logging.debug("Visualizing the graph showing all sequences of the best iteration as html in the default webbrowser")
        graph = visualize_graph(tspsolver, data_frame)
        graph.visualize_sequences_in_graph()

