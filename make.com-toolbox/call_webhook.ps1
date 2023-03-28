$url = "https://hook.eu1.make.com/XXX"
$jsonData = @"
{
  "Address": {
    "original": "adr1",
    "is_valid": false,
    "formatted": "adr2"
  },
  "ExternalOrderId": "12345",
  "OrderDate": "2023-03-27",
  "OrderPos": "3",
  "OrderTable": "00719243518448 BRAND KETO KAKAO CRUNC 10 14 1 00719243518462 BRAND KETO NUSS CRUNCH 10 22 1 09120115891407 KETO GRANOLA HIMBEER-SCHO 10 16 1",
  "end": "Ende der Bestellung",
  "DeliveryDate": "2023-03-28",
  "DeliveryTime": "17.00"
}
"@
Invoke-WebRequest -Uri $url -Method POST -Body $jsonData -ContentType "application/json"