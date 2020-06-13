# -*- coding: utf-8 -*

import exifread
import argparse
import os
import glob
import time
from datetime import datetime

FIELD = 'EXIF DateTimeOriginal'
FILES = []

def check_repeat(dt_str):
    for it in FILES:
        if dt_str == it:
            return True
    return False

# 解析命令行参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--indir", type=str, help="photos directory")
args = vars(ap.parse_args())

# 参数错误
if args["indir"] is None:
    print("--indir error!")
    exit()

try:
    # 加载jpg文件
    paths = glob.glob(os.path.join(args['indir'], '*.jpg'))
    s = int(time.time())
    new_name = ""
    for p in paths:
        tags = exifread.process_file(open(p,'rb'))        
        if FIELD in tags:
            new_name = datetime.strptime(str(tags[FIELD]), '%Y:%m:%d %H:%M:%S').strftime('%Y%m%d_%H%M%S')
        else:        
            new_name = os.path.splitext(p)[0]

        if check_repeat(new_name):
            print(int(time.time()) - s)
            new_name = new_name + '.' + str(int(time.time() - s))

        n = os.path.join(args["indir"], (new_name + '.jpg'))
        os.rename(p, n)
        FILES.append(new_name)
        print("old={}, new={}".format(p, n))
except:
    print(new_name)