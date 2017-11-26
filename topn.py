'''
Created on Nov 26, 2017

@author: blcarlson
'''
import os
import json
import codecs
from collections import OrderedDict

TOPN = 200

def write_json(data, filename):
    with open(filename, 'w') as outfile:  
        json.dump(data, outfile)

def write_md(language, items, filename):
    with codecs.open(filename, "a", "utf-8") as f:
        f.write('\n#### {language}\n'.format(language=language))

        for item in items['site']:            
            title = item['title']
            description = item['description']
            tdate = item['date']
            url = item['url']
            f.write(u"* [{title}]({url}) (Trending on {date}):{description}\n".format(title=title, url=url, date=tdate, description=description))


def main():
    path_to_json = os.getcwd().replace('src','') + '/'#github-trending/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print(json_files)
    
    data = {}
    for json_file in json_files:
        with open(path_to_json+json_file) as data_file:
            data[json_file.replace('.json','')] = json.load(data_file)
        
    data = OrderedDict(sorted(data.items(), key=lambda t: t[0],reverse=True))
    url_list = []
    top_list = {}
    top_list['site'] = [] 
    for entry in data:
        print entry
        items = data[entry]['site']
        for item in items:
            url = item['url']
            if(url not in url_list and url_list.__len__() <= TOPN):
                url_list.append(item['url'])
                item['date']= entry
                top_list['site'].append(item)
                
    file_md = 'top'+TOPN.__str__()+'.md'
    file_json = 'top'+TOPN.__str__()+'.json'

    try:
        os.remove(file_md)
        os.remove(file_json)
    except OSError:
        pass
    
    
    write_md('Java Top '+TOPN.__str__(), top_list, file_md)
    write_json(top_list, file_json)
    print(file_md)
    print(file_json)
    print("COMPLETE")

if __name__ == '__main__':
    main()