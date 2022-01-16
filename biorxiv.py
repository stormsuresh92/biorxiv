from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm


s = HTMLSession()

data = []
urls = ['https://www.biorxiv.org/collection/cancer-biology?page={}'.format(x) for x in range(1, 51)]
for url in tqdm(urls):
	r = s.get(url)
	content = r.html.find('div.highwire-cite.highwire-cite-highwire-article.highwire-citation-biorxiv-article-pap-list-overline.clearfix')
	for item in tqdm(content):
		ti = item.find('span.highwire-cite-title', first=True).text
		author = item.find('span.highwire-citation-authors', first=True).text
		meta = item.find('span.highwire-cite-metadata-pages.highwire-cite-metadata', first=True).text
		link = 'https://www.biorxiv.org' + item.find('a.highwire-cite-linked-title', first=True).attrs['href']
		dic = {
			'Title':ti,
			'Author':author,
			'Date':meta,
			'Link':link
		}
		data.append(dic)

df = pd.DataFrame(data)
df.to_csv('biorxiv.csv', index=False)