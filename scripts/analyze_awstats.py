#!/usr/bin/env python

import argparse
import os

UBUNTU_DISTROS = ['precise', 'quantal', 'raring', 'saucy', 'trusty', 'utopic', 'vivid', 'wily', 'xenial', 'yakkety', 'zesty', 'artful', 'bionic', 'cosmic', 'disco', 'eoan', 'focal','jammy']
DEBIAN_DISTROS = ['jessie', 'stretch', 'buster', 'bullseye']
OS_DISTROS = UBUNTU_DISTROS + DEBIAN_DISTROS
ARCHES = ['i386', 'amd64', 'armhf', 'arm64', 'source']
ROS1_DISTROS = ['boxturtle', 'cturtle', 'diamondback', 'electric', 'fuerte', 'groovy', 'hydro', 'indigo', 'jade', 'kinetic', 'lunar', 'melodic', 'noetic']
ROS2_DISTROS = ['ardent', 'bouncy', 'crystal', 'dashing', 'eloquent', 'foxy', 'galactic', 'humble','iron']
ROS2_ROLLING_DISTROS = ['rolling']

ROS_DISTROS = ROS1_DISTROS + ROS2_DISTROS + ROS2_ROLLING_DISTROS

MIN_DATA_THRESHOLD = 0.001

def count_d(res):
    return -1 * res.count_downloads()

class Results:
    def __init__(self, package, rosdistro):
        self.urls = {}
        self.name = package
        self.rosdistro = rosdistro
    def add_url(self, url, count):
        if url in self.urls:
            self.urls[url] += count
        else:
            self.urls[url] = count

    def count_downloads(self, arch=None, distro=None):
        total = 0
        for url, count in self.urls.items():
            if not arch or arch == get_arch_from_url(url):
                if not distro or distro == get_distro_from_url(url):
                    total += count
        return total

def get_beginning_url(url):
    if not url.endswith('.deb') and not url.endswith('.dsc'):
        #print("not a debian package %s" % url)
        return None
    bn = os.path.basename(url)
    #print("bn %s" % bn)
    return bn.split('_')[0]
    
def get_arch_from_url(url):
    if url.endswith('.dsc'):
        return 'source'
    if not url.endswith('.deb'):
        #print("not a debian package %s" % url)
        return None
    bn = os.path.basename(url)
    bn = bn[:-4]
    # print("bn %s" % bn)
    return bn.split('_')[-1]
    
def get_distro_from_url(url):
    """ Detect which distro we're using. This implementation has the potentila to overmatch."""
    for distro in OS_DISTROS:
        if distro in url:
            return distro
    return None

def get_package_info_from_url(basename_beginning):
    name_elements = basename_beginning.split('-')
    if len(name_elements) < 3:
        # print("package name too short: %s" % basename_beginning)
        return None
    if name_elements[0] != 'ros':
        print("not a ros package name: %s" % basename_beginning)
        return None

    distro = name_elements[1]
    return distro

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
        shadow_fixed = 0
        awstats_version = None
        for line in fh:
            if not awstats_version:
                if 'AWSTATS DATA FILE' in line:
                    awstats_version = line.split()[3]
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
            if '/ros-shadow-fixed' in line:
                shadow_fixed += 1
                # print("SKIPPED, shadow_fixed")
                continue
            if '/ros2-testing' in line:
                shadow_fixed += 1
                # print("SKIPPED, ros2-testing")
                continue
            elements = line.strip().split()
            if len(elements) < 4:
                print("Too few elemnts in %s" % elements)
                # print("line: %s" % line)
                skipped_lines += 1
                continue
            processed_lines += 1

            url = elements[0]
            count = int(elements[1])
            # print("url %s" % url)
            beg = get_beginning_url(url)
            arch = get_arch_from_url(url)
            if not beg:
                #print("failing here %s --- %s" % (beg, url))
                continue
            rosdistro = get_package_info_from_url(beg)
            # print("%s -- %s" % (rosdistro, beg))
            if beg in results:
                results[beg].add_url(url, count)
            else:
                results[beg] = Results(beg, rosdistro)
                results[beg].add_url(url, count)
                # print("hello %s" % beg)


s = sorted(results.values(), key=count_d)
for i in range(0, min(100000, len(results))):
    if s[i].name[0:3] == 'ros' or s[i].name[0:3] == 'pyt' :
        print("%s: %s" % (s[i].name, s[i].count_downloads()))




# non_hydro = [r for r in results.values() if r.rosdistro != 'hydro']

total_downloads = 0
for r in results.values():
    total_downloads += r.count_downloads()

unique_urls = 0
for r in results.values():
    unique_urls += len(r.urls)

arch_stats = {}
archdistro_stats = {}
rd_stats = {}
print("Breakdown by rosdistro:")
for rd in ROS_DISTROS:
    rd_stats[rd] = sum([r.count_downloads() for r in results.values() if r.rosdistro == rd]) * 100.0/total_downloads
    print("%s: %.2f %%" % (rd, rd_stats[rd]))
print("Breakdown by Arch:")
for arch in ARCHES:
    arch_stats[arch] = sum([r.count_downloads(arch) for r in results.values()]) * 100.0/total_downloads
    print("%s: %.2f %%" % (arch, arch_stats[arch]))
    for distro in OS_DISTROS:
        archdistro = '%s_%s' % (distro, arch)
        archdistro_stats[archdistro] = sum([r.count_downloads(arch=arch, distro=distro) for r in results.values()]) * 100.0/total_downloads

print("Results larger than %s%%" % MIN_DATA_THRESHOLD)
for k, v in sorted(archdistro_stats.items()):
    if v > MIN_DATA_THRESHOLD:
        print("%s: %.2f %%" % (k, v))

print("Unique debian package versions: %s" % unique_urls)
print("Number of different packages: %s" % len(results))
print("total deb downloads: %s" % total_downloads)
print("skipped lines: %s" % skipped_lines)
print("processed lines: %s" % processed_lines)
print("shadow_fixed lines skipped: %s" % shadow_fixed)
