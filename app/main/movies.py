import json
import subprocess
from os import path

class Movies():
    def __init__( self ):
        self.contents = []

    def getContent(self, content):
        d = path.dirname(__file__)
        outfile = path.join(d, "movie/movies.json")
        fo = open(outfile, "r+")
        fo.truncate()
        fo.close()
        subprocess.run('scrapy crawl movie -o movies.json -t json', shell=True, cwd=path.join(d, "movie"))
        with open(outfile) as json_file:
            data = json.load(json_file)
            for x in data:
                info = '%s\n%s' % (x['movie_title'], x['movie_link'])
                self.contents.append({'type':'text', 'content':info})

        # result = ''
        # tmplen = 0
        # random.shuffle(contentlist)
        # for x in contentlist:
        #     tmplen += len(x)
        #     if tmplen > 1022:
        #         break
        #     if result != '':
        #         result += '\n\n'
        #     result += x
        #     tmplen = len(result)

        return self.contents
