**The Magi**
=========================================
Sabi. Simple, Lightweight, but Not Beautiful.


Quick Start
-------------------

_NOTICE: This software is currently compatible with Debian distributions of Linux. Future development will add additional OS support._

_NOTICE: This package will install software from your apt sources: nginx and apache2_

**To view your webserver:**
* After running The Magi each time, it will print a list of each ports being
          used (also saved to ./magi/docs/myWebservers.txt).
* In your web browser, go to localhost:portnumber (substituting port number
          for the ports aforementioned) _NOTE: If this is on a remote server, type
          the IP address of that server instead of localhost._

**To add webservers:**
* Make a directory/folder of albums of images and videos you want to include.
* (Optional) Make a config file in magi/config. (See evangelion.conf for example)
  * There are four variables: category, title, banner, auth
    * category: Name of your directory
    * title: Title on browser tab
    * banner: Top headline for the website
    * auth: True/False/Unique
* Put the new directory in ./magi/categories

**To update The Magi:**
* Open your terminal
* Navigate to where you installed The Magi
* Type `sudo python3 magi.py`


Example
-------------

There is an included webserver with The Magi.  You must run magi.py once to get it setup,
but beyond that it is accessible. If you have run magi.py and not added any other webservers,
it will be available in your web browser at localhost:9001.  There you will find an example
from Hideaki Anno's Neon Genesis Evangelion franchise, the namesake for The Magi.  You can
navigate this webserver like any other website.

Inside magi/config/evangelion.conf, you will see how the configuration file is setup for this
evangelion webserver.  Inside magi/categories/ you will see a directory called evangelion.
This is the top level collection, the directory that will become the web server.  Inside
evangelion, there are two directories: web and subcategories. The web directory is all managed
by The Magi for you. The subcategories directory is where you will place your albums. The two
albums included in our example: angels and characters.  Inside each of those albums are
a few pictures from the series.

File Structure
--------------------

Inside The Magi installation folder, there are four items:

* Categories - Where you will add directories for each webserver. Inside each directory you add,
                there should be collections of media in separate directories.
* Config - Where you will give The Magi the tools it needs to get you rolling. Simply create a new
            config file for each webserver, following the example provided.
* Docs - README and list of current webservers

Future Development
-----------------------

* Add additional Linux distribution support
* Add macOS and Windows 10 support
* Change server management to subdomains from host:port format
* Integrate modular CSS support to easily import custom CSS templates
* Improve integration of video formats into Magi generated webpages
* Improve server indexing speeds for faster page loading
