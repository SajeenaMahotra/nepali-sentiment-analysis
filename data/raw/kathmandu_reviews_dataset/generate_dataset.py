"""
Synthetic Code-Mixed Romanized Nepali-English E-Commerce Review Dataset
=======================================================================
Generator v2 — 100,000 rows, expanded template & slot space.

Project: "Sentiment Analysis of Code-Mixed Nepali-English Product Reviews
on a Local Online Marketplace based in Kathmandu"

Design changes over v1 (2,500 rows):
  - Product catalogue expanded from ~46 to ~200 SKUs across 10 categories.
  - Each sentiment has FIVE fragment pools instead of three:
        opener  →  product_aspect  →  delivery_aspect  →  service_aspect  →  closer
    A review picks from any subset of these (1–5 fragments), giving
    much higher combinatorial diversity.
  - Slot-based body templates: phrases like "{aspect} {quality} cha" are
    expanded against tables of 30+ aspects × 20+ qualities × 10+ intensifiers,
    yielding tens of thousands of unique body phrases per sentiment.
  - Mixed-sentiment reviews (~8%): positive product / negative delivery,
    or vice-versa — reflects real Nepali e-commerce reviews.
  - Schema is identical (22 columns) — drop-in replacement for v1.

Reproducibility: random.seed(42).
"""
import csv
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUT = Path("/home/claude/marketplace_v2")
OUT.mkdir(exist_ok=True, parents=True)

