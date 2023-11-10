# Setup

Create virtual env, enter virtual env, install deps, setup kernel, run jupyter

```shell
python3 -m venv metrics
source ./metrics/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=metrics
pip install pandas numpy plotly nbformat
jupyter notebook
```

Now, once you've opened the notebook, go to `kernel->Change Kernel` and select `metrics`.


Now, go update your data, and get two months. Use the `analyze_awstags.py` script to generate a data set. 

For example,

```shell
python3 analyze_awstats.py awstats102022.packages.ros.org.txt > October2022.txt
python3 analyze_awstats.py awstats102023.packages.ros.org.txt > October2023.txt
    ```

