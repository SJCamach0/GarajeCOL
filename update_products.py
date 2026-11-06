"""
Script to update all product images, prices, and URLs for GarajeCOL.
Copies real product photos, converts to optimized JPG, and updates products.json.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import shutil
from PIL import Image

SRC_DIR = r'c:\Users\SANTIAGO\Downloads\Multimedia\Multimedia-20261105T233940Z-1-001\Multimedia'
DST_DIR = r'd:\GarajeCOL\static\images'
PRODUCTS_JSON = r'd:\GarajeCOL\data\products.json'

# Mapping: product_id -> { source_filename, new_image_name, price, price_formatted, official_url, official_store_name }
PRODUCT_UPDATES = {
    "akt-nkd-125": {
        "src": "AKT NKD 125.png",
        "img": "moto-akt-nkd.jpg",
        "price": 4990000,
        "price_formatted": "$ 4.990.000",
        "official_url": "https://aktmotos.com/motos-akt/calle/nkd-125/",
        "official_store_name": "AKT Motos Colombia Oficial"
    },
    "boxer-ct-100": {
        "src": "Bajaj Boxer CT 100 KS.png",
        "img": "moto-boxer-ct100.jpg",
        "price": 6199000,
        "price_formatted": "$ 6.199.000",
        "official_url": "https://grupouma.com/colombia/motos/boxer/boxer-ct100-es/",
        "official_store_name": "Grupo UMA Bajaj Colombia"
    },
    "ktm-duke-390": {
        "src": "KTM Duke 390 Gen 3.png",
        "img": "moto-ktm-duke390.jpg",
        "price": 31990000,
        "price_formatted": "$ 31.990.000",
        "official_url": "https://ktm-r2r.com/referencias/390-duke-generacion-3/",
        "official_store_name": "KTM R2R Colombia"
    },
    "yamaha-mt-03": {
        "src": "Yamaha MT-03.jpg",
        "img": "moto-yamaha-mt03.jpg",
        "price": 31900000,
        "price_formatted": "$ 31.900.000",
        "official_url": "https://www.incolmotos-yamaha.com.co/vehiculos/",
        "official_store_name": "Incolmotos Yamaha Oficial"
    },
    "ktm-450-exc-f": {
        "src": "KTM 450 EXC-F.png",
        "img": "moto-ktm-450.jpg",
        "price": 65990000,
        "price_formatted": "$ 65.990.000",
        "official_url": "https://www.autocolombiana.com.co/",
        "official_store_name": "Autocolombiana KTM"
    },
    "husqvarna-te-300": {
        "src": "Husqvarna TE 300.png",
        "img": "moto-husq-te300.jpg",
        "price": 64990000,
        "price_formatted": "$ 64.990.000",
        "official_url": "https://www.autocolombiana.com.co/husqvarna-te-300-2027/p",
        "official_store_name": "Autocolombiana Husqvarna"
    },
    "yamaha-wr450f": {
        "src": "Yamaha WR450F.png",
        "img": "moto-yamaha-wr450f.jpg",
        "price": 51500000,
        "price_formatted": "$ 51.500.000",
        "official_url": "https://www.incolmotos-yamaha.com.co/vehiculo/wr450f/8418/",
        "official_store_name": "Incolmotos Yamaha Oficial"
    },
    "suzuki-vstrom-650": {
        "src": "Suzuki V-Strom 650 XT.webp",
        "img": "moto-suzuki-vstrom.jpg",
        "price": 51209000,
        "price_formatted": "$ 51.209.000",
        "official_url": "https://pijaossuzuki.com/producto/v-strom-650xt-aventura/",
        "official_store_name": "Pijaos Suzuki Colombia"
    },
    "kawasaki-ninja-zx10r": {
        "src": "Kawasaki Ninja ZX-10R.png" if os.path.exists(os.path.join(SRC_DIR, "Kawasaki Ninja ZX-10R.png")) else None,
        "img": "moto-ninja-zx10r.jpg",
        "price": 115990000,
        "price_formatted": "$ 115.990.000",
        "official_url": "https://dismerca.com/referencias/kawasaki-ninja-zx-10r/",
        "official_store_name": "Dismerca Kawasaki Colombia"
    },
    "bmw-r-1250-gs": {
        "src": "BMW R 1250 GS Adventure.jpg",
        "img": "moto-bmw-gs1250.jpg",
        "price": 145000000,
        "price_formatted": "$ 145.000.000",
        "official_url": "https://www.bmw-motorrad.com.co/",
        "official_store_name": "BMW Motorrad Colombia"
    },
    "shaft-pro-610-dv": {
        "src": "Shaft Pro 610 DV.jpg",
        "img": "casco-shaft-pro.jpg",
        "price": 450000,
        "price_formatted": "$ 450.000",
        "official_url": "https://virtualstoregp.com.co/categoria-producto/cascos/shaft-pro/pro-610/",
        "official_store_name": "Virtual Store GP Colombia"
    },
    "hjc-c10": {
        "src": "HJC C10.jpg",
        "img": "casco-hjc-c10.jpg",
        "price": 645000,
        "price_formatted": "$ 645.000",
        "official_url": "https://www.outletmotero.com.co/productos/casco-hjc-c10-semi-flat-obsequio-pinlock/",
        "official_store_name": "Outlet Motero Colombia"
    },
    "agv-pista-gp-rr": {
        "src": "Pista GP RR.jpg",
        "img": "casco-agv-pista.jpg",
        "price": 5850000,
        "price_formatted": "$ 5.850.000",
        "official_url": "https://all2bikes.com/products/casco-pista-gp-rr-red-carbon",
        "official_store_name": "All2Bikes Colombia"
    },
    "shoei-x-spr-pro": {
        "src": "X-SPR Pro.jpg",
        "img": "casco-shoei-xspr.jpg",
        "price": 4800000,
        "price_formatted": "$ 4.800.000",
        "official_url": "https://www.mercadolibre.com.co/casco-moto-shoei-x-spr-pro-negro-mate-con-gorra-fxm-talla-6162-xl/p/MCO25127917",
        "official_store_name": "Shoei en MercadoLibre Colombia"
    },
    "arai-rx-7v-evo": {
        "src": "RX-7V Evo.jpg",
        "img": "casco-arai-rx7v.jpg",
        "price": 4200000,
        "price_formatted": "$ 4.200.000",
        "official_url": "https://all2bikes.com/collections/arai",
        "official_store_name": "All2Bikes Arai Colombia"
    },
    "guantes-shaft-sh10": {
        "src": "Guantes Shaft SH-10 Pro.jpg",
        "img": "guantes-shaft-sh10.jpg",
        "price": 150000,
        "price_formatted": "$ 150.000",
        "official_url": "https://www.inducascos.com/textil/guantes-para-moto/shaft?map=category-1,category-2,brand",
        "official_store_name": "Inducascos Colombia"
    },
    "chaqueta-shaft-urban": {
        "src": "Chaqueta Shaft Urban Wind.webp",
        "img": "chaqueta-shaft-urban.jpg",
        "price": 360000,
        "price_formatted": "$ 360.000",
        "official_url": "https://cascoloco.com/products/chaqueta-shaft-aeroshade-negro",
        "official_store_name": "Cascoloco Colombia"
    },
    "guantes-alpinestars-smx1": {
        "src": "Guantes Alpinestars SMX-1 Air V2.jpg",
        "img": "guantes-alpinestars-smx.jpg",
        "price": 380000,
        "price_formatted": "$ 380.000",
        "official_url": "https://skinsmoto.com/producto/guantes-alpinestars-smx1-r-air-v2/",
        "official_store_name": "Skins Moto Colombia"
    },
    "chaqueta-alpinestars-tsps": {
        "src": "Chaqueta Alpinestars T-SPS Air WP.jpg",
        "img": "chaqueta-alpinestars-tsps.jpg",
        "price": 1079910,
        "price_formatted": "$ 1.079.910",
        "official_url": "https://www.alkosto.com/chaqueta-moto-alpinestars-t-sps-v2-waterproof-negro-talla/p/8059347397436",
        "official_store_name": "Alkosto Colombia"
    },
    "alpinestars-mono-gp-plus-v4": {
        "src": "Mono GP Plus V4.jpg",
        "img": "ropa-mono-gpplus.jpg",
        "price": 5130000,
        "price_formatted": "$ 5.130.000",
        "official_url": "https://all2bikes.com/products/traje-alpinestars-gp-plus-v4-leather-suit",
        "official_store_name": "All2Bikes Colombia"
    },
    "dainese-laguna-seca-5": {
        "src": "Laguna Seca 5.jpg",
        "img": "ropa-dainese-laguna.jpg",
        "price": 6800000,
        "price_formatted": "$ 6.800.000",
        "official_url": "https://www.dainese.com/us/es/moto/hombre/monos/",
        "official_store_name": "Dainese Store Oficial"
    },
    "rst-tractech-evo-4": {
        "src": "TracTech Evo 4.jpg",
        "img": "ropa-rst-tractech.jpg",
        "price": 3550000,
        "price_formatted": "$ 3.550.000",
        "official_url": "https://skinsmoto.com/producto/mono-rst-tractech-evo-4/",
        "official_store_name": "Skins Moto Colombia"
    },
    "rep-bujia-ngk": {
        "src": "Bujía NGK Iridium IX.jpg",
        "img": "rep-bujia-ngk.jpg",
        "price": 57033,
        "price_formatted": "$ 57.033",
        "official_url": "https://www.mercadolibre.com.co/ngk-4344-ltr5ix11-bujia-iridium-ix-paquete-de-4/up/MCOU4011203652",
        "official_store_name": "NGK en MercadoLibre Colombia"
    },
    "rep-aceite-motul": {
        "src": "Aceite Motul 7100 10W40 4T.jpg",
        "img": "rep-aceite-motul.jpg",
        "price": 68500,
        "price_formatted": "$ 68.500",
        "official_url": "https://www.americanmotos.com/products/aceite-motul-7100-10w40-4t-1l",
        "official_store_name": "American Motos Colombia"
    },
    "kn-filtro-racing": {
        "src": "Filtro de Aire K&N Racing.jpg",
        "img": "rep-filtro-kn.jpg",
        "price": 361400,
        "price_formatted": "$ 361.400",
        "official_url": "https://www.auteco.com.co/filtro-de-aire-k-n-universal-alto-flujo-conico-11010515/p",
        "official_store_name": "Auteco Colombia"
    },
    "rep-pastillas-brembo": {
        "src": "Pastillas Brembo Sinterizadas CC.webp",
        "img": "rep-pastillas-brembo.jpg",
        "price": 237900,
        "price_formatted": "$ 237.900",
        "official_url": "https://www.americanmotos.com/products/pastilla-de-freno-brembo-07092",
        "official_store_name": "American Motos Colombia"
    },
    "did-kit-cadena-zvm-x": {
        "src": "Kit cadena ZVM-X Super Street.jpg",
        "img": "rep-kit-cadena-did.jpg",
        "price": 740000,
        "price_formatted": "$ 740.000",
        "official_url": "https://www.quintamotos.com.co/productos/cadena-did-zvm-x-525x130-con-x-ring-dorada-12pj1/",
        "official_store_name": "Quinta Motos Colombia"
    },
    "brembo-disco-t-drive-320": {
        "src": "Disco T-Drive 320 Competición.jpg",
        "img": "rep-disco-brembo.jpg",
        "price": 2380024,
        "price_formatted": "$ 2.380.024",
        "official_url": "https://www.brembo.com/es/moto/performance-y-racing/discos-t-drive",
        "official_store_name": "Brembo Racing Oficial"
    },
}

# Note: Kawasaki Ninja ZX-10R is not in the source photos folder
# Check if the file exists with different extensions
def find_kawasaki_src():
    for ext in ['.png', '.jpg', '.jpeg', '.webp']:
        fname = f'Kawasaki Ninja ZX-10R{ext}'
        if os.path.exists(os.path.join(SRC_DIR, fname)):
            return fname
    return None

kaw_src = find_kawasaki_src()
if kaw_src:
    PRODUCT_UPDATES["kawasaki-ninja-zx10r"]["src"] = kaw_src
    print(f"✓ Found Kawasaki source: {kaw_src}")
else:
    print("⚠ No Kawasaki Ninja ZX-10R photo found in source folder, keeping existing image")
    PRODUCT_UPDATES["kawasaki-ninja-zx10r"]["src"] = None

# Make sure destination directory exists
os.makedirs(DST_DIR, exist_ok=True)

# Step 1: Copy and optimize all images
print("\n=== STEP 1: Processing Images ===\n")
TARGET_WIDTH = 800
JPEG_QUALITY = 90

processed = 0
skipped = 0

for product_id, update in PRODUCT_UPDATES.items():
    src_file = update.get("src")
    if not src_file:
        print(f"  SKIP {product_id}: no source file")
        skipped += 1
        continue
    
    src_path = os.path.join(SRC_DIR, src_file)
    dst_path = os.path.join(DST_DIR, update["img"])
    
    if not os.path.exists(src_path):
        print(f"  MISSING {product_id}: {src_file}")
        skipped += 1
        continue
    
    try:
        img = Image.open(src_path)
        
        # Convert to RGB if necessary (for PNG with alpha, WEBP, etc.)
        if img.mode in ('RGBA', 'P', 'LA'):
            # Create white background
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if 'A' in img.mode:
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if wider than target
        w, h = img.size
        if w > TARGET_WIDTH:
            ratio = TARGET_WIDTH / w
            new_h = int(h * ratio)
            img = img.resize((TARGET_WIDTH, new_h), Image.LANCZOS)
        
        # Save as optimized JPEG
        img.save(dst_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        
        final_size = os.path.getsize(dst_path)
        print(f"  ✓ {product_id}: {src_file} → {update['img']} ({img.size[0]}x{img.size[1]}, {final_size//1024}KB)")
        processed += 1
        
    except Exception as e:
        print(f"  ERROR {product_id}: {e}")
        skipped += 1

print(f"\nImages: {processed} processed, {skipped} skipped")

# Step 2: Update products.json
print("\n=== STEP 2: Updating products.json ===\n")

with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
    products = json.load(f)

updated_count = 0
for product in products:
    pid = product["id"]
    if pid in PRODUCT_UPDATES:
        update = PRODUCT_UPDATES[pid]
        
        # Update price
        product["price"] = update["price"]
        product["price_formatted"] = update["price_formatted"]
        
        # Update URLs
        product["official_url"] = update["official_url"]
        product["official_store_name"] = update["official_store_name"]
        
        # Update image paths (unified - same image for card and detail)
        img_path = f"/static/images/{update['img']}"
        product["image"] = img_path
        product["image_large"] = img_path
        product["thumbnails"] = [img_path]
        
        updated_count += 1
        print(f"  ✓ {pid}: price={update['price_formatted']}, img={update['img']}")

# Save updated JSON
with open(PRODUCTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"\nProducts updated: {updated_count}/{len(products)}")

# Step 3: List any old images that might be cars / no longer needed
print("\n=== STEP 3: Checking for stale images ===\n")
used_images = set()
for product in products:
    used_images.add(os.path.basename(product["image"]))
    used_images.add(os.path.basename(product["image_large"]))
    for t in product.get("thumbnails", []):
        used_images.add(os.path.basename(t))

existing = set(os.listdir(DST_DIR))
unused = existing - used_images
if unused:
    print(f"  Unused images in static/images/ ({len(unused)}):")
    for f in sorted(unused):
        print(f"    - {f}")
else:
    print("  No unused images found.")

print("\n=== DONE ===")
