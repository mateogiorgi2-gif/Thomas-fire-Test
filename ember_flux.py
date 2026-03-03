#!/usr/bin/env python3

import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.crs import CRS
import os

def read_ember_flux_data_bil(ember_flux_raster_path, band=None, agg=True, draw_flux=True):
    with rasterio.open(ember_flux_raster_path) as src:
        dst_crs = 'EPSG:4326'
        transform, width, height = calculate_default_transform(
            CRS.from_epsg(26911), dst_crs, src.width, src.height, *src.bounds)
        res = src.transform.a

        plot_data = np.empty((height, width), dtype=src.meta['dtype'])
        if band is not None:
            data = src.read(band)
        else:
            data = src.read()

        data = np.nan_to_num(data, nan=0.0)

        if agg:
            data = np.sum(data, axis=0)
        if draw_flux:
            data = data / res / res

        reproject(
            source=data,
            destination=plot_data,
            src_transform=src.transform,
            src_crs=CRS.from_epsg(26911),
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )

        left, bottom = transform * (0, height)
        right, top = transform * (width, 0)
        data_extent = [left, right, bottom, top]
        return plot_data, data_extent

# === User-defined paths ===
case_root = "/home/yqin123/scratch/ELMFIRE_SIMU/CasesForThesis/8_ThomasFire_WNGUST_FBFMO30_EU_WUE"
ember_flux_raster_path = os.path.join(case_root, 'scratch', 'ember_flux_0000001_0136808.bil')
npz_data_path = os.path.join(case_root, 'outputs', 'ember_flux.npz')

print("Starting ember flux post-processing...")
agg = True

# Process all 900 bands
for i in range(900):
    print(f"Processing band {i+1}/900")
    try:
        ember_flux_data, data_extent = read_ember_flux_data_bil(
            ember_flux_raster_path, band=i+1, agg=False, draw_flux=True
        )
    except Exception as e:
        print(f"Stopped at band {i+1}: {e}", flush=True)
        break

    if i == 0:
        ember_flux_data_transient = np.zeros((900, ember_flux_data.shape[0], ember_flux_data.shape[1]), dtype=np.float32)
        ember_flux_data_transient[i, :, :] = ember_flux_data
        ember_flux_data_all = ember_flux_data
    else:
        ember_flux_data_transient[i, :, :] = ember_flux_data
        ember_flux_data_all += ember_flux_data

# Save results
np.savez_compressed(npz_data_path,
    ember_flux_data_all=ember_flux_data_all,
    ember_flux_data_transient=ember_flux_data_transient,
    data_extent=data_extent
)
print(f"Saved output to {npz_data_path}")

