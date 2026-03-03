#!/bin/bash
#SBATCH -t 3-00:00:00
#SBATCH --mem-per-cpu=20480
#SBATCH --account atrouve-prj-eng
#SBATCH --ntasks 1
# Load necessary modules
module purge
module load swig
module load python/gcc/11.3.0/ 
module load gdal
module load jupyter

# Start Jupyter Notebook on the compute node
pip install rasterio

echo "Starting Python script at $(date)"
python -u ember_flux.py
echo "Job finished at $(date)"


exit 0
