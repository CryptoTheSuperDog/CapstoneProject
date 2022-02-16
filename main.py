# This code is part of a capstone project at the Rochester Institute of Technology under advisor: Carlos Castellanos
# What this code is meant to do is use Generative Adversarial Networks in order to create a climate for the
# Trappist1-e exoplanet based off of the data we currently have on the planet and a photo-chemical model that can
# calculate all of the appropriate features for the atmosphere
import os
cwd = os.getcwd()
import numpy as np
import pandas as pd
import sys
sys.path.insert(1, f"{cwd}/timegan")
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from modules import takeData, atmos, generateData
from metrics import visualization_metrics, predictive_metrics, discriminative_metrics


if __name__ == "__main__":
    # First run atmos to calculate needed elements for analysis
    atmos("trappist1e")

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

    data = pd.read_csv(f"{cwd}/Data.txt", skiprows=3, header=None, delimiter=" ")
    temps = pd.DataFrame(data)
    seq_length = 1

    # generate new data instances
    new_data = np.array(temps).reshape((temps.shape[0], seq_length, temps.shape[1]))
    gen_data = generateData(new_data)

    # print discriminative and predictive score
    metric_iteration = 2

    discriminative_score = list()
    for _ in range(metric_iteration):
        temp_disc = discriminative_metrics.discriminative_score_metrics(new_data, gen_data)
        discriminative_score.append(temp_disc)

    print('Discriminative score: ' + str(np.round(np.mean(discriminative_score), 4)))

    # predictive_score = list()
    # for tt in range(metric_iteration):
    #     temp_pred = predictive_metrics.predictive_score_metrics(new_data, gen_data)
    #     predictive_score.append(temp_pred)
    #
    # print('Predictive score: ' + str(np.round(np.mean(predictive_score), 4)))

    # visualization of data

    # visualization_metrics.visualization(new_data, gen_data, 'pca')
    visualization_metrics.visualization(new_data, gen_data, 'tsne')
