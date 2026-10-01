
import urllib.request

urls = [
    'https://www.thyssenkrupp-steel.com/en/products/hot-strip/multiphase-steels/ferrite-bainite-phase-steel.html',
    'https://www.swisssteel-group.com/en/products/engineering-steel/bainitic-steels',
    'https://www.azom.com/article.aspx?ArticleID=6022'
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        print(f'200 OK: {url}')
    except Exception as e:
        print(f'Failed {url}: {e}')