# ===========================================================================
# 1. EXPANDED PRODUCT CATALOGUE  — ~200 SKUs across 10 categories
# ===========================================================================
CATEGORIES: dict[str, list[tuple]] = {
    "Mobiles & Tablets": [
        ("Samsung Galaxy A15 5G", 28999, "Samsung"),
        ("Samsung Galaxy A25 5G", 33999, "Samsung"),
        ("Samsung Galaxy M14", 17999, "Samsung"),
        ("Samsung Galaxy S23 FE", 65990, "Samsung"),
        ("Samsung Galaxy Tab A9", 24999, "Samsung"),
        ("Redmi Note 13 Pro", 34500, "Xiaomi"),
        ("Redmi Note 13", 23999, "Xiaomi"),
        ("Redmi 13C", 16999, "Xiaomi"),
        ("Xiaomi Pad 6", 49990, "Xiaomi"),
        ("Realme Narzo 70", 22999, "Realme"),
        ("Realme C53", 15999, "Realme"),
        ("Realme 11 Pro", 38999, "Realme"),
        ("iPhone 13 (Refurbished)", 79999, "Apple"),
        ("iPhone 14 128GB", 119900, "Apple"),
        ("iPhone 11 64GB", 65990, "Apple"),
        ("iPad 9th Gen 64GB", 56990, "Apple"),
        ("Oppo A78 4GB/128GB", 25990, "Oppo"),
        ("Oppo A98 5G", 35990, "Oppo"),
        ("Oppo Reno 10", 49990, "Oppo"),
        ("Vivo Y28 6GB/128GB", 26499, "Vivo"),
        ("Vivo Y100 5G", 32999, "Vivo"),
        ("Vivo V29e", 41990, "Vivo"),
        ("Nokia G42 5G", 31000, "Nokia"),
        ("Nokia C32", 12999, "Nokia"),
        ("Tecno Spark 20", 18499, "Tecno"),
        ("Tecno Camon 20", 27999, "Tecno"),
        ("Infinix Hot 30", 17999, "Infinix"),
        ("Infinix Note 30", 23999, "Infinix"),
    ],
    "Electronics & Accessories": [
        ("boAt Rockerz 450 Headphone", 3299, "boAt"),
        ("boAt Airdopes 141", 2499, "boAt"),
        ("Mi Power Bank 20000mAh", 2799, "Xiaomi"),
        ("Mi Power Bank 10000mAh", 1799, "Xiaomi"),
        ("JBL Go 3 Bluetooth Speaker", 4999, "JBL"),
        ("JBL Tune 510BT", 7999, "JBL"),
        ("Realme Buds Air 5", 4599, "Realme"),
        ("Anker USB-C Fast Charger 20W", 2199, "Anker"),
        ("Anker Soundcore Mini Speaker", 3499, "Anker"),
        ("Logitech M170 Wireless Mouse", 1599, "Logitech"),
        ("Logitech K380 Keyboard", 5990, "Logitech"),
        ("HP DeskJet 2331 Printer", 8999, "HP"),
        ("HP 15s Laptop", 78990, "HP"),
        ("TP-Link Archer C20 Router", 3199, "TP-Link"),
        ("TP-Link TL-WR841N Router", 1899, "TP-Link"),
        ("Apple AirPods Pro 2", 32990, "Apple"),
        ("Apple Lightning Cable 1m", 2299, "Apple"),
        ("Sony WH-CH520 Headphones", 8990, "Sony"),
        ("Mi Band 8", 4499, "Xiaomi"),
        ("Noise ColorFit Pulse 2", 3499, "Noise"),
        ("Lenovo IdeaPad Slim 3", 65990, "Lenovo"),
        ("Asus VivoBook 15", 71990, "Asus"),
        ("Western Digital 1TB HDD", 5499, "WD"),
        ("Sandisk Ultra 64GB Pendrive", 999, "SanDisk"),
        ("Sandisk Ultra 32GB MicroSD", 549, "SanDisk"),
    ],
    "Fashion - Men": [
        ("Levis 511 Slim Fit Jeans", 4500, "Levis"),
        ("Levis 511 Black Jeans", 4700, "Levis"),
        ("Nike Revolution 6 Running Shoes", 7800, "Nike"),
        ("Nike Air Max SC", 11990, "Nike"),
        ("Adidas Cotton Round Neck T-Shirt", 1899, "Adidas"),
        ("Adidas Adilette Slides", 2799, "Adidas"),
        ("Bata Formal Leather Shoes", 3299, "Bata"),
        ("Bata Power Sneakers", 2499, "Bata"),
        ("Goldstar G10 Sports Shoes", 1499, "Goldstar"),
        ("Goldstar Trekking Shoes", 1990, "Goldstar"),
        ("Puma Sling Bag (Black)", 2199, "Puma"),
        ("Puma Cotton Polo T-Shirt", 2599, "Puma"),
        ("Wrangler Slim Fit Jeans", 3990, "Wrangler"),
        ("UCB Half Sleeve Shirt", 2799, "UCB"),
        ("Allen Solly Formal Trouser", 2999, "Allen Solly"),
        ("Peter England Shirt", 2499, "Peter England"),
        ("Reebok Classics Sneakers", 5990, "Reebok"),
        ("Skechers GoWalk 5", 7990, "Skechers"),
        ("Hidesign Leather Wallet", 3299, "Hidesign"),
        ("Tommy Hilfiger Belt", 3990, "Tommy"),
    ],
    "Fashion - Women": [
        ("Cotton Kurta Set (Pink)", 1899, "Generic"),
        ("Cotton Kurta Set (Blue)", 1899, "Generic"),
        ("Anouk Floral Top", 1299, "Anouk"),
        ("Anouk Embroidered Kurta", 1899, "Anouk"),
        ("Daraz Mall Saree (Banarasi)", 4499, "Generic"),
        ("Daraz Mall Saree (Silk)", 5990, "Generic"),
        ("Lakme Eyeconic Kajal", 425, "Lakme"),
        ("Lakme 9 to 5 Lipstick", 599, "Lakme"),
        ("Maybelline Fit Me Foundation", 850, "Maybelline"),
        ("Maybelline Lash Sensational Mascara", 750, "Maybelline"),
        ("Nivea Soft Light Moisturizer", 320, "Nivea"),
        ("Nivea Body Lotion 400ml", 525, "Nivea"),
        ("Forever 21 Crop Top", 1499, "Forever 21"),
        ("Zara Pleated Skirt", 2999, "Zara"),
        ("Vero Moda Maxi Dress", 3499, "Vero Moda"),
        ("Biba Anarkali Suit", 4999, "Biba"),
        ("W For Woman Tunic", 1999, "W"),
        ("Mochi Block Heels", 2799, "Mochi"),
        ("Catwalk Flats", 1499, "Catwalk"),
        ("Hidesign Leather Sling Bag", 4990, "Hidesign"),
    ],
    "Home & Lifestyle": [
        ("Prestige IRIS 750W Mixer Grinder", 4799, "Prestige"),
        ("Prestige Induction Cooktop", 3999, "Prestige"),
        ("Pigeon Favourite 1.5L Pressure Cooker", 1899, "Pigeon"),
        ("Pigeon Stainless Steel Kadhai", 1499, "Pigeon"),
        ("Milton Thermosteel Flask 1L", 1450, "Milton"),
        ("Milton Tiffin 4-Container", 1299, "Milton"),
        ("CG 32-inch LED TV", 21500, "CG"),
        ("CG 43-inch Smart TV", 35990, "CG"),
        ("Hometown 2-Seater Sofa", 24990, "Hometown"),
        ("Nilkamal Plastic Chair", 1099, "Nilkamal"),
        ("Nilkamal Storage Box 30L", 899, "Nilkamal"),
        ("Philips Air Fryer 4.1L", 12990, "Philips"),
        ("Philips Hand Blender", 3999, "Philips"),
        ("Bajaj Ceiling Fan", 3499, "Bajaj"),
        ("Bajaj Iron 1000W", 1599, "Bajaj"),
        ("Havells Stand Fan", 4990, "Havells"),
        ("Eveready Rechargeable Lamp", 1799, "Eveready"),
        ("Cello H2O Bottle 1L", 449, "Cello"),
        ("Borosil Glass Set 6pc", 1099, "Borosil"),
        ("Tupperware Lunch Box", 899, "Tupperware"),
    ],
    "Books & Stationery": [
        ("Atomic Habits (Paperback)", 599, "Penguin"),
        ("Karnali Blues by Buddhi Sagar", 450, "Fineprint"),
        ("Palpasa Cafe by Narayan Wagle", 350, "Nepalaya"),
        ("Seto Dharti by Amar Neupane", 500, "Fineprint"),
        ("Sumnima by BP Koirala", 250, "Sajha"),
        ("Faber-Castell Sketch Pen Set", 320, "Faber-Castell"),
        ("Classmate Notebook 200 Pages", 145, "Classmate"),
        ("Classmate Spiral Notebook", 175, "Classmate"),
        ("Apsara Drawing Pencil 10pc", 85, "Apsara"),
        ("Reynolds 045 Ball Pen 5pc", 75, "Reynolds"),
        ("Cello Butterflow Pen Pack", 60, "Cello"),
        ("Camlin Geometry Box", 195, "Camlin"),
        ("The Psychology of Money", 599, "Harriman"),
        ("Rich Dad Poor Dad", 449, "Plata"),
        ("Ikigai (Hardcover)", 699, "Hutchinson"),
    ],
    "Groceries": [
        ("Wai Wai Chicken Pack of 30", 750, "Chaudhary Group"),
        ("Wai Wai Veg Pack of 30", 720, "Chaudhary Group"),
        ("Tulsi Mustard Oil 5L", 1450, "Tulsi"),
        ("Tulsi Mustard Oil 1L", 320, "Tulsi"),
        ("Himalayan Spring Water 20L Jar", 250, "Himalayan"),
        ("Bisleri Water 1L", 30, "Bisleri"),
        ("Nepal Tea Premium 500g", 525, "Nepal Tea"),
        ("Tokla CTC Tea 500g", 440, "Tokla"),
        ("Nescafe Classic 100g Jar", 525, "Nescafe"),
        ("Nestle Maggi 70g (12-pack)", 350, "Nestle"),
        ("Daawat Basmati Rice 5kg", 1850, "Daawat"),
        ("Annapurna Atta 10kg", 1150, "Annapurna"),
        ("DDC Milk Powder 500g", 425, "DDC"),
        ("Dabur Real Mango Juice 1L", 220, "Dabur"),
        ("Heinz Tomato Ketchup 1kg", 345, "Heinz"),
    ],
    "Beauty & Health": [
        ("Himalaya Face Wash Neem", 199, "Himalaya"),
        ("Himalaya Anti-Hairfall Shampoo", 285, "Himalaya"),
        ("Dabur Amla Hair Oil 200ml", 285, "Dabur"),
        ("Dabur Vatika Shampoo 200ml", 245, "Dabur"),
        ("Colgate MaxFresh Toothpaste", 150, "Colgate"),
        ("Colgate Visible White", 175, "Colgate"),
        ("Sensodyne Toothpaste 75g", 245, "Sensodyne"),
        ("Dettol Soap (Pack of 4)", 240, "Dettol"),
        ("Dettol Antiseptic Liquid 250ml", 195, "Dettol"),
        ("Lifebuoy Soap (Pack of 4)", 165, "Lifebuoy"),
        ("Pond's Cold Cream 100g", 225, "Ponds"),
        ("Pond's White Beauty Cream", 290, "Ponds"),
        ("Head & Shoulders Shampoo 340ml", 485, "P&G"),
        ("Patanjali Aloe Vera Gel 150ml", 145, "Patanjali"),
        ("Patanjali Dant Kanti", 75, "Patanjali"),
        ("Vicks VapoRub 50ml", 195, "Vicks"),
        ("Whisper Sanitary Pads (Pack of 14)", 265, "P&G"),
        ("Stayfree Secure XL", 195, "Stayfree"),
    ],
    "Baby & Toys": [
        ("Pampers Premium Care Pants L", 1299, "Pampers"),
        ("Pampers Active Baby Diapers M", 999, "Pampers"),
        ("Huggies Wonder Pants M", 925, "Huggies"),
        ("Cerelac Wheat Apple Cherry", 425, "Nestle"),
        ("Cerelac Rice 300g", 395, "Nestle"),
        ("Lactogen Stage 2 Formula", 885, "Nestle"),
        ("Lego Classic Bricks Set", 3499, "Lego"),
        ("Lego City Police Set", 4999, "Lego"),
        ("Hot Wheels 5-Pack Cars", 1299, "Hot Wheels"),
        ("Barbie Fashionista Doll", 1499, "Barbie"),
        ("Funskool UNO Card Game", 599, "Funskool"),
        ("Funskool Stack-up Toy", 749, "Funskool"),
    ],
    "Sports & Outdoor": [
        ("SG Cricket Bat (Kashmir Willow)", 3999, "SG"),
        ("Cosco Football Size 5", 999, "Cosco"),
        ("Yonex Mavis 350 Shuttlecock", 1399, "Yonex"),
        ("Yonex GR-303 Badminton Racket", 1899, "Yonex"),
        ("Decathlon Domyos Yoga Mat", 1499, "Decathlon"),
        ("Decathlon Quechua 30L Backpack", 1999, "Decathlon"),
        ("Wildcraft Hypadura 35L", 3499, "Wildcraft"),
        ("Speedo Swim Goggles", 1799, "Speedo"),
        ("Yonex Tennis Racket Pro", 4990, "Yonex"),
        ("Rockrider ST 30 MTB", 24990, "Rockrider"),
    ],
}

# Expanded sellers list (mirrors real Nepali marketplace seller variety)
SELLERS = [
    "Daraz Mall", "Sastodeal Official", "Hamrobazar Verified",
    "Kathmandu Electronics", "New Road Mobile Hub", "Putalisadak Store",
    "Bhatbhateni Online", "Big Mart Express", "Gyan Mandir Bookhouse",
    "Pokhara Trading", "Boudha Boutique", "Lalitpur Lifestyle",
    "Newroad Fashion House", "Asan Bazaar Online", "Thamel Tech World",
    "Babarmahal Beauty", "Patan Style", "Kalanki Kitchenware",
    "Maharajgunj Mart", "Chabahil Collections", "Kupondole Crafts",
    "Sundhara Selections", "Naxal Niche", "Tinkune Trends",
    "Sanepa Supplies", "Jawalakhel Junction", "Bansbari Boulevard",
    "Damkal Deals", "Ekantakuna Emporium", "Pulchowk Plaza",
]

LOCATIONS = [
    "Kathmandu", "Lalitpur", "Bhaktapur", "Pokhara", "Biratnagar",
    "Birgunj", "Butwal", "Chitwan", "Dharan", "Hetauda", "Janakpur",
    "Nepalgunj", "Itahari", "Banepa", "Dhulikhel", "Bharatpur",
    "Damak", "Tikapur", "Tulsipur", "Ghorahi",
]
LOCATION_WEIGHTS = [42, 14, 6, 8, 3, 2, 3, 4, 2, 3, 2, 2, 3, 3, 3, 3, 1, 1, 1, 1]

PAYMENT_METHODS = ["Cash on Delivery", "eSewa", "Khalti", "IME Pay", "Card", "ConnectIPS", "FonePay"]
PAYMENT_WEIGHTS = [50, 18, 13, 5, 7, 3, 4]

DELIVERY_PARTNERS = [
    "Daraz Express", "Aramex", "Pathao", "InDriver Logistics",
    "Nepal Can Move", "Local Courier", "Tootle Delivery", "DHL Nepal",
]

# ===========================================================================
# 2. EXPANDED TEMPLATE POOLS — 5 fragment slots per sentiment
# ===========================================================================
# Slots: opener, product_aspect, delivery_aspect, service_aspect, closer.
# A review composes a random subset (always opener + 1-4 of the others).

# ---- POSITIVE -------------------------------------------------------------
POS_OPENERS = [
    "Wow, ekdam ramro product cha!", "Maile yo {product} order gareko thiye, satisfied chu.",
    "Ekdam khusi laagyo yo product paera.", "Highly recommended! Quality dherai ramro cha.",
    "Best purchase of the year ho yo!", "Bhanchu k bhanu, ekdam top notch cha samaan.",
    "Yesto quality yo price ma kaha pauchhau hai!", "Mero expectation bhanda dherai ramro aayo.",
    "Genuine product cha, packaging pani neat.", "Worth every rupee, pasinaa ko paisa khera gayena.",
    "Ekdam mast cha yaar, friends lai pani recommend gareko.", "Order garna naparekai bhayena, perfect samaan.",
    "Fully satisfied! Seller le ramro service diyo.", "Original branded product cha, sabai labels ramrosanga match cha.",
    "Sasto ma ramro, ke chai!", "Photo ma jasto thiyo, exactly tyestai aayo.",
    "Trust gariyo, ra dhokha pani bhayena.", "Product is super and delivery was on time, very happy!",
    "Yo product ko quality bhanne kura nai chaina, perfect cha.",
    "First time order gareko, but ekdam impressed chu.", "Babal product ho, paisa wasted bhayena.",
    "Quality ra value dubai bhetiyo yo product ma.", "Sale ma kineko thiye, but original aayo ekdam khushi.",
    "Bro yesto quality yo budget ma vetnu mushkil cha!",
    "Imported jasto feel auncha, super product.", "Premium feel garauchha hat ma rakhda nai.",
    "Description ra reality match bhayo, ramro lagyo.", "Yo seller bata kineko thiye pheri pheri kinchhu.",
    "Excellent! 10/10 from my side.", "Amazing quality, dherai khushi chu.",
    "Pakkai try garnu hola yo, tikai cha.", "Solid product ho yaar, full performance cha.",
    "Babal samaan ho, paisa anusar bhanda dherai value cha.", "Maile yo {product} kineko, life-saver bhayo.",
    "Honest review: product ekdam genuine ra ramro cha.",
    "Yo daam ma yesto quality? Babal dil ma chuyo!", "Loved the quality, exceeded my expectations!",
    "Salute to the seller, dherai ramro packing.", "Yesto seller le market ma trust banauchha.",
    "Wholeheartedly recommend, koi pani niraash hudaina.",
]

