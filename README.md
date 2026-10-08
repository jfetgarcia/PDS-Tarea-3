# PDS-Tarea-3
Files in this repository
| File | Tooltip |
| --- | --- |

## Dependencies
For a reproducible enviroment Conda Miniforge was used. For Linux Ubuntu, the following command was used:
```
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

## Running scripts
1.  Run the enviroment script to setup dependencies necessary for both scripts
```
conda env create -f environment.yml
conda activate pds-tarea3
```
2. Running scripts example
```
python3 <>.py
```
3. Exit enviroment
```
conda deactivate
```

## Troubleshooting
When installing the conda enviroment. The base enviroment might not activate. This can
result in the `conda` commands not being recognized. This can be fixed by running the
conda binary as follows:
```
<PATH TO MINIFORGE INSTALL>/miniforge3/bin/conda init
```
The terminal should show `(base)` at the start of the line if the conda base
enviroment was succesfully enabled.
