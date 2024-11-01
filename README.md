# OneShotQr
> One Shot QR is a web application that allows you to generate a QR code that is accessible only a specific number of times and dont have direct link


## TechStack
| Technology| Version|
|-----------|--------|
|Python|3.12.6|
|Flask|3.0.3|
|Pytest|8.3.3|


## Description
**OneShotQr** generates special QR codes that, once scanned, redirect the user to **OneShotQr**, and the application then redirects the user to the original URL. This is designed so that the user does not know the URL without first scanning the code. In a way, they are disposable QR codes.