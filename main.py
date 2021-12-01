# This code is part of a capstone project at the Rochester Institute of Technology under advisor: Carlos Castellanos
# What this code is meant to do is use Generative Adversarial Networks in order to create a climate for the
# Trappist1-e exoplanet based off of the data we currently have on the planet and a photo-chemical model that can
# calculate all of the appropriate features for the atmosphere

import sys
import pandas as pd
from typing import TextIO
from modules import takeData, atmos, generateData
sys.path.insert(1, "C:/Users/Administrator/timegan")
sys.path.insert(2, "C:/Users/Administrator/atmos")
sys.path.insert(3, "C:/Users/Administrator/timegan/metrics")
from timegan import timegan
from metrics import discriminative_metrics
from predictive_metrics import predictive_score_metrics
from visualization_metrics import visualization
from data_loading import MinMaxScaler


if __name__ == "__main__":
    # First run atmos to calculate needed elements for analysis
    atmos("mars")

    # Tables names of the out.out file, no commas or lowercase or special characters in title
    table_names: dict = {1: " MIXING RATIOS OF LONG",
                         2: " PHOTOLYSIS RATES",
                         3: " ENERGY FLUXES IN W",
                         4: " NUMBER DENSITIES OF LONG",
                         5: " AQUEOUS PHASE SPECIES",
                         6: " NORMAL HENRYS LAW COEFFICIENTS",
                         7: " ENHANCEMENTS OF HENRYS LAW COEFFICIENTS",
                         8: " GIORGI AND CHAMEIDES RAINOUT RATES",
                         9: " RAINOUT RATE",
                         10: " CONSERVATION OF SULFUR",
                         11: " INTEGRATED REACTION RATES",
                         12: " PHOTOCHEMICAL EQUILIBRIUM AND INERT SPECIES",
                         13: " ATMOSPHERIC PARAMETERS",
                         14: " SULFATE AEROSOL PARAMETERS",
                         15: " S",  # S8 AEROSOL PARAMETERS
                         }

    # Grab the specific data from the out.out file that we need for the new climates
    takeData(13,  "out.out", table_names)

    data = pd.read_csv("C:/Users/Administrator/PycharmProjects/Trappist_Climate_Code/Data.txt",
                       skiprows=3, header=None, delimiter=" ")
    temps = pd.DataFrame(data[1])

    # generate new data instances
    generateData(temps)

# TODO: get our data pre-processed correctly for timegan
# TODO: change all file paths from hardcoded to os method of getting base directory and then adding other file paths
