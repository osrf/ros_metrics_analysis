# How to run Jupyter in a venv

Create the venv
```
python -m venv metrics
source ./metrics/bin/activate
```

Intstall your deps 
```
pip3 install pandas numpy plotly pygithub ipykernel
```

Run this command
```
python3 -m ipykernel install --user --name=metrics --display-name "METRICS"
```


