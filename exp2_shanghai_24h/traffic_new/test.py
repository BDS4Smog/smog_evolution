# -*- coding: utf-8 -*-
import jieba


a = u"粗发！为了不堵车！[打哈气]"

seg = jieba.cut(a)
for s in seg:
	print s.encode('utf-8')

