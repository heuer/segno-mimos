Changes
=======

0.1.8 -- 2016-09-04
-------------------
* Disable automatic error incrementation (Segno >= 0.1.7) (neither PyQRCode
  nor qrcode support it)


0.1.7 -- 2016-08-24
-------------------
* Adapt Segno's 0.1.6 API changes


0.1.6 -- 2016-08-17
-------------------
* Internal code changes
* qrcode: Image could not be saved in another output format using the
  "format" or "kind" parameter. Fixed.


0.1.5 -- 2016-08-16
-------------------
* Updated docs
* Removed return statement from ``PyQRCode.png()``
* Internal code changes
* Renamed (internal) module ``segno_mimos.qrcode.img`` into ``_img`` to avoid
  confusion with ``segno_mimos.qrcode.image``


0.1.4 -- 2016-08-14
-------------------
* Initial release
* Support for PyQRCode 1.2.1 and qrcode 5.3
