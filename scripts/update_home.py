#!/usr/bin/env python3
"""更新首页 description 与「阅读今日日报」按钮链接。"""
import re
import sys

path, desc, ym, date = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

with open(path, encoding="utf-8") as f:
    content = f.read()

content = re.sub(r"^description:.*$", "description: " + desc, content, count=1, flags=re.M)
content = re.sub(r'link="/\d{4}-\d{2}/\d{4}-\d{2}-\d{2}"', 'link="/%s/%s"' % (ym, date), content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("首页已更新: %s/%s" % (ym, date))
