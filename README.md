# Satellite-to-satellite SPM research data

Research data accompanying **The potential and advantages of obtaining diverse training data solely from satellite observations: Evidence from estimating suspended particulate matter concentrations in Japanese lakes**.

Authors: Chenlu Zhang and Bunkei Matsushita, University of Tsukuba.

## Contents

| Directory | Contents |
| --- | --- |
| `data/dataset_i` | 348 retained in-situ–OLCI matchups, measured SPM, OLCI spectra and stored Mai25 estimates |
| `data/dataset_ii` | 692,100 retained satellite-to-satellite records with training, validation and independent-test assignments |
| `data/dataset_iii` | Independent Japanese lake validation observations, censoring strings, satellite inputs and stored predictions |
| `data/independent_test` | Stored predictions for the independent test lakes in Dataset II |
| `models` | Four frozen sensor-specific model checkpoints and configuration/feature metadata |
| `metadata` | Sample counts, source citations and source-file checksums |
| `scripts` | Scripts for calculating validation metrics and verifying file checksums |

## Sample counts

| Sensor | Retained Dataset II | Training | Validation | Independent test | Dataset III total | Field SPM >=1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S2 | 371592 | 266532 | 66633 | 38427 | 896 | 721 |
| L7 | 133771 | 94386 | 23596 | 15789 | 577 | 427 |
| L8 | 131579 | 94438 | 23610 | 13531 | 431 | 347 |
| L9 | 55158 | 37710 | 9428 | 8020 | 142 | 117 |

## Reading the data

All tabular data are UTF-8 CSV compressed with gzip. Standard Python, R, and other analysis tools can read these files directly. For example, `pandas.read_csv("data/dataset_ii/S2_training_matchups.csv.gz")`.

`data_dictionary.csv` documents the retained fields. Original field names and numeric values are preserved.

SPM concentrations are in g m^-3, numerically equal to mg L^-1. In Dataset I, `SPM` is the measured concentration and `mai` is the stored OLCI estimate. In Dataset II, `SPM` is the satellite-derived training target, not an in-situ measurement. Land-sensor reflectance columns follow the manuscript's Level-2 surface reflectance divided by pi convention. OLCI Rrs comes from C2RCC.

Dataset III preserves `SS` (including original censoring text), `SS2` (numeric measurement), and `pred_spm` (the manuscript model prediction). Quantitative evaluation uses SS2 >=1 and finite positive predictions. Records below the reporting threshold retain their original censoring notation. Benchmark predictions are recorded under the source column names.

Dataset II's `source_row_0based` identifies the original data row before cleaning; the corresponding original Excel row is this index plus 2. `split` is the frozen membership and must not be reshuffled when reproducing the stored results. Independent-test `src_row` refers to that original source row.

## Version and model identity

The data and checkpoints correspond to the original Japanese-lake analysis. The S2 model uses eight spectral bands and six mixture components; its independent field-validation MdAPD is 39.9333%. Checkpoint configuration and input-band order are provided for all four sensors.

Mai25 implementation: the clear-water absorption term was evaluated using ln rather than log10. The deposited estimates and model checkpoints were produced with this implementation.

Model architecture and feature order are recorded in `models/checkpoint_metadata.json`. The `.pt` files contain the original model and scaling state. The scripts reproduce validation statistics from the stored predictions; a training environment is not included.

## Verification

Python 3.10 or later is sufficient; no third-party package is required:

```sh
python scripts/check_integrity.py
python scripts/verify_validation.py
```

Expected Dataset III MdAPD percentages are 39.933276 (S2), 56.274939 (L7), 46.938083 (L8), and 49.211951 (L9). Dataset I has N=348, RMSD(log10)=0.326773 and MdAPD=32.958323%.

The scripts operate on stored predictions and do not retrain the models.

## Data sources and reuse

Source citations are listed in `metadata/data_sources.json`. Please cite the study and the original datasets when reusing these records. Source datasets remain subject to the terms of their respective providers. Contact the corresponding author for reuse enquiries concerning derived materials.

## Citation

Use the metadata in `CITATION.cff`. The associated article has not been assigned a publication DOI in this deposit.

## Contact

Bunkei Matsushita, Institute of Life and Environmental Sciences, University of Tsukuba: matsushita.bunkei.gn@u.tsukuba.ac.jp.
