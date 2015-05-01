# POICrawler
Lấy địa điểm yêu thích

## Thư viện

Viết bằng Python 3.

```
pip install requests
```

```
pip install beautifulsoup4
```

```
pip install pymongo
```

## Sử dụng code

```
python run.py
```

Dữ liệu lấy sẵn nằm ở ```example_output.txt```, với 5000 quán ăn được lấy từ [Foody.vn](http://www.foody.vn/ho-chi-minh/dia-diem). Giới hạn 5000 được đặt trong ```run.py```.

Ví dụ một đối tượng ```Diner```:

```
"_type": "diner",
"foody_id": 595,
"name": "MOF Japanese Dessert Cafe - Lê Lợi",
"address": {
    "street_address": "30 Lê Lợi, P. Bến Nghé",
    "district": "Quận 1",
    "city": "TP. HCM",
    "country": "Việt Nam"
},
"phone": "(08) 38 277 898",
"cuisine": "Nhật Bản",
"open_time": "08:00",
"close_time": "22:30",
"price_min": 70000,
"price_max": 165000
```



## Giấy phép

MIT License
