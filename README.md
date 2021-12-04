# CapstoneProject

This repository is part of my capstone project in the preliminary stages. We are modeling the climate of the exo-planet TRAPPIST1-e with the intention of subjecting organisms and microbes to the environment using a climate chamber. We will be using a climate modeling package written in Fortran called [Atmos](https://github.com/VirtualPlanetaryLaboratory/atmos) and a time series GAN model called [TimeGans](https://github.com/jsyoon0823/TimeGAN). The data for the parameters to input into the input file of can be found [here](http://exoplanet.eu/catalog/trappist-1_e/).

# Packages and Environment
All of the code is going to be written in python but there are specific versions needed. Also there is some fortran code that Atmos must run so a fortran compiler is needed as well. 
* Python(3.7) because tensorflow 1.15.0 is being used in TimeGan and any other version after 3.7 can not install it. Tensorflow has depreciated some functions
* tensorflow 1.15.0
* numpy>=1.17.2
* tqdm>=4.36.1
* argparse>=1.1
* pandas>=0.25.1
* scikit-learn>=0.21.3
* matplotlib>=3.1.1
* Any fortran compiler (I used [gfortran](https://gcc.gnu.org/wiki/GFortranBinaries))

# Run Current code
I need to change the hardcoded directories in the code, once I do that this line will disappear. First make sure all programs are in the same directory. 
Create a template for the planet in the atmos/PHOTOCHEM/INPUTFILES/TEMPLATES. Specificly you want to copy and edit an existing PLANET.dat folder.
When the code is run, a bash shell script from atmos is run and then a shell will pop up prompting for a planet template. Enter the planet model you saved in the template folder, followed by y,y,n,n. 
That should get an atmos output and then the code will do the rest. Enjoy!