POS_PRODUCT = [
    "Quality top class, finishing pani neat ra clean.", "Battery backup ramro cha, full din chal cha.",
    "Sound quality ekdam crisp, bass pani powerful.", "Fitting perfect cha, size chart match bhayo.",
    "Color photo ma dekheko jasto natural cha.", "Material premium feel diunchha hat ma.",
    "Original piece confirm bhayo, QR code scan gardaa verified.",
    "Camera quality outstanding, low light ma pani clear.", "Performance smooth cha, gaming pani lag bhayena.",
    "Comfortable for daily use, lightweight pani.", "Stitching ramro cha, kahibata pani thread niskeko chaina.",
    "Smell pani fresh aauchha kholda, kunai duplicate ko jasto chaina.", "Durable ho jasto laagyo, build quality solid cha.",
    "Skin lai suit gareko cha, kunai allergic reaction bhayena.", "Setup easy thiyo, manual pani Nepali ma diyeko cha.",
    "Recipe perfect aayo, motor pani noisy chaina.", "Page quality A1, paper pani thick ra premium.",
    "Charging fast cha, 1 ghanta bhitra full hunchha.", "Display sharp ra colorful cha, video herna maja.",
    "Build quality solid lagyo, heavy duty use ma pani thik chha.",
    "Touch response smooth cha, lag ko issue chaina.", "Compact size cha, bag ma sajilai aatauchha.",
    "Wireless connectivity strong cha, range pani decent.",
    "Audio clarity outstanding cha, calls clear sunincha.", "Cooling system efficient cha, heating issue chaina.",
    "Material breathable cha, garmi ma comfortable cha.",
    "Ergonomic design cha, lamo samaya use garda thakai chaina.", "Buttons tactile feedback ramro chha.",
    "Speaker output loud ra clear cha, party ma maja aaucha.",
    "Battery life impressive, 8-10 ghanta easily chal cha.", "Fast charging working perfectly, 30 min ma 60% bharcha.",
    "Color accuracy ramro cha, photo edit ko lagi best cha.", "Storage capacity ample cha, kahile pani full hudaina.",
    "Fingerprint sensor fast cha, unlock instant huncha.", "Screen-to-body ratio impressive, immersive viewing experience.",
    "Texture fabric ko soft chha, skin lai gentle.",
    "Build paint scratch resistant lagyo, daily use ma chal cha.", "Detachable parts haru cleaning ko lagi handy cha.",
    "Power efficiency ramro, electricity bill ma pani fark pareko cha.", "Noise cancellation dami cha, public ma pani peaceful experience.",
]

POS_DELIVERY = [
    "Fast delivery ra original product, dubai bhayo.", "Order gareko 2 din mai delivery bhayo, super fast.",
    "Packaging neat ra secure thiyo.", "Courier guy professional thiyo, time-on-time pugayo.",
    "Tracking accurate thiyo, real-time update aaiyo.",
    "Delivery before estimated date bhayo, salute to logistics team.", "Door step delivery ramro thiyo, no hassle.",
    "Outer box damage thiyena, sealed packaging.", "Cash on delivery option pani smooth thiyo.",
    "Bubble wrap ra protective foam le secure pareko thiyo.", "Same day delivery! Kathmandu valley ma dherai ramro service.",
    "Delivery boy le call gareko, location confirm gareko, professional.", "Free shipping milyo, paisa pani bachyo.",
]

POS_SERVICE = [
    "Seller le freebie pani diye, surprise gift aayo.", "Seller le ramro service diyo, query ko reply pani fast.",
    "Customer support 24/7 active, instant response.", "Return policy clear thiyo, no confusion.",
    "Warranty card ra invoice dubai milyo.", "Seller le personally call gareko quality check ko lagi.",
    "After sales service top class, problem solve garyo immediately.", "Refund/exchange policy customer-friendly cha.",
]

POS_CLOSERS = [
    "Sabai lai recommend gareko chu yo seller bata kinna.", "Will buy again from this shop. 5 stars!",
    "Dhanyabad seller, keep up the good work!", "Aru saamaan pani yahabata kinchhu ab ta.",
    "Highly recommended, 100% genuine.", "Family friends sabai lai dekhayera tarikhi diyeko ho.",
    "Definitely value for money, no regrets at all.", "Mast experience, order garna napos hesitate.",
    "Repeat customer banne bhayechhu ma yo store ko.", "Thanks Daraz/seller, fast and reliable!",
    "Khusi chu purchase garera, no complaints.", "Yesto seller haru bata business badhos hai!",
    "All good, full marks from my side.", "Awesome product, awesome service. Maja aayo.",
    "Truly worth it, sasto ra ramro ko combo.", "Worth recommending, 5/5 from my side.",
    "Pakkai kinnu hola sabai le, regret hudaina.", "Trustable seller, future ma pani order garchhu.",
    "Mero pailo experience successful bhayo, dherai ramro lagyo.", "Aru products pani try garchhu yo seller ko.",
]

# ---- NEGATIVE -------------------------------------------------------------
NEG_OPENERS = [
    "Ekdam disappointment bhayo yo product le.", "Photo ma dekheko jasto bilkul chaina.",
    "Paisa khera gayo, ramro lagena.", "Don't buy this product, regret hunchha.",
    "Faltu samaan paunu paryo, returning it!", "Maile {product} order gareko, but quality kharab cha.",
    "Worst experience kinda, kahile pani aru lai recommend gardina.", "Fake product ho yo confirm, original hoina!",
    "Bekar seller, customer service zero cha.", "Yesto cheap quality ko samaan kati pataudaina hola.",
    "Refund maag rakheko chu, seller le response pani didaina.", "Defective product aayo packing bata.",
    "Dhokha bhayo, asha gareko jasto kei pani chaina.", "Wrong item delivered, complaint gareko 3 din bhayo.",
    "Damaged condition ma aayo product, courier le tehi bhanyo.", "Useless product, totally waste of money.",
    "Haram lagyo paisa kharcha gareko.", "Description ma lekheko ra actual product different cha.",
    "Seller le kura pani sundaina, very rude reply.", "Order ko status update pani didaina, kati waste service.",
    "1 hapta ma damage bhayo, kasari yo quality bechinchha?", "Bahira bata herda thik dekhincha but use garda kharab.",
    "Faltu ko seller, support kura nai gardaina.", "Mero paisa ko value yo product le diyena.",
    "Duplicate product ho 100%, original hoina at all.", "Bahut nirash banayo yo purchase le.",
    "Cheating ho yo bhanne lagyo malai.", "Yo seller lai block hunu parchha marketplace bata.",
    "Fully unacceptable quality, immediately return gareko chu.",
    "Mismatch bhayo description ra actual product ma.", "Battery dead aayo, charge nai hudaina.",
    "Yesto naramro quality ko samaan kati le accept garchhan?",
    "Fake review haru padhera kinya, dhokha bhayo.", "Returning ASAP, refund chahincha.",
    "Worst purchase ever, yesto product nakinnu ramro.", "Faltu paisa kharcheko, regret matra cha.",
    "Pheri yo seller bata kahile pani kindina.", "Disappointment bhayo expectation jhukyo.",
    "Saamaan haina, junk maatra ho yo.", "Photo ma jasto chha actual ma tyo bhanda kharab.",
]

