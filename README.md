finsburyFoods
=============

Finsbury Foods Stock Summary Tools

Installation:
==============
There is nothing that needs compiling in this project, however there are the following external dependencies:

External Dependencies:
=====================
I use stdnum for validation of ean numbers. This was not a module that I had used before but seems to be very widely-used and is public license. 
I used dateutil for parsing of dates from the input in order to add the option to ignore transactions outside of a date range. I have commonly used this module in the past
and seems by many to be considered part of the core python stack.

[download dateutil here](https://pypi.python.org/pypi/python-dateutil "dateutil available here")
[download stdnum here](https://pypi.python.org/pypi/python-stdnum/ "stdnum available here")


Unit Tests:
===========
If you have nose installed, you can run the tests simply by typing nosetests in the project directory.

Alternatively, the tests are located in the `test` folder and can be run directly by running `python test/test_parseTransaction.py` etc.

Main Program:
=============

Run the main program as follows:


    ./finsburySummary.py <stockFilename> <transactionFilename>

