import sys
import os
os_path = os.getcwd()
sys.path.append(os_path)

from scrapy.cmdline import execute

execute(["scrapy", "crawl", "cnblogs"])