NEG_PRODUCT = [
    "Quality ekdam poor, 1 hapta ma bigriyo.", "Battery backup faltu, 2 ghanta pani chaldaina.",
    "Color photo bhanda completely fark cha.", "Size ekdam sano cha, return garda extra charge laagyo.",
    "Sound quality dherai noisy, distortion aauchha.", "Material cheap plastic feel, premium description thiyo.",
    "Fake/duplicate product, brand ko logo pani galat print cha.", "Stitching khulisake ko cha already, 2 din ma!",
    "Charger include thiyena, alag kinnu paryo.", "Display ma scratch thiyo bata kholda.",
    "Smell ekdam strong chemical jasto, headache hune.", "Skin ma rashes aayo lagaune bittikai.",
    "Manual english/chinese matra cha, kei bujhena.", "Motor noise dherai cha, neighbors complaint gariraheka chan.",
    "Page haru already torn thiye, used jasto laagyo.", "Charging slow cha, 5 ghanta laagcha full hun.",
    "Software laggy, bistarai chal cha.", "Glue smell, kapada ma dirty mark pani thiyo.",
    "Battery swelling started after 2 weeks, dangerous lagyo.",
    "Camera blur cha, low light ma kei dekhinna.", "Touch unresponsive cha, multi-touch fail.",
    "Heating issue serious cha, 10 min use garda nai garam.",
    "Build quality flimsy, fall pareko ma crack ayo.", "Performance lag huncha, basic apps ma pani slow.",
    "Color faded jasto laagcha first wash pachi, durable haina.", "Connectivity weak, bluetooth pair garna pani garho.",
    "Power button stuck huncha kahile kahin.",
    "Microphone noise cancellation faltu cha, calls ma echo aauchha.", "Speaker volume low cha, max ma pani sunincha haina.",
    "Display ghost touch issue cha, random taps lag huncha.",
    "Accessories include thiyena description ma lekheko jasto.", "Genuine warranty card chaina, fake ho jasto laagcha.",
    "Functionality limited cha, advertised features kaam gardainan.", "Defective unit aayo, exchange request gareko chu.",
    "Plastic build cheap feel, hand ma rakhda dukhdo lagcha.",
    "Print/text quality blurry cha pages ma.", "Power adapter incompatible cha Nepali socket sanga.",
    "Calibration off cha, accurate readings dindainan.", "Memory full hudaina ramrosanga, lag huncha frequent.",
]

NEG_DELIVERY = [
    "Damaged condition ma aayo, courier le toilo handle gareko cha.",
    "Delivery 2 hapta delay bhayo, ridiculous!", "Wrong address ma pugaeko thiyo, paunai paunai gahro.",
    "Packaging damaged, bahirai bata torn thiyo.", "Tracking update kahile pani didaina.",
    "Box dhibilesh thiyo, item andar damage thiyo.", "Pathao guy le rude bahaviour gareko, complaint gareko chu.",
    "Outer box opened thiyo arrival ma, tampered jasto laagyo.",
    "Wrong item bhetiyo, completely different product order gareko thiye.",
    "COD reject gareko, paisa ready thiyo tara delivery boy ramrari samjhena.",
    "Delivery date kayipalta change bhayo, frustrating.",
]

NEG_SERVICE = [
    "Seller le response didaina, complaint sun-eko jasto chaina.", "Customer support utterly useless cha.",
    "Refund process kahile complete hudaina.", "Return pickup arrange garna 5 din lagyo.",
    "Warranty claim ma kura suniyena, bekar policies.", "Support number unreachable cha, mail ko reply pani slow.",
    "Seller arrogant cha, customer ko kuro tinai sundaina.", "After-sales nai zero, ekchoti payment gariyo bhane sambhauchhain.",
]

NEG_CLOSERS = [
    "Don't waste your money, look for other sellers.", "Worst experience, refund maag rakheko chu.",
    "Will never order from this seller again.", "Pls beware, photo dekhera order nagarnu hola.",
    "1 star ni dina mann chaina, forced to give 1.", "Daraz/Sastodeal le yesto seller block garnu paryo.",
    "Paisa firta dieko bhaye thik thiyo.", "Disappointed, expectations naturally jhukhera aayo.",
    "Fully unsatisfied with this purchase.", "Ek star pani over jasto laagcha!",
    "Aru kasaikai sanga kinnu hola yesto haina.", "Customer support pani usai bekar, no help.",
    "Dukha laagyo paisa wasted hunda.", "I want my money back, immediately.",
    "Nevermind, ma aru store ma jaanchu.", "Yesto seller bata bachera ranu, sabai lai warning.",
    "Pheri kahile yo seller bata order gardina.", "Strict action linu paryo seller marathi.",
    "Trust gareko bhayena, regret hudaicha.", "Faltu purchase, paisa wasted bhayo.",
]

# ---- NEUTRAL --------------------------------------------------------------
NEU_OPENERS = [
    "Average product ho, kei khasai impress garne kura chaina.", "Thik chha, but expectation bhanda ali tala.",
    "Decent for the price, but premium feel chaina.", "Mixed feelings cha yo product paera.",
    "Some pros, some cons cha.", "Daily use ko lagi okay cha jastai laagcha.",
    "Maile yo {product} kineko, pheri kinnu paryo bhane sochnu parla.",
    "Yo price range ma yestai paine ho jasto laagcha.", "It is what it is, paisa anusar ko quality.",
    "Two minds chu yo lai recommend garu ki nagaru bhanera.", "Honest review bhannu paryo bhane, normal cha.",
    "Bhako thik thik cha, baki time le bhanchha.", "Use garera herchu thik bhae rakhchu, naramro bhae return.",
    "Just received, abasamma testing ma cha.",
    "Average banaune samaan ho, hotai kasto kasto kura chaina.",
    "Saadharan product ho, kei special kura chaina.",
    "Compromise garnu paryo kayi kura ma, thik thik laagyo.",
    "Hot or cold haina, lukewarm experience.", "Some cool features, but few drawbacks pani.",
    "Worth ko ho bhanne kura debatable cha.",
    "Initial impression decent thiyo, time le batauchha.", "Acceptable cha but excited huna sakdina.",
    "Functional cha tara wow factor missing.",
    "Beneficial pani cha, problem pani cha.", "Need to use more before final verdict, abasamma okay.",
]

