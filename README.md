# Wa Ying College Mathematics Past Paper Collector

## What is it
It collects the URL of all Mathematics past papers available in WYC Moodle web-based classroom and downloads them.

## Prerequisites
- An account that could log in to the web-based classroom of WYC
- Python 3.x installed
- Python packages BeautifulSoup4 and requests installed

### Usage
1. Download and install the latest Python 3 from the [official site of Python](https://www.python.org/downloads/) if you don't have it.
2. Install the required packages by the following commands if you don't have them.

	``pip install beautifulsoup4``

	``pip install requests``
3. Edit ``main.py``. At line 5 and 6, change ``WTFK`` to your login username and ``CHEMISTRY`` to your password.
4. Run ``main.py``. All files downloaded are located in``/downloads`` which is located in the same directory as the ``main.py`` do. 