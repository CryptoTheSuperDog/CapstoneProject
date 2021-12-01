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
    # takeData(13, "out.out")

    data = pd.read_csv("C:/Users/Administrator/PycharmProjects/Trappist_Climate_Code/Data.txt",
                       skiprows=3, header=None, delimiter=" ")
    temps = pd.DataFrame(data[1])

    # generate new data instances
    generateData(temps)

# TODO: get our data pre-processed correctly for timegan
# TODO: change all file paths from hardcoded to os method of getting base directory and then adding other file paths
