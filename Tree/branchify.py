"""
branchify.py
@Autor: Rentian Dong, Modified by R. Anthony Rojas Chavez 
"""
import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size
from argparse import ArgumentParser
from src.Util.matrix import as_adj_list
from Bio import Phylo
from src.Util.stdout_redirect import StdoutRedirector
from src.Util.misc import get_accession
DEFAULT_THRESHOLD = 0.009

class Group:
    """
    to store temporary results during branchify algorithm
    """
    def __init__(self, ids, depth):
        self.ids = ids
        self.depth = depth

# noinspection PyShadowingBuiltins
def branchify_khans(dist_adj_list, thresh=DEFAULT_THRESHOLD):
    """
    computes branches using Khan's method.
    :param dist_adj_list: an adjacency list of the from id -> {id -> dist}
    :param thresh: ids with distance less than threshold will be grouped
    :return: the groups computed
    """
    branches = {}
    # noinspection PyShadowingBuiltins
    for id in dist_adj_list:
        is_grouped = False
        for leader_id in branches:
            if dist_adj_list[leader_id][id] < thresh:
                branches[leader_id].append(id)
                is_grouped = True
                break
        if not is_grouped:
            branches[id] = []
    return [[id] + branches[id] for id in branches]


def branchify_tree(tree, thresh=DEFAULT_THRESHOLD):
    """
    computes branches bottom up. groups are sub-trees where distance from
    root to furthest node is no more than threshold
    :param tree: a BioPython Tree instance
    :param thresh: threshold
    :return: list of groups
    """
    groups = __branchify_tree_help(tree.root, thresh)
    return [g.ids for g in groups]


def __branchify_tree_help(root, thresh=DEFAULT_THRESHOLD):
    if len(root.clades) == 0:
        return [Group([get_accession(root.name)], root.branch_length)]
    glists = [__branchify_tree_help(node, thresh) for node in root.clades]
    collapsed = Group([], 0)
    res = []
    for glist in glists:
        if len(glist) == 1 and glist[0].depth + root.branch_length < thresh:
            collapsed.ids += glist[0].ids
            collapsed.depth = max(collapsed.depth, glist[0].depth + root.branch_length)
        else:
            res += glist
    if len(collapsed.ids) > 0:
        res.append(collapsed)
    return res


def main():
    """
    entry point
    """
    # parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-i', dest='in_file_name', type=str, required=True, help='newick file')
    parser.add_argument('-t', dest='threshold', type=float)
    parser.add_argument('-m', dest='method', type=str)
    parser.add_argument('-o', dest='out_file_name', type=str, help="each line is a group's accession numbers")
    args = parser.parse_args()

    # compute the branches
    threshold = args.threshold if args.threshold else DEFAULT_THRESHOLD
    if args.method is None or args.method == 'khan':
        with open(args.in_file_name) as f:
            branches = branchify_khans(as_adj_list(f, id_col=True), thresh=threshold)
    else:
        with open(args.in_file_name) as f:
            branches = branchify_tree(Phylo.read(f, 'newick'), threshold)
    # noinspection PyTypeChecker
    branches = sorted(branches, key=len, reverse=True)

    i = 0  # group number
    with StdoutRedirector(args.out_file_name):
        for branch in branches:
            print(f'Group_{str(i)}_{str(len(branch))}:')
            i += 1
            for b in branch:
                print(b)
            print()


if __name__ == '__main__':
    main()