NEU_PRODUCT = [
    "Quality average, durability le bhandai chaina.", "Color slightly different cha photo bhanda but acceptable.",
    "Battery 4-5 ghanta chal cha, normal range ma cha.", "Sound quality okay cha but bass weak.",
    "Fitting ali loose cha, size chart match bhayena thik sanga.", "Material plastic feel garchha but functional.",
    "Performance ramro cha but heating issue cha.",
    "Camera daylight ma thik cha, low light ma weak.", "Stitching average, dherai use sahala ki napos thaha bhayena.",
    "Manual unclear thiyo, YouTube hereh feature seek paryo.", "Price ali mahango lagyo yesto quality lai.",
    "Color faded jasto laagcha first wash pachi.", "Setup confusing thiyo but kosis garda chal yo.",
    "Build moderate cha, basic use ko lagi thik.", "Display okay cha, outdoor visibility weak.",
    "Storage limited but expandable cha.", "Functionality basic cha, advanced features missing.",
    "Charging speed average, fast charge advertised bhaeko jasto chaina.",
    "Audio quality decent, soundstage limited cha.", "Comfort moderate cha, lamo time use garda thakauchha.",
    "Connectivity stable cha but range slightly limited.", "Memory adequate cha but heavy apps ma slow.",
    "Buttons feedback weak feel cha but functional.", "Touchscreen responsive but sensitivity adjust garna chahincha.",
    "Vibration motor weak feel cha.", "Camera autofocus slow cha kahile kahin.",
    "Bluetooth pairing complicated thiyo first time.",
]

NEU_DELIVERY = [
    "Delivery time delay bhayo 2 din, baki thik.", "Packing simple thiyo, premium packing chaina.",
    "Courier le rough handle gareko hola jasto, but item safe ayo.",
    "Tracking inconsistent thiyo but final delivery time correct.",
    "On-time pugayo, no surprises good or bad.", "Standard COD experience, kei special chaina.",
]

NEU_SERVICE = [
    "Seller response slow but reply ayo eventually.", "Average customer service, queries answered eventually.",
    "Return policy clear chaina but acceptable cha.", "Standard packaging, no issues, no extras.",
    "Warranty card ayo but verification needed jasto.",
]

NEU_CLOSERS = [
    "Will see how it lasts, time bhane pachi review update gauchu.", "Not bad, not amazing. Mid-range.",
    "Could be better but okay for now.", "Maybe ramro option chha yes paisa anusar.",
    "Recommend or not, hard to say.", "Ali ali doubt cha yo product ko quality ma.",
    "If you have lower budget, yo chalcha.", "Average rating dieko chu honest review ko nimti.",
    "Kasailai chal cha, kasailai chaldaina hola.", "Try at your own risk, sabai lai suit nahuna sakcha.",
    "Update lekhchu pheri 1 mahina pachi.", "Decent cha, paisa anusar.",
    "Nothing extraordinary, just an average product.", "Use garera bhanaula time pachi.",
    "Rakhne bhanera kinya, return garne mann pani chaina.", "Mid-tier choice ho yo, premium chaina.",
    "Saadharan product, saadharan rating.", "Okay-ish, not exciting, not terrible.",
    "Wait and watch ko strategy linu paryo.", "Final verdict aru kura test garera matra dinu paryo.",
]

# ===========================================================================
# 3. SLOT-BASED PHRASE GENERATORS — explode combinatorially
# ===========================================================================
ASPECTS = [
    "quality", "build", "design", "performance", "look", "finish",
    "sound", "display", "screen", "color", "material", "fitting",
    "stitching", "fabric", "battery", "charging speed", "camera",
    "weight", "size", "comfort", "feel", "packaging", "delivery time",
    "value for money", "price", "durability", "feature set",
    "user experience", "interface", "software",
]
POS_QUALITIES = [
    "ramro", "premium", "smooth", "solid", "amazing", "outstanding",
    "top class", "babal", "mast", "perfect", "ekdam ramro",
    "high quality", "excellent", "dami", "sundar", "satisfying",
]
NEG_QUALITIES = [
    "kharab", "naramro", "cheap", "poor", "faltu", "terrible",
    "broken", "defective", "worst", "ekdam naramro", "low quality",
    "useless", "weak", "bekar", "duplicate jasto", "thirupiti",
]
NEU_QUALITIES = [
    "average", "okay", "thik thik", "saadharan", "moderate", "decent",
    "passable", "neither good nor bad", "acceptable", "lukewarm",
]
INTENSIFIERS = [
    "ekdam", "dherai", "thoderai", "bilkul", "asaadhya", "ekdum",
    "really", "very", "super", "quite", "rather", "fairly", "absolutely",
]
HEDGES = [
    "ali", "thodai", "kati kati", "slightly", "somewhat", "kinda",
    "a bit", "more or less",
]
SHORT_POS = [
    "Mast cha!", "Ramro cha.", "Top notch.", "Loved it!", "Babal product.",
    "Highly recommend!", "Worth it.", "Excellent purchase.", "Bhalo lagyo.",
    "Salute seller.", "Original cha 100%.", "Perfect!", "Genuine product.",
    "Khushi chu.", "Solid item.",
]
SHORT_NEG = [
    "Bekar product.", "Worst!", "Don't buy.", "Faltu cha.", "Naramro ekdam.",
    "Refund maag rakheko.", "Fake product.", "Disappointed.", "Total waste.",
    "Bhayena ramro.", "Cheating.", "Useless item.", "Damaged aayo.",
    "Returning it.", "Avoid this.",
]
SHORT_NEU = [
    "Average cha.", "Thik thik.", "Mid product.", "Decent for price.",
    "Okay cha.", "Mixed bag.", "Saadharan.", "Not great, not bad.",
    "Will see.", "Acceptable.", "Functional cha.",
]


def slot_phrase_pos() -> str:
    return random.choice([
        f"{random.choice(ASPECTS).capitalize()} {random.choice(INTENSIFIERS)} {random.choice(POS_QUALITIES)} cha.",
        f"{random.choice(ASPECTS).capitalize()} {random.choice(POS_QUALITIES)} cha, {random.choice(INTENSIFIERS)} satisfied chu.",
        f"Yo product ko {random.choice(ASPECTS)} {random.choice(POS_QUALITIES)} feel diunchha.",
        f"{random.choice(INTENSIFIERS).capitalize()} {random.choice(POS_QUALITIES)} {random.choice(ASPECTS)}, recommend garchhu.",
        f"{random.choice(ASPECTS).capitalize()} bhanchu bhane, {random.choice(POS_QUALITIES)} ko ramro experience.",
    ])


