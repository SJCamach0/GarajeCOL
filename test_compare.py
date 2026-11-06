import urllib.request, json
req = urllib.request.Request(
    'http://127.0.0.1:5000/api/compare',
    data=json.dumps({'ids': ['akt-nkd-125', 'boxer-ct-100', 'ktm-duke-390']}).encode(),
    headers={'Content-Type': 'application/json'}
)
r = urllib.request.urlopen(req)
d = json.loads(r.read())
print(f"Compare OK: {len(d['products'])} products returned")
for p in d['products']:
    print(f"  - {p['name']}: {p['price_formatted']}")
