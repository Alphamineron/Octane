# Standard Libraries
import sys

# CLI Libraries
import pprint
import colorama
import argparse
from tqdm import tqdm
from utils.spinner import Spinner

# Data Libraries
import pandas as pd
import datadotworld as dw


DATASET_URL = "alphamineron/medium-bookmarks"


def fetch_dataset(DATASET_URL = DATASET_URL):
    """
        Fetchs the data.world dataset from the given url path using dw.load_dataset()

        The load_dataset() function facilitates maintaining copies of datasets on the
        local filesystem. It will download a given dataset's datapackage and store it
        under ~/.dw/cache. When used subsequently, load_dataset() will use the copy
        stored on disk and will work offline, unless it's called with force_update=True
        or auto_update=True.

        force_update=True will overwrite your local copy unconditionally.
        auto_update=True will only overwrite your local copy if a newer version of the dataset is available on data.world.

        Returns
        -------
        `datadotworld.models.dataset.LocalDataset` object

    """
    sys.stdout.write("\n> Fetching bookmarks from: https://data.world/" + DATASET_URL + " -> ")
    with Spinner():
        dataset = dw.load_dataset(DATASET_URL, auto_update=True)
        print("\n")

    if args.verbose:
        colorama.init(autoreset = True)
        print(colorama.Fore.BLACK + colorama.Back.YELLOW + "\n Local Dataset Info: " + "---"*23, "\n")

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(dataset.describe())
        print("\n", dataset.dataframes)

        print(colorama.Fore.BLACK + colorama.Back.YELLOW + "\n" + "---"*30)

    return dataset

def sync_dataset(DATASET_URL = DATASET_URL):
    sys.stdout.write("\n> Syncing files at: https://data.world/" + DATASET_URL + " -> ")
    with Spinner():
        api_client = dw.api_client()
        api_client.sync_files(DATASET_URL)
        print("\n")

def pd_clean_col(mediumDF):
    """
        Removes dublicate columns such as bookmarkedat, posturl, posttitle.

        Returns
        -------
        `pandas.core.frame.DataFrame` object : Cleaned Dataframe
    """
    mediumDF = mediumDF[["bookmarked_at", "post_url" ,"post_title"]]  # Select Specific Columns
    print(mediumDF.info())

    return mediumDF

def main():
    sync_dataset()

    dataset = fetch_dataset()
    mediumDF = dataset.dataframes["medium_bookmarks"]
    mediumDF = pd_clean_col(mediumDF)

    # print(mediumDF.shape)
    print("\n", mediumDF)





if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("-v", "--verbose",
                            help="Show more detailed information",
                            action="store_true")
    args = argparser.parse_args()
    main()
















# TODO: EXTRA ROBUSTNESS - Make the script able to detect multiple files within a dataset that contain medium data
    # for df in dataset.dataframes.values():
    #     print(df.columns.values.tolist())
