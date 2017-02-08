Segno Mimos - Adapt Segno's API to other QR Code libs
=====================================================

Segno Mimos aims to emulate the API of other Python QR Code libs. While this
works more or less API-wise, the resulting QR Codes may look different.

Currently, `PyQRCode`_ and `qrcode`_ are supported.

Segno Mimos does not require any of 3rd party libs (like Pillow or PyPNG), it
just requires `Segno`_ to be installed.

Since both libs do not support Micro QR Codes, this lib creates QR Codes, only.


Replace PyQRCode with Segno
---------------------------

If a 3rd party lib uses PyQRCode and changing the code of the lib isn't
possible, use:

.. code-block:: python

    >>> import segno_mimos
    >>> segno_mimos.install_as_pyqrcode()


To replace PyQRCode with Segno in your code, change

.. code-block:: python

    >>> import pyqrcode

with:

.. code-block:: python

    >>> from segno_mimos import pyqrcode


After that import you should be able to use your existing code without any
changes:

.. code-block:: python

    >>> from segno_mimos import pyqrcode
    >>> # Example from PyQRCode README:
    >>> url = pyqrcode.create('http://uca.edu')
    >>> url.svg('uca-url.svg', scale=8)
    >>> url.eps('uca-url.eps', scale=2)
    >>> print(url.terminal(quiet_zone=1))

Please note, that ``qr = pyqrcode.QrCode('Dark side of the Moon')`` DOES NOT
work, use the factory function ``pyqrcode.create()``.

The underlying ``segno.QRCode`` instance can be accessed as follows:

.. code-block:: python

    >>> from segno_mimos import pyqrcode
    >>> # qr behaves like pyqrcode.QRCode
    >>> qr = pyqrcode.create('Up Jumped the Devil')
    >>> # Get the underlying Segno QRCode instance
    >>> segno_qr = qr.segno_qrcode


Replace qrcode with Segno
-------------------------

If a 3rd-party lib uses qrcode, use the following code snippet before
importing the 3rd-party lib:

.. code-block:: python

    >>> import segno_mimos
    >>> segno_mimos.install_as_qrcode()

The 3rd-party lib should use Segno automatically.


Since qrcode has a more complex API (i.e. factories) replacing it with
Segno can be more difficult; in the simpliest case replace

.. code-block:: python

    >>> import qrcode


in your code with:

.. code-block:: python

    >>> from segno_mimos import qrcode
    >>> # From now on, you can use qrcode as usual
    >>> img = qrcode.make('Some data here')
    >>> img.save('qrcode.png')
    >>> # Segno Mimos provides the "constants" module as well, so this works, too
    >>> qr = qrcode.QRCode(version=1,
    ...     error_correction=qrcode.constants.ERROR_CORRECT_L,
    ...     box_size=10,
    ...     border=4)
    >>> img = qr.make_image()
    >>> # Utilizing the "kind" parameter of qrcode works for PDF, PNG, and EPS files
    >>> img.save('qrcode.png', kind='png')  # Unnecessary, since PNG is the default
    >>> img.save('qrcode.pdf', kind='pdf')
    >>> img.save('qrcode.eps', kind='eps')


If your code uses any of the standard image factories, use the following imports:

.. code-block:: python

    >>> from segno_mimos import qrcode
    >>> import segno_mimos.qrcode.image.svg
    >>> import segno_mimos.qrcode.image.pure
    >>> qr = qrcode.QRCode(version=1,
    ...     error_correction=qrcode.constants.ERROR_CORRECT_L,
    ...     box_size=10,
    ...     border=4)
    >>> # Use the image factory as usual, no code changes necessary
    >>> svg_img = qr.make_image(image_factory=qrcode.image.svg.SvgFragmentImage)
    >>> pure_img = qr.make_image(image_factory=qrcode.image.pure.PymagingImage)

The "pure" image factory is actually the same as the default image factory, it
just exists to minimize code changes. Further, all SVG image factories are
serializing the QR Code as path, never as a combination of rects
(like ``qrcode.image.svg.SvgImage`` does). The SVG factories do not require
any 3rd party libs (aside from segno) like lxml etc.



.. _PyQRCode: https://pypi.python.org/pypi/PyQRCode/
.. _qrcode: https://pypi.python.org/pypi/qrcode/
.. _Segno: https://pypi.python.org/pypi/segno/
