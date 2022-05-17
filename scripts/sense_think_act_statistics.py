#!/usr/bin/env python3

import argparse
import os
from urllib.parse import unquote

MIN_DATA_THRESHOLD = 0.001

def count_d(res):
    return -1 * res.count_downloads()

class Results:
    def __init__(self, episode):
        self.counts = {}
        self.bandwidths = {}
        self.name = episode
    def add_month(self, month, count, bandwidth):
        if month in self.counts:
            self.counts[month] += count
        else:
            self.counts[month] = count
        if month in self.bandwidths:
            self.bandwidths[month] += bandwidth
        else:
            self.bandwidths[month] = bandwidth

    def count_downloads(self):
        total = 0
        for _, count in self.counts.items():
            total += count
        return total

    def count_bandwidth(self):
        total = 0
        for _, bandwidth in self.bandwidths.items():
            total += bandwidth
        return total


def get_episode_from_url(basename_beginning):
    url_elements = basename_beginning.split('/')
    if not url_elements[-1].endswith('.mp3'):
        print("not an mp3: %s" % basename_beginning)
        return None
    
    episode = unquote(url_elements[-1].split('.')[0])
    return episode

parser = argparse.ArgumentParser(description="process awstats files")
parser.add_argument('filename', help="filename to load", type=str, nargs='+')


args = parser.parse_args()

print("Loading %s" % args.filename)

results = {}
other_packages = {}


AWSTATS_DOWNLOAD_SECTION = {
    '6.9': 'SIDER',
    '7.4': 'DOWNLOADS'
}

for filename in args.filename:

    with open(filename, 'r') as fh:
        inside = False
        skipped_lines = 0
        processed_lines = 0
        awstats_version = None
        month = None

        for line in fh:
            if not awstats_version:
                if not awstats_version and 'AWSTATS DATA FILE' in line:
                    awstats_version = line.split()[3]
                    continue

                if not month and 'FirstTime' in line:
                    month = line.split()[1][0:5]
                    continue

            # print("processing line %s" % line)
            if not inside and 'BEGIN_%s ' % AWSTATS_DOWNLOAD_SECTION[awstats_version] in line:
                inside = True
                continue
            if inside and ('END_%s' % AWSTATS_DOWNLOAD_SECTION[awstats_version]) in line:
                inside = False
                continue
            if not inside:
                skipped_lines += 1
                # print("SKIPPED, not inside")
                continue
            if not '/sensethinkact/' in line:
                skipped_lines += 1
                # print("SKIPPED", line)
                continue
            elements = line.strip().split()
            if len(elements) < 4:
                print("Too few elemnts in %s" % elements)
                # print("line: %s" % line)
                skipped_lines += 1
                continue
            # print("processed", line)

            processed_lines += 1

            url = elements[0]
            episode = get_episode_from_url(url)

            count = int(elements[1])
            hits = int(elements[2])
            bandwidth = int(elements[3])/1024/1024/1024


            if episode in results:
                results[episode].add_month(month, count + hits, bandwidth)
            else:
                rosdistro = "none"
                results[episode] = Results(episode)
                results[episode].add_month(month, count + hits, bandwidth)
                # print("hello %s" % beg)


s = sorted(results.values(), key=count_d)
for i in range(0, min(100000, len(results))):
    print("%s: %s Downloads and  %.2f GB" % (s[i].name, s[i].count_downloads(), s[i].count_bandwidth()))

# print(results.keys())

total_downloads = 0
total_bandwidth = 0
for r in results.values():
    total_downloads += r.count_downloads()
    total_bandwidth += r.count_bandwidth()



print("Number of different episodes: %s" % len(results))
print("total downloads: %s" % total_downloads)
print("total bandwitdh: %.2f GB" % total_bandwidth)

