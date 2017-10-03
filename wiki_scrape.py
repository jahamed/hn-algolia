import requests
import credentials
import pdb
import codecs
from tqdm import tqdm

params = {
	'query' : 'en.wikipedia.org',
	'restrictSearchableAttributes' : 'url',
	'tags' : 'story',
	'hitsPerPage' : 20,
	'page' : 0
}

try:
 r = requests.get('http://hn.algolia.com/api/v1/search_by_date', params=params)

 pdb.set_trace()

 if r.status_code == requests.codes.ok:
	output_file = codecs.open("wiki_links.txt", "w", encoding="utf-8-sig")
	r_json = r.json()
	nbPages = r_json['nbPages']
 	nbHits = r_json['nbHits']
 	r_urls = set()
 	r_dupe_urls = set()

 	# make a request for every page of results
 	print("Requesting data from Algolia...")
 	for i in tqdm(range(params['page'], nbPages)):
 		params['page'] = params['page'] + 1
		r = requests.get('http://hn.algolia.com/api/v1/search_by_date', params=params)

		# extract urls from each page, dedupe them
		for hit in r.json()['hits']:
			url = hit['url']
			if url in r_urls:
				r_dupe_urls.add(url)
			else:
				r_urls.add(url)

	for s in r_urls:
		output_file.write(s + '\n')

	print("# of duplicate urls {}".format(len(r_dupe_urls)))
	for s in r_dupe_urls:
		print(s)

	output_file.close()
except requests.exceptions.RequestException as e:
	print(e)
	sys.exit(1)