def slot_phrase_neg() -> str:
    return random.choice([
        f"{random.choice(ASPECTS).capitalize()} {random.choice(INTENSIFIERS)} {random.choice(NEG_QUALITIES)} cha.",
        f"{random.choice(ASPECTS).capitalize()} {random.choice(NEG_QUALITIES)} cha, paisa khera gayo.",
        f"Yo product ko {random.choice(ASPECTS)} {random.choice(NEG_QUALITIES)} ho.",
        f"{random.choice(INTENSIFIERS).capitalize()} {random.choice(NEG_QUALITIES)} {random.choice(ASPECTS)}, regret cha.",
        f"{random.choice(ASPECTS).capitalize()} ekdam {random.choice(NEG_QUALITIES)}, returning it.",
    ])


def slot_phrase_neu() -> str:
    return random.choice([
        f"{random.choice(ASPECTS).capitalize()} {random.choice(HEDGES)} {random.choice(NEU_QUALITIES)} cha.",
        f"{random.choice(ASPECTS).capitalize()} {random.choice(NEU_QUALITIES)} cha, kei special chaina.",
        f"Yo product ko {random.choice(ASPECTS)} {random.choice(NEU_QUALITIES)} feel diunchha.",
        f"{random.choice(HEDGES).capitalize()} {random.choice(NEU_QUALITIES)} {random.choice(ASPECTS)}, saadharan.",
        f"{random.choice(ASPECTS).capitalize()} {random.choice(NEU_QUALITIES)}, will see how it goes.",
    ])


# ===========================================================================
# 4. EMOJIS, TYPOS, CODE-MIXING ANALYSIS — same logic as v1
# ===========================================================================
EMOJIS_POS = ["👍","❤️","🔥","⭐","😊","💯","🥰","✨","🎉","💖"]
EMOJIS_NEG = ["👎","😠","💔","😡","⚠️","💢","😤","🤬"]
EMOJIS_NEU = ["🤔","😐","🙂","🤷","😶"]

TYPO_MAP = [
    ("ekdam","ekdum"),("cha","chha"),("garera","garra"),("ramro","raamro"),
    ("paisa","paissa"),("ho","ho!"),("garekko","gareko"),("dherai","dherrai"),
    ("naramro","naraamro"),("thik","thikai"),("babal","babbal"),
]

def maybe_apply_typos(text: str) -> str:
    if random.random() > 0.30:
        return text
    a, b = random.choice(TYPO_MAP)
    return text.replace(a, b, 1)

def maybe_add_emoji(text: str, sentiment: str) -> str:
    if random.random() > 0.20:
        return text
    pool = {"positive":EMOJIS_POS,"negative":EMOJIS_NEG,"neutral":EMOJIS_NEU}[sentiment]
    return f"{text} {random.choice(pool)}"

ENGLISH_HINT_WORDS = {
    "the","is","and","for","very","good","bad","best","worst","product",
    "delivery","fast","slow","buy","highly","quality","service","thanks",
    "amazing","useless","cheap","value","money","battery","camera","sound",
    "package","size","color","fitting","performance","material","average",
    "okay","decent","premium","original","fake","refund","return",
    "recommended","review","with","all","have","this","that","but","from",
    "will","not","you","are","was","i","to","of","in","on","it","as","be",
    "an","or","so","if","after","before","again","also","more","less","than",
    "satisfied","disappointed","expected","expectation","received","damaged",
    "defective","genuine","duplicate","stars","star","really","super","great",
    "perfect","totally","completely","neither","either","display","screen",
    "build","design","look","feel","weight","comfort","durability","interface",
    "software","absolutely","truly","quite","rather","fairly",
}
NEPALI_HINT_WORDS = {
    "cha","chha","ho","ramro","kharab","ekdam","garyo","bhayo","dherai",
    "paisa","samaan","saamaan","khusi","ekdum","naramro","thiyo","thiye",
    "bhanchu","bhanera","garera","garna","ko","ma","lai","le","ra","tara",
    "sanga","haina","ho!","sasto","mahango","tikai","tikkai","thik","thik-thik",
    "huncha","hunna","din","raat","purano","naya","sano","thulo","kati",
    "kasari","kahile","namaskar","dhanyabad","babal","ramri","sangai",
    "yesto","yo","tyo","jasto","baki","abasamma","ali","thodai","babbal",
    "raamro","ramrosanga","bhalo","khusi","dukha","mann","yaar","bro",
    "saadharan","mast","dami","faltu","bekar","sundar",
}

def estimate_code_mixing(text: str) -> dict:
    tokens = re.findall(r"[A-Za-z]+", text.lower())
    if not tokens:
        return {"en_ratio":0.0,"ne_ratio":0.0,"dominance":"unknown"}
    en = sum(1 for t in tokens if t in ENGLISH_HINT_WORDS)
    ne = sum(1 for t in tokens if t in NEPALI_HINT_WORDS)
    total = len(tokens)
    en_r = round(en/total, 3); ne_r = round(ne/total, 3)
    if en_r > ne_r * 1.4:    dom = "English-dominant"
    elif ne_r > en_r * 1.4:  dom = "Nepali-dominant"
    else:                    dom = "Balanced"
    return {"en_ratio":en_r,"ne_ratio":ne_r,"dominance":dom}

def has_emoji(text: str) -> bool:
    return any(ord(c) > 0x2600 for c in text)


