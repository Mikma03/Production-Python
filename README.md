
<!-- TOC -->

- [Introduction - useful links](#introduction---useful-links)
  - [Python ... sheets](#python--sheets)
    - [SpeedSheet](#speedsheet)
    - [Cheatsheet](#cheatsheet)
  - [Index of Python Enhancement Proposals (PEPs)](#index-of-python-enhancement-proposals-peps)
- [The best books on the Python market](#the-best-books-on-the-python-market)
- [Places for practise. General purpose & interview](#places-for-practise-general-purpose--interview)
- [Active communities - Python](#active-communities---python)
  - [Mailing lists](#mailing-lists)
  - [Others communities](#others-communities)
- [Modern Python Development Environments](#modern-python-development-environments)
- [New Things in Python](#new-things-in-python)

<!-- /TOC -->

# Introduction - useful links
___
## Python ... sheets

### SpeedSheet

Interactive Python cheat sheet. Covers the core Python programming language

> https://speedsheet.io/s/python#gcez

### Cheatsheet

Based on the book Automate the Boring Stuff with Python and many other sources.

> https://www.pythoncheatsheet.org/


## Index of Python Enhancement Proposals (PEPs)

This PEP contains the index of all Python Enhancement Proposals.

> https://peps.python.org/

# The best books on the Python market
___

# Places for practise. General purpose & interview
___

# Active communities - Python
___

## Mailing lists

Besides lists with very specific themes, there are few general mailing lists that should be very interesting for every Python programmer. These are:

- **python-ideas@python.org:** 

This is a staple when it comes to Python mailing lists. It is a place for discussing a wide variety of ideas regarding Python. Most PEPs start as a speculative idea discussion on this mailing list. It is a great place for discussing potential "what ifs" and finding out what features people would like to see in the near future.

- **python-dev@python.org:** 

This is a mailing list specifically for the purpose of core Python development (mainly CPython interpreter). It is also a place where first drafts of new PEPs are discussed before being officially announced through other channels. It isn't a place where you should be asking for general Python help, but it is an essential resource if you would like to try your hand at fixing known bugs in the CPython interpreter or the Python standard library.

- **python-announce-list@python.org:** 

This is a mailing list for various announcements. You can find announcements of conferences and meetups here, as well as notifications about new releases of your favorite packages and frameworks or new PEPs. It is also great for discovering new and exciting projects.

## Others communities

- PySlackers Slack workspace (**https://pyslackers.com**): A large community of Python enthusiasts using the Slack messaging platform to discuss anything Python-related

- Python Discord server (**https://pythondiscord.com**): Another open Python community but using Discord as their messaging platform

- /r/python subreddit (**https://www.reddit.com/r/Python/**): A single subreddit on the Reddit platform dedicated to Python

- Python Weekly **(http://www.pythonweekly.com/)** is a popular newsletter that delivers to its subscribers dozens of new, interesting Python packages and resources every week

- PyCoder's Weekly **(https://pycoders.com)** is another popular weekly newsletter with a digest of new packages and interesting articles

# Modern Python Development Environments
___

The pip installation can be bootstrapped using the ensurepip module as in the following example:

    python -m ensure pip

When you have pip available, installing a new package is as simple as this:

    pip install <package-name>

Among other features, pip allows specific versions of packages to be installed (using `pip install <package-name>==<version>`) or upgraded to the latest version available (using `pip install -–upgrade <package-name>`).

When you use` pip` to install a new package from PyPI, it will be installed into one of the available site-packages directories. The exact location of site-packages directories is specific to the operating system. You can inspect paths where Python will be searching for modules and packages by using the `site` module as a command as follows:

    python -m site


An alternative way to obtain the site-packages is by invoking `sys.getsitepackages()`. The following is an example of using that function in an interactive shell:

    >>> import site
    >>> site.getsitepackages()
    ['C:\\Users\\mikol\\AppData\\Local\\Programs\\Python\\Python310', 'C:\\Users\\mikol\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages']
    >>>

The important thing to note about `venv` is that it does not provide any additional abilities to track what packages should be installed in it. Virtual environments are also not portable and should not be moved to another system/machine or even a different filesystem path. This means that a new virtual environment needs to be created every time you want to install your application on a new host.

Because of this, there is a best practice that's used by `pip` users to store the definition of all project dependencies in a single place. The easiest way to do this is by creating a `requirements.txt` file (this is the naming convention).

With such a file, all dependencies can be easily installed in a single step. The `pip install` command understands the format of such requirements files. You can specify the path to a requirements file using the `-r` flag as in the following example:

    pip install -r requirements.txt

There is the `pip freeze` command, which prints all packages in the current environment together with their versions, but it should be used carefully. This list will also include dependencies of your dependencies, so for large projects, it will quickly become very large. You will have to carefully inspect whether the list contains anything installed accidentally or by mistake.

**There are two leading tools for providing system-level isolation of development environments:**

- Docker for operating system-level virtualization
- Vagrant for machine virtualization

Install:

      You can find Docker installation instructions on https://www.docker.com/get-started


Docker supports plenty of instructions, but the most basic ones that you need to know in order to get started are as follows:

https://learning.oreilly.com/library/view/expert-python-programming/9781801071109/Text/Chapter_2.xhtml#:-:text=Docker%20supports%20plenty%20of,started%20are%20as%20follows%3A


      The official Docker documentation can be found at https://docs.docker.com/

The following table gives a short list of such useful utilities that I find invaluable when working with any code. Think of it as a mini awesome list of programming productivity tools:

https://learning.oreilly.com/library/view/expert-python-programming/9781801071109/Text/Chapter_2.xhtml#:-:text=The%20following%20table,programming%20productivity%20tools%3A


# New Things in Python

