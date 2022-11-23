These are helpful scripts designed to assist in the generation of the ROS metrics report and other visualizations of ROS metrics and trends.

ROS Metrics are posted here: https://wiki.ros.org/Metrics

# To get recent stats

* SSH into OSU and run `update.bash`

```
ssh ros@osuoslros
bash update.bash
```

* Now you can pull down the data files locally for analysis using the fetch script in the scripts directory

```
./fetch.bash

```

* Alternatively you can pull down a single month using:

```
rsync -ave ssh osuoslros:~/awstats/awstats<MM><YYYY>.packages.ros.org.txt . --bwlimit 500 --progress --partial
rsync -ave ssh osuoslros:~/awstats/awstats<MM><YYYY>.downloads.ros.org.txt . --bwlimit 500 --progress --partial
```

* Summarize the stats using `analyze_awstats.py` in the scripts directory. 

```
./analyze_awstats.py awstats082022.packages.ros.org.txt
```


