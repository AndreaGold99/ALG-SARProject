# version 1.1
import argparse
import pickle
import sys

from SAR_lib import SAR_Project


def syntax():
    print("python %s indexfile [-s] [query | -l query_list]" % sys.argv[0])
    #print(sys.argv)
    sys.exit()


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Search the index.')

    parser.add_argument('index', metavar='index', type=str,
                        help='name of the file with the index object.')

    parser.add_argument('-S', '--stem', dest='stem', action='store_true', default=False, 
                    help='use stem index by default.')

    parser.add_argument('-th', '--threshold',dest='threshold', metavar='th', type=int,
                    help = 'threshold to use in case to look up similar terms,\
                    only useful with "--trie" option or "--ntrie option". Default value is 3',default=3)
    parser.add_argument("-D", "--distance", dest="distance", metavar="distance", type=str,
                        choices=["levenshtein", "restricted", "intermediate"],\
                        help="distance algorithm to use to similar retrieval. default value is levensthein. choose from [\"levensthein\", \"restricted\", \"intermediate\"]", default="levenshtein")

    group0 = parser.add_mutually_exclusive_group()
    
    group0.add_argument('-N', '--snippet', dest='snippet', action='store_true', default=False, 
                    help='show a snippet of the retrieved documents.')

    group0.add_argument('-C', '--count', dest='count', action='store_true', default=False, 
                    help='show only the number of documents retrieved.')

    parser.add_argument('-A', '--all', dest='all', action='store_true', default=False, 
                    help='show all the results. If not used, only the first 10 results are showed. Does not apply with -C and -T options.')

    parser.add_argument('-R', '--rank', dest='rank', action='store_true', default=False, 
                    help='rank results. Does not apply with -C and -T options.')


    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-Q', '--query', dest='query', metavar= 'query', type=str, action='store',
                    help='query.')
    group1.add_argument('-L', '--list', dest='qlist', metavar= 'qlist', type=str, action='store',
                    help='file with queries.')
    group1.add_argument('-T', '--test', dest='test', metavar= 'test', type=str, action='store',
                    help='file with queries and results, for testing.')

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("-TR", "--trie",dest='trie',action='store_true',
                        default=False,help="use Trie for retrieval of similar terms in case the desired term.\
                        it's not present")
    group2.add_argument("-NTR", "--notrie", dest="notrie", action="store_true",
                        default=False,help="dont use trie for retrieve")
    args = parser.parse_args()

    with open(args.index, 'rb') as fh:
        searcher = pickle.load(fh)

    searcher.set_stemming(args.stem)
    searcher.set_ranking(args.rank)
    searcher.set_showall(args.all)
    searcher.set_snippet(args.snippet)
    searcher.set_trie(args.trie)
    searcher.set_vocab(args.notrie)
    searcher.set_distance(args.distance)
    searcher.set_threshold(args.threshold)
    # se debe contar o mostrar resultados?
    if args.count is True:
        fnc = searcher.solve_and_count
    else:
        fnc = searcher.solve_and_show

    if args.test is not None:
        # opt: -T, testing

        with open(args.test, encoding='utf-8') as fh:
            lines = fh.read().split('\n')
            for line in lines:
                if len(line) > 0 and not line.startswith('#'):
                    query, reference = line.split('\t')
                    reference = int(reference)
                    result = searcher.solve_and_count(query)
                    if result != reference:
                        print("==> ERROR: '%s'\t%d\t%d" % (query, result, reference))
                        sys.exit(-1)
                else:
                    print(line)
            print('\nParece que todo ha ido bien, buen trabajo!')

    elif args.query is not None:
        # opt: -Q, una query pasada como argumento
        fnc(args.query) # searcher.solve_and_show(args.query)

    elif args.qlist is not None:
        # opt: -L, una lista de queries
        with open(args.qlist, encoding='utf-8') as fh:
            queries = fh.read().split('\n')
            queries.pop()
            for query in queries:
                if len(query) > 0 and not query.startswith('#'):
                    fnc(query)
                else:
                    print(query)
    else:
        # modo interactivo
        query = input("query:")
        while query != "":
            fnc(query)
            query = input("query:")
