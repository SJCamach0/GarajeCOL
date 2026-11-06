import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import json

BASE = 'http://127.0.0.1:5000'

# Test 1: Main pages return 200
pages = ['/', '/login', '/register', '/motos', '/cascos', '/ropa-y-accesorios', '/repuestos', '/comparador', '/personalizacion', '/favoritos']
print('=== TEST 1: Page Status Codes ===')
for page in pages:
    try:
        req = urllib.request.urlopen(f'{BASE}{page}')
        print(f'  OK {req.status} {page}')
    except Exception as e:
        print(f'  FAIL {page}: {e}')

# Test 2: All product images load
print('\n=== TEST 2: Product Images ===')
api = urllib.request.urlopen(f'{BASE}/api/products')
data = json.loads(api.read())
products = data['products']
img_ok = 0
img_fail = 0
for p in products:
    img_url = f'{BASE}{p["image"]}'
    try:
        req = urllib.request.urlopen(img_url)
        if req.status == 200:
            img_ok += 1
        else:
            print(f'  FAIL {req.status}: {p["name"]} -> {p["image"]}')
            img_fail += 1
    except Exception as e:
        print(f'  FAIL: {p["name"]} -> {p["image"]} ({e})')
        img_fail += 1

print(f'  Images: {img_ok} OK, {img_fail} failed out of {len(products)}')

# Test 3: Verify prices updated
print('\n=== TEST 3: Price Verification ===')
expected = {
    'AKT NKD 125': 4990000,
    'Bajaj Boxer CT 100 KS': 6199000,
    'KTM Duke 390 Gen 3': 31990000,
    'Kawasaki Ninja ZX-10R': 115990000,
    'Shaft Pro 610 DV': 450000,
    'HJC C10': 645000,
    'Pista GP RR': 5850000,
    'Guantes Shaft SH-10 Pro': 150000,
    'Chaqueta Shaft Urban Wind': 360000,
}
price_ok = 0
price_fail = 0
for p in products:
    name = p['name']
    if name in expected:
        if p['price'] == expected[name]:
            print(f'  OK {name}: {p["price_formatted"]}')
            price_ok += 1
        else:
            print(f'  MISMATCH {name}: got {p["price"]}, expected {expected[name]}')
            price_fail += 1

# Test 4: URL Samples
print('\n=== TEST 4: URL Samples ===')
url_checks = {
    'AKT NKD 125': 'aktmotos.com',
    'Bajaj Boxer CT 100 KS': 'grupouma.com',
    'KTM Duke 390 Gen 3': 'ktm-r2r.com',
    'Kawasaki Ninja ZX-10R': 'dismerca.com',
    'Shaft Pro 610 DV': 'virtualstoregp.com.co',
    'HJC C10': 'outletmotero.com.co',
}
for p in products:
    if p['name'] in url_checks:
        domain = url_checks[p['name']]
        if domain in p['official_url']:
            print(f'  OK {p["name"]}: {p["official_url"][:70]}')
        else:
            print(f'  WRONG {p["name"]}: {p["official_url"]}')

# Test 5: Detail pages load
print('\n=== TEST 5: Detail Pages (sample) ===')
for p in products[:5]:
    try:
        req = urllib.request.urlopen(f'{BASE}/producto/{p["id"]}')
        print(f'  OK {req.status} /producto/{p["id"]}')
    except Exception as e:
        print(f'  FAIL /producto/{p["id"]}: {e}')

# Test 6: No automobiles
print('\n=== TEST 6: No Automobiles ===')
all_moto = True
for p in products:
    if p['category'] not in ['motos', 'cascos', 'ropa', 'repuestos']:
        print(f'  WARNING: {p["name"]} has category {p["category"]}')
        all_moto = False
if all_moto:
    print(f'  All {len(products)} products are motorcycle-related. No automobiles.')

# Test 7: Comparator max 3
print('\n=== TEST 7: Comparator API ===')
ids = [products[0]['id'], products[1]['id'], products[2]['id']]
req_url = f'{BASE}/api/compare?ids={",".join(ids)}'
try:
    r = urllib.request.urlopen(req_url)
    cmp = json.loads(r.read())
    print(f'  OK Compare 3 products: got {len(cmp["products"])} products')
except Exception as e:
    print(f'  FAIL: {e}')

print('\n=== ALL TESTS COMPLETE ===')
