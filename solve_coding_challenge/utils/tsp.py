import numpy as np
import logging
import random


class solvetsp:
    def __init__(self, dist_frame):
        """
        This class solves the traveling salesman problem with the 2-opt algorithm. As input, the distance matrix must
        be given in a pandas dataframe.
        :param dist_frame: dataframe
            Dataframe containing the distance matrix for all locations
        """
        self.dist_frame = dist_frame
        self.num = len(dist_frame) + 1  # Ismaning is at start and end of the list
        self.init = None
        self.set_init()

        # Optimize parameter:
        self.sequence = []  # Most recent sequence of locations (in numbers from 0-20)
        self.sequence_dists = []  # Distances between the locations
        self.dist = 0  # Total distance of the most recent sequence
        self.iterated_dists = []  # List of all calculated total distances over the iterations
        self.iterated_sequences = []  # List of all calculated sequences over the iterations
        self.best_iterated_sequences = []
        self.best_iterated_dist = []

    def solve_opt2(self, scorethresh, iterations=20):
        """
        This function executes the 2-opt algorithm for optimizing the route with the given distance matrix.
        Here, the iterations, which always start with a new random route, can be set. the scorethresh defines the
        threshold, where  the algorithm stops the optimizing process for each iteration. A common default value here is
        0.0001. A score of 0 describes no opimization between two steps in the algorithm.
        :param scorethresh: float
            Lower threshold for the score of each iteration
        :param iterations: int
            Number of iteration with random initial route
        :return:
        """
        # Get Initial sequence and distance
        self.sequence = self.init
        self.dist, self.sequence_dist = self._get_fulldist(self.sequence)
        logging.debug("Initial distance set: {d}".format(d=self.dist))
        logging.debug("Initial sequence set: {s}".format(s=self.sequence))

        all_sequences = []
        all_dists = []
        # Iterate over the number of iterations:
        for it in range(iterations):
            score = 1
            iteration_sequences = []
            iteration_dists = []
            while score > scorethresh:
                dist_prev = self.dist
                # Iterate over all parts of the sequence:
                for start in range(1, self.num - 2):
                    for stop in range(start + 1, self.num - 1):
                        # Reorder parts of the sequence:
                        sequence_new = np.concatenate((self.sequence[0:start],
                                                       self.sequence[stop:-len(self.sequence) + start - 1:-1],
                                                       self.sequence[stop + 1:len(self.sequence)])).tolist()
                        # Calculate new total distance of the resulting sequence:
                        dist_new, sequence_new_dist = self._get_fulldist(sequence_new)
                        self.sequence_dists.append(dist_new)
                        iteration_sequences.append(sequence_new)
                        iteration_dists.append(dist_new)
                        # Check if new total distance is smaller than recent total distance and save new best sequence
                        # and total distance (if not do nothing):
                        if dist_new < self.dist:
                            self.sequence = sequence_new
                            self.dist = dist_new
                            logging.debug("New best distance set: {d}".format(d=dist_new))

                score = 1 - self.dist / dist_prev
            # Save best distance and sequence from this iteration:
            all_sequences.append(iteration_sequences)
            all_dists.append(iteration_dists)
            self.iterated_dists.append(self.dist)
            self.iterated_sequences.append(self.sequence)
            logging.info("Score of Iteration {i}: {s}, Distance: {d}".format(i=it, s=score, d=self.dist))

            # Start over with new initial sequence:
            self.set_init(rand=True)
            self.sequence = self.init
            self.dist, self.sequence_dist = self._get_fulldist(self.sequence)

        # Get best total distance and sequence:
        self.dist = np.min(self.iterated_dists)
        try:
            ind = np.where(self.iterated_dists == self.dist)[0][0]
        except ValueError:
            ind = np.where(self.iterated_dists == self.dist)[0]
        self.sequence = self.iterated_sequences[ind]
        self.best_iterated_sequences = all_sequences[ind]
        self.best_iterated_dist = all_dists[ind]
        logging.info("Best result: Distance: {d} from Iteration {i}".format(i=ind, d=self.dist))

    def set_init(self, rand=True, init_list=None):
        """
        This function sets the initial route to a given order (init_list) or randomly. If nothing is set, the order will
        be set to random.
        :param rand: bool
        :param init_list: list [int]
        :return:
        """
        if rand or init_list is None:
            # Create random list of numbers between 1 and number of cities minus one:
            init_list = list(range(1, self.num - 1))
            random.shuffle(init_list)
        elif init_list is not None and len(init_list) == self.num:
            pass
        else:
            raise ValueError("init_list not set or does not have a length according to the given dist_frame")

        # Put Ismaning at start and end of the list:
        init_list = np.concatenate(([0], init_list, [0]))

        self.init = init_list

    def _get_fulldist(self, sequence):
        """
        Internal function to calculate the distances over the given sequence. Returns single distance as well as total
        distance.
        :param sequence: list [int]
            List of the locations in calculated order
        :return:
        fulldist: float
            Total distance for the given sequence
        sequence_dist: list [float]
            List of all single distances for the given sequence
        """
        sequence_dist = []
        for i in range(len(sequence) - 1):
            sequence_dist.append(self.dist_frame[sequence[i]][sequence[i + 1]])
        fulldist = sum(sequence_dist)
        return fulldist, sequence_dist

    def get_result(self):
        """
        This function returns the internal objects containing the resulting sequence (in numbers from 0-20) and total
        distance for the respective sequence.
        :return:
        sequence: list [int]
            List of the locations in calculated order
        dist: float
            Total distance for the given sequence
        """
        return self.sequence, self.dist

    def get_best_sequences(self):
        return self.best_iterated_dist, self.best_iterated_sequences
