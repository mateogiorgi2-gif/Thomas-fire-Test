#!/bin/bash
#SBATCH -t 3-00:00:00
#SBATCH --mem-per-cpu=20480
#SBATCH --account atrouve-prj-eng
#SBATCH --ntasks 1
module purge
module load openmpi/4.1.1/gcc/
module load cuda/gcc/9.4.0/
module load curl/gcc/9.4.0/
module load gdal/3.4.0/gcc/
module load python

# ELMFIRE_VER=${ELMFIRE_VER:-2023.1015}

SCRATCH=./scratch
INPUTS=./inputs
OUTPUTS=./outputs

rm -f -r $SCRATCH $OUTPUTS 
mkdir $SCRATCH $OUTPUTS

# cp $ELMFIRE_BASE_DIR/build/source/fuel_models.csv $MISC
# cp $ELMFIRE_BASE_DIR/build/source/building_fuel_models.csv $MISC

# echo $CELLSIZE | python input_generator.py
cp elmfire.data.in $INPUTS/elmfire.data
# cp $ELMFIRE_BASE_DIR/build/source/fuel_models.csv $MISC
A_SRS="EPSG: 26910" # Spatial reference system - UTM Zone 10

# Execute ELMFIRE
# mpirun -np 1 elmfire_debug $INPUTS/elmfire.data > IGNITED_BY_FIREBRANDS.txt
mpirun -np 1 elmfire_debug $INPUTS/elmfire.data
# elmfire_debug ./inputs/elmfire.data


exit 0
