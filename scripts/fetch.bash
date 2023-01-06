rsync -ave ssh ros@ros1.osuosl.org:~/awstats/* . --bwlimit 5000 --progress --partial
rsync -ave ssh ros@ros1.osuosl.org:/var/www/wiki.ros.org/data/edit-log . --bwlimit 5000 --progress --partial