# ===========================================================================
# 5. REVIEW BUILDER — composes from 5 fragment slots + slot-based phrases
# ===========================================================================
def build_review(sentiment: str, product_tuple, category: str, idx: int) -> dict:
    product_name, base_price, brand = product_tuple

    # Pool selection
    if sentiment == "positive":
        opener_pool, prod_pool, deliv_pool, serv_pool, closer_pool = \
            POS_OPENERS, POS_PRODUCT, POS_DELIVERY, POS_SERVICE, POS_CLOSERS
        short_pool, slot_fn = SHORT_POS, slot_phrase_pos
        rating = random.choices([4,5,5,5,5,5], k=1)[0]
    elif sentiment == "negative":
        opener_pool, prod_pool, deliv_pool, serv_pool, closer_pool = \
            NEG_OPENERS, NEG_PRODUCT, NEG_DELIVERY, NEG_SERVICE, NEG_CLOSERS
        short_pool, slot_fn = SHORT_NEG, slot_phrase_neg
        rating = random.choices([1,1,1,1,2,2], k=1)[0]
    else:
        opener_pool, prod_pool, deliv_pool, serv_pool, closer_pool = \
            NEU_OPENERS, NEU_PRODUCT, NEU_DELIVERY, NEU_SERVICE, NEU_CLOSERS
        short_pool, slot_fn = SHORT_NEU, slot_phrase_neu
        rating = random.choices([2,3,3,3,3,4], k=1)[0]

    # ~10% of reviews are very short (single phrase) — mirrors real users
    r = random.random()
    if r < 0.10:
        text = random.choice(short_pool)
    else:
        # Compose 1–5 fragments. Always include opener.
        # 30% chance of a slot-based phrase mixed in (more diversity)
        parts = [random.choice(opener_pool)]
        if random.random() < 0.78:
            parts.append(random.choice(prod_pool) if random.random() < 0.55 else slot_fn())
        if random.random() < 0.42:
            parts.append(random.choice(deliv_pool))
        if random.random() < 0.35:
            parts.append(random.choice(serv_pool))
        if random.random() < 0.55:
            parts.append(random.choice(closer_pool))
        text = " ".join(parts)

    # Mixed-aspect reviews (~8% of non-neutral reviews): inject opposing phrase
    # e.g. positive product + negative delivery gripe
    if sentiment == "positive" and random.random() < 0.08:
        text += " " + random.choice(NEG_DELIVERY) if random.random() < 0.5 else \
                " " + slot_phrase_neg()
    elif sentiment == "negative" and random.random() < 0.06:
        text += " " + random.choice(POS_DELIVERY)

    text = text.format(product=product_name, seller="seller")
    text = maybe_apply_typos(text)
    text = maybe_add_emoji(text, sentiment)

    cm = estimate_code_mixing(text)

    # Slightly wider date range than v1 to fit larger sample (Jan 2024 → Apr 2026)
    review_date = datetime(2024, 1, 1) + timedelta(
        days=random.randint(0, 850),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )

    location = random.choices(LOCATIONS, weights=LOCATION_WEIGHTS, k=1)[0]
    payment  = random.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS, k=1)[0]
    helpful  = random.randint(0, 15) if sentiment == "neutral" else random.randint(0, 80)
    verified = random.random() < (0.88 if sentiment != "negative" else 0.82)

    return {
        "review_id":            f"R{idx:06d}",
        "product_id":           f"P{abs(hash(product_name)) % 100000:05d}",
        "product_name":         product_name,
        "product_category":     category,
        "brand":                brand,
        "product_price_npr":    base_price,
        "seller_name":          random.choice(SELLERS),
        "delivery_partner":     random.choice(DELIVERY_PARTNERS),
        "reviewer_location":    location,
        "payment_method":       payment,
        "review_date":          review_date.strftime("%Y-%m-%d %H:%M"),
        "review_text":          text,
        "rating":               rating,
        "sentiment_label":      sentiment,
        "verified_purchase":    verified,
        "helpful_count":        helpful,
        "review_length_chars":  len(text),
        "review_length_tokens": len(re.findall(r"\S+", text)),
        "english_token_ratio":  cm["en_ratio"],
        "nepali_token_ratio":   cm["ne_ratio"],
        "language_dominance":   cm["dominance"],
        "has_emoji":            has_emoji(text),
    }


# ===========================================================================
# 6. BUILD DATASET
# ===========================================================================
TOTAL = 100_000
# Same proportions as v1 (~58/30/12 — slightly rebalanced toward positives
# to stay faithful to Pradhananga & Sah's natural skew)
SPLIT = {"positive": 58_000, "negative": 30_000, "neutral": 12_000}
assert sum(SPLIT.values()) == TOTAL

flat_products = [(name, price, brand, cat)
                 for cat, items in CATEGORIES.items()
                 for (name, price, brand) in items]
print(f"Product catalogue: {len(flat_products)} SKUs across {len(CATEGORIES)} categories")

print(f"Generating {TOTAL:,} reviews ...")
records = []
idx = 1
for sentiment, count in SPLIT.items():
    for _ in range(count):
        name, price, brand, cat = random.choice(flat_products)
        records.append(build_review(sentiment, (name, price, brand), cat, idx))
        idx += 1
        if idx % 20000 == 0:
            print(f"  ... {idx-1:,} reviews done")

random.shuffle(records)
for i, rec in enumerate(records, start=1):
    rec["review_id"] = f"R{i:06d}"

# Diversity sanity check
unique_texts = len({r["review_text"] for r in records})
print(f"Unique review texts: {unique_texts:,} / {TOTAL:,} "
      f"({100*unique_texts/TOTAL:.1f}% unique)")

# ===========================================================================
# 7. WRITE PRIMARY CSV
# ===========================================================================
csv_path = OUT / "kathmandu_marketplace_reviews_100k.csv"
fieldnames = list(records[0].keys())
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(records)
print(f"Wrote {csv_path}")

# ===========================================================================
# 8. STRATIFIED 70/15/15 SPLITS
# ===========================================================================
by_sent: dict[str, list] = {"positive":[], "negative":[], "neutral":[]}
for r in records:
    by_sent[r["sentiment_label"]].append(r)

train, val, test = [], [], []
for sent, rows in by_sent.items():
    random.shuffle(rows)
    n = len(rows)
    n_train = int(n * 0.70)
    n_val   = int(n * 0.15)
    train.extend(rows[:n_train])
    val.extend(rows[n_train:n_train+n_val])
    test.extend(rows[n_train+n_val:])
random.shuffle(train); random.shuffle(val); random.shuffle(test)

for split_name, split_data in [("train",train),("val",val),("test",test)]:
    p = OUT / f"split_{split_name}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(split_data)
    print(f"  {split_name}: {len(split_data):,} rows -> {p.name}")

# ===========================================================================
# 9. METADATA
# ===========================================================================
metadata = {
    "dataset_name": "Kathmandu Marketplace Code-Mixed Reviews v2",
    "version": "2.0.0",
    "created": datetime.now().strftime("%Y-%m-%d"),
    "total_reviews": TOTAL,
    "class_distribution": SPLIT,
    "schema_columns": fieldnames,
    "products_total": len(flat_products),
    "categories": list(CATEGORIES.keys()),
    "sellers": len(SELLERS),
    "locations": LOCATIONS,
    "payment_methods": PAYMENT_METHODS,
    "delivery_partners": DELIVERY_PARTNERS,
    "splits": {"train": len(train), "val": len(val), "test": len(test)},
    "reproducibility": "random.seed(42)",
    "diversity_metrics": {
        "unique_review_texts": unique_texts,
        "uniqueness_pct": round(100*unique_texts/TOTAL, 2),
    },
    "modeled_after": [
        "Pradhananga & Sah (2023) Transformer-Based Sentiment Analysis on Romanized Nepali Daraz reviews",
        "Chaudhary et al. (2025) NEPTUN normalization for Romanized Nepali",
    ],
    "notes": "Synthetic dataset; not from any real marketplace. Generic 'Kathmandu marketplace' framing.",
}
(OUT / "dataset_metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
print("Wrote dataset_metadata.json")
print("\nDone.")
