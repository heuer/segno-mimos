Changes
=======

0.2.1 -- 2017-02-08
-------------------
* Fixed typos and internal changes to support Py 3 more prominent


0.2.0 -- 2017-02-08
-------------------
* Support for PyQRCode's qrcode.xbm() method which returns the QR Code as
  XBM image (requires Segno >= 0.2.4).
* Support for python-qrcode data optimization.
* Better test coverage
* Tests against Python 3.6 (tested against PyPy, Py 2.6, 2.7, 3.4, 3.6)


0.1.9 -- 2016-09-19
-------------------
* Added ``install_as_qrcode`` and ``install_as_pyqrcode`` which may be useful
  if qrcode or PyQRCode is used and should be replaced by Segno without code
  changes.
* Fixed Python packaging.


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
