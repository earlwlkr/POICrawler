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
{
    _id: "5543805e7504971d78fe006e",
    price_min: 70000,
    _type: "diner",
    close_time: "1900-01-01T22:30:00.000Z",
    open_time: "1900-01-01T08:00:00.000Z",
    phone: "(08) 38 277 898",
    price_max: 165000,
    cuisine: "Nhật Bản",
    category: 4,
    foody_id: 595,
    address: {
        country: "Vietnam",
        street_address: "30 Lê Lợi, P. Bến Nghé",
        city: "TP. HCM",
        district: "Quận 1"
    },
    name: "MOF Japanese Dessert Cafe - Lê Lợi"
}
```



## Giấy phép

MIT License
