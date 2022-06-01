#build virtual environment
mkdir Isoplexis && cd Isoplexis
python3 -m venv venv

#activate virtual environment
source venv/bin/activate

#install required libraries dash and pandas
python -m pip install --upgrade pip
python -m pip install dash  pandas numpy scipy dash-bootstrap-components matplotlib seaborn sklearn statsmodels 
python -m pip install matplotlib seaborn
python -m pip install statsmodels 

python -m pip install sklearn
#dash-bio 

#make python script app.py
touch app.py

#go into app.py to write script

#activate virtual environment
source venv/bin/activate



