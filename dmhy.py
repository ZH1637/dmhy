# VERSION: 1.00
# AUTHORS: ZH (zh1140074772@gmail.com)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from html.parser import HTMLParser
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
from lxml import etree


# some other imports if necessary

class dmhy(object):

    url = 'https://share.dmhy.org'
    name = 'DMHY'
    supported_categories = {
        'all': '0'
    }

    @classmethod
    def analyze_torrent(cls, tr_list: list):
        res = []
        for tr in tr_list:
            tmp = {
                'date': tr.xpath('./td[1]/text()')[0].strip().split()[0],
                'name': ''.join(tr.xpath('./td[3]//text()')).replace('\n', '').replace('\t', ''),
                'desc_link': f"{cls.url}{tr.xpath('./td[3]/a/@href')[0]}",
                'engine_url': cls.url,
                'size': tr.xpath('./td[5]/text()')[0]
            }
            seeds = tr.xpath('./td[6]//text()')[0]
            leech = tr.xpath('./td[7]//text()')[0]
            tmp['seeds'] = int(seeds) if seeds.isalnum() else -1
            tmp['leech'] = int(leech) if leech.isalnum() else -1
            tmp[
                'link'] = f"https://dl.dmhy.org/{tmp['date']}/{tr.xpath('./td[4]/a[2]/@href')[0].split('magnet:?xt=urn:btih:')[1]}.torrent"
            res.append(tmp)
            prettyPrinter(tmp)
        return res

    def search(self, what, cat='all'):
        hits = []
        url = self.url
        page = 1

        while True:
            res = retrieve_url(f"{url}/topics/list/page/{page}?keyword={what.replace(' ', '+')}")
            tr_list = etree.HTML(res).xpath("//*[@id='topic_list']/tbody/tr")
            hits.extend(self.analyze_torrent(tr_list))
            page += 1
            if len(tr_list) < 80:
                break


if __name__ == '__main__':
    d = dmhy()
    d.search('dxd')
