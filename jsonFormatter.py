from anytree import AnyNode, RenderTree
from anytree.importer import JsonImporter
from anytree.exporter import DictExporter
from collections import OrderedDict
from pprint import pprint
import json

PATH = "./"

def writeToJSON(fileName, data):
    filePathNameWExt = PATH + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)

def readFromJSON(fileName):
	json_data=open(PATH + fileName).read()
	return json_data

def tree_toJSON(tree):
    exporter = DictExporter()
    pprint(exporter.export(tree))
    tree_in_json = exporter.export(tree)
    return tree_in_json

def JSON_toTree(json_data):
    importer = JsonImporter()
    ITSM_tree = importer.import_(json_data)
    print(RenderTree(ITSM_tree))
    return ITSM_tree
