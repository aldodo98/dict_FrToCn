词典筛选策略：
1. 爬虫爬取下来的数据进行匹配：
	a.拿24s为例，会以sku为匹配标准，确保中法翻译一一对照
2. 爬虫在输出数据前对数据进行粗筛选：
	a..粗筛选步骤1：将中法名字划分为单个词条，中文中出现的单词如果有没有翻译的，在法语原文中标记，比如Jupe crayon，假如crayon没有翻译，直接译为crayon连衣裙，则最后的词典中的词条为{jupe:连衣裙}，所有的单词都会以小写的形式
	b.粗筛选步骤2：中文名中出现不存在于原法语名称的法语单词，标记为无效数据
		如：robe claire：clear裙，为无效数据
	c.粗筛选步骤3：中文中存在未知字符时，认为网站自身翻译错误，标记为无效数据
		如：robe claire：%#@裙，为无效数据
	d.粗筛选步骤4：翻译时翻译为非中文语言时，认为网址自身翻译错误，标记为无效数据
		如：robe claire：クリアドレス，为无效数据
3.在sql工具中对数据进行第二次粗筛选:
	a.将所有法语以及其中文翻译中相同的字段合并，然后根据其中文翻译出现的频率，保留频率最高的字段
	b.将得到的视图保存为json格式
4.人工细筛选：
	a.清除明显错误的翻译
	b.清除有未识别符号的：比如-，无法在最初阶段识别
	c.清除单位：比如mg，ml
	d.翻译为不同语言但没有识别到的
	e.品牌名称在原网站中没有翻译的：Sandro étole，长围巾。清除Sandro
5.数据量：商品总数2w+，最后词条≈4.7k
6.词典种类对照：总共有六个种类：accessoires 配饰, beaute 美妆, bijoux 首饰, chaussures 鞋子, pretaporter 成衣,sac 包包