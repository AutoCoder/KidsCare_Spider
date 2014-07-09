'''
Created on 2014.6.12

@author: HELI
'''
import json
import codecs

# normalized_dest_List = {}
# with open("destination_list.json") as file:
# 	normalized_dest_List = json.load(file)
# 	
# uncompleteList = codecs.open("uncomplete_list.txt", 'a','utf-8')
	
# class SpiderUtility(object):
# 	'utilities for spider'
# 	
# 	@staticmethod 
# 	def compare(dest):
# 	    return dest[u"ID"]
# 	
# 	@staticmethod 
# 	def normalize_city(destination):
# 		id = []
# 		for dest in destination:
# 			if normalized_dest_List.has_key(dest):
# 				id.append(normalized_dest_List[dest])
# 			else:
# 				uncompleteList.write(dest+u'\n')
# 		id.sort(key=SpiderUtility.compare)
# 		if id:
# 			id_str = str(id[0][u'ID'])
# 			for subitem in id[1:]:
# 				id_str += "-"
# 				id_str += str(subitem[u'ID'])
# 			return id_str;
# 		else:
# 			return ""
			