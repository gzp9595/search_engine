# -*- coding: utf-8 -*-

from Doc2vec import *

if __name__ == '__main__':
	engine = Doc2vec(save_path = './model')
	text = '江苏省徐州市云龙区人民法院\b刑 事 判 决 书\b（2016）苏0303刑初340号\b公诉机关徐州市云龙区人民检察院。\b被告人张某某，男。2011年4月1日因吸毒被连云港市公安局新浦分局行政拘留十日，并处罚款人民币2000元。2012年11月9日因吸毒被连云港市公安局新浦分局行政拘留十日，并处罚款人民币2000元，同时被责令接受社区戒毒三年。2013年1月25日因吸毒被连云港市公安局新浦分局行政拘留十五日，并处罚款人民币2000元，同时被决定强制戒毒二年。2016年1月19日因吸毒被连云港市公安局海州分局行政拘留十五日，并处罚款人民币2000元，同时被决定强制戒毒二年。2016年1月21日因涉嫌贩卖毒品罪被徐州市公安局云龙分局刑事拘留，2016年2月3日经徐州市云龙区人民检察院批准逮捕，次日由该分局执行逮捕。现羁押于徐州市看守所。\b被告人神某某，男。2009年8月13日因吸毒被徐州市公安局鼓楼分局行政拘留十五日。2012年12月8日因吸毒被徐州市公安局鼓楼分局行政拘留十五日，并被责令接受社区戒毒三年。2013年3月18日因吸毒被徐州市公安局公共交通治安分局行政拘留十五日，并被决定强制隔离戒毒二年。2015年12月31日因涉嫌贩卖毒品罪被徐州市公安局云龙分局刑事拘留，2016年2月3日经徐州市云龙区人民检察院批准逮捕，次日由该分局执行逮捕。现羁押于徐州市看守所。\b被告人吴某某，男。2015年7月4日因吸毒被徐州市公安局泉山分局行政拘留十五日（未执行），并被责令接受社区戒毒三年。2015年12月31日因涉嫌贩卖毒品罪被徐州市公安局云龙分局取保候审，2016年3月30日经徐州市云龙区人民检察院决定取保候审，同日由该分局执行取保候审。\b徐州市云龙区人民检察院以云检诉刑诉[2016]345号起诉书指控被告人张某某、神某某、吴某某犯贩卖毒品罪，于2016年9月29日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。徐州市云龙区人民检察院指派检察员李铁林出庭支持公诉。被告人张某某、神某某、吴某某到庭参加诉讼。现已审理终结。\b经审理查明：\b2015年8月至12月，被告人张某某、神某某、吴某某分别在江苏省连云港市、徐州市等地贩卖甲基苯丙胺（冰毒）。'
	text1 = '广东省广州市增城区人民法院\b刑 事 判 决 书\b（2016）粤0183刑初1442号\b公诉机关广东省广州市增城区人民检察院。\b被告人张某，居民，户籍地址广东省广州市增城区。被告人张某因吸毒于2009年5月26日被原增城市公安局行政拘留，同年6月10日被强制隔离戒毒。因本案于2016年6月23日被羁押，同月23日被刑事拘留，同年7月15日被逮捕，同年7月15日由广州市公安局增城区分局决定对被告人张某取保候审。\b广东省广州市增城区人民检察院以穗增检诉刑诉[2016]1402号起诉书指控被告人张某、单某乙犯贩卖毒品罪，于2016年11月29日向本院提起公诉。本院受理后，依法组成合议庭，公开开庭审理了本案。广东省广州市增城区人民检察院检察员张芸出庭支持公诉，被告人张某、单某乙到庭参加诉讼。后公诉机关于2017年1月20日以证据发生变化为由撤回对被告人单某乙的起诉，本院于同月22日裁定准许。现已审理终结。\b广东省广州市增城区人民检察院指控，2016年6月15日9时许，吸毒人员曾某乙通过电话联系被告人张某向其购买170元毒品海洛因，后又通电话联系单某乙让其从被告人张某处拿毒品，并承诺一起吸食。单某乙明知是毒品交易，仍驾驶粤E×××××小汽车去到广州市增城区荔城街莲花市场从被告人张某处拿了一包毒品海洛因，并答应帮被告人张某向曾某乙收取毒资人民币170元，后携带上述毒品驾车到增城区中新镇恒大上水成221栋802房，将上述毒品海洛因交给曾某乙并一起吸食。后单某乙及吸毒人员曾某乙在该小区停车场被公安人员抓获。在曾某乙身上查获剩余的部分毒品白色粉末1包（经检验，净重0.02克，检出海洛因成分）。2015年6月23日，被告人张某在其住处被公安人员抓获，现场缴获毒品白色固体1包（经检验，净重0.45克，检出海洛因成分）。\b公诉机关认为，被告人张某的行为已构成贩卖毒品罪，鉴于被告人张某归案后如实供述其罪行，依法可从轻处罚。提请本院依照《中华人民共和国刑法》第三百四十七条第一款、第四款、第六十七条第三款的规定对被告人张某判处刑罚。\b被告人张某对公诉机关指控的事实无异议，并承认控罪。\b经审理查明，2016年6月15日9时许，吸毒人员曾某乙通过电话联系被告人张某向其购买170元毒品海洛因（0.3克）后，再电话联系单某乙让其从被告人张某处带毒品。后单某乙驾驶粤E×××××小汽车去到广州市增城区荔城街莲花市场找到被告人张某，从被告人张某处拿了一包毒品海洛因并携带到增城区中新镇恒大上水成221栋802房交给曾某乙。当天中午13时许，单某乙、曾某乙在该小区停车场被公安人员抓获，在曾某乙身上查获剩余的部分毒品白色粉末1包（经检验，净重0.02克，检出海洛因成分）。2015年6月23日，被告人张某在其住处被公安人员抓获，现场缴获毒品白色固体1包（经检验，净重0.45克，检出海洛因成分）。\b上述事实，有下列由公诉机关当庭出示，经控、辩双方质证，经本院予以确认的证据证实：\b1、受案登记表、立案决定书，证实公安机关对本案依法立案侦查。\b2、抓获经过、归案说明，证实被告人张某于2016年6月23日17时被拘传到案。\b3、被告人张某的户籍材料，证实被告人张某已达到刑事责任年龄。\b4、现场勘验笔录、现场图及现场照片，证实现场位于增城区中新镇恒大上水成221栋地下停车场。\b5、搜查笔录、扣押笔录、扣押清单，证实公安机关于2016年6月15日现场扣押白色粉末1包、Farreri型手机1台、VIVO型Y35手机1台、荣威350牌小车（车牌为粤E×××××）。\b6、搜查笔录、扣押决定书，证实2016年6月23日17时公安人员在被告人张某住处（广州市增城区荔城街莲花市场10栋一楼和二楼保安宿舍）缴获毒品疑似物1包（毛重约1克）、铁盒1个、浅绿色手机1台。'
        print "init"	
	em0 = engine.get_embedding(text = text, mode = 0)
	em1 = engine.get_embedding(text = text, mode = 1)
	em2 = engine.get_embedding(text = text, mode = 2)
	em3 = engine.get_embedding(text = text, mode = 3)
	em4 = engine.get_embedding(text = text, mode = 4)

	em01 = engine.get_embedding(text = text1, mode = 0)
	em11 = engine.get_embedding(text = text1, mode = 1)
	em21 = engine.get_embedding(text = text1, mode = 2)
	em31 = engine.get_embedding(text = text1, mode = 3)
	em41 = engine.get_embedding(text = text1, mode = 4)

	print engine.get_similarity(embedding1 = em0, embedding2 = em01, mode = 0)
	print engine.get_similarity(embedding1 = em1, embedding2 = em11, mode = 1)
	print engine.get_similarity(embedding1 = em2, embedding2 = em21, mode = 2)
	print engine.get_similarity(embedding1 = em3, embedding2 = em31, mode = 3)
	print engine.get_similarity(embedding1 = em4, embedding2 = em41, mode = 4)
