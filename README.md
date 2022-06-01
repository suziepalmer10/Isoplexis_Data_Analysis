# Isoplexis Data Analysis - Suzette Palmer (Zhan and Koh labs)

## Installation

### Clone Isoplexis Github Repository

```
git clone https://github.com/suziepalmer10/Isoplexis_Data_Analysis.git
```

### Installation

1. Create a virtual environment:

- On Biohpc: 

```
module add python/3.8.x-anaconda
python -V
conda create -n isoplexis python=3.8.8 ipykernel
source activate isoplexis

```

- On Local System (Mac/Linux) 

```
python3 -m venv isoplexis

```


2. Update pip and install required libraries 

```
python -m pip install --upgrade pip
python -m pip install dash  pandas numpy scipy dash-bootstrap-components matplotlib seaborn sklearn statsmodels 

```
3. Activate virtual environment

- On Biohpc: 

```
module add python/3.8.x-anaconda
source activate isoplexis

```

- On Local System (Max/Linux)

```
source venv/bin/activate

```
