import requests
import json
import os
from scrapy.selector import Selector


lua_script = """
function main(splash)
    splash:go("https://www.youtube.com/results?search_query=gaoxiao")
    splash:wait(2)
    splash:runjs("var circle = setInterval(function(){scrollTo(1, 1000000)}, 500)")
    splash:wait(10)
    splash:runjs("clearInterval(circle)")
    return splash:html()
end
"""

splash_url = 'http://localhost:8050/execute'
headers = {'content-type': 'application/json'}
data = json.dumps({'lua_source': lua_script})
response = requests.post(splash_url, headers=headers, data=data)
sel = Selector(response)
video_url = sel.xpath('//*[@id="thumbnail"]/@href').extract()
already_download = []
for single_video in video_url:
    if single_video not in already_download:
        already_download.append(single_video)
        download_url = 'https://www.youtube.com' + single_video
        os.system(f'youtube-dl -f 22 {download_url}')
