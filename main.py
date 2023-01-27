from nltk.stem import PorterStemmer
import argparse
from pathlib import Path

# functions

from index.auxiliaries import *

def main(file):
    # Load data from json file containing URLS
    data = load_data(file)

    # Initialise stemmer
    stemmer = PorterStemmer()

    # Create index
    index, pos_index, stats = create_index(data, stemmer)

    # Save non positionnal index in a json
    save_index(index, "mon_stemmer.title.non_pos_index.json")

    # Save positionnal index in a json
    save_index(index, "mon_stemmer.title.pos_index.json")

    # Save stats in a json
    save_stats(stats, "metadata.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'SimpleWebIndex',
                    description = 'Builds a simple webindex out of an url json file',
                    epilog = 'Good luck, sometimes it works.')

    parser.add_argument('filename')

    args = parser.parse_args()
    
    main(args.filename)