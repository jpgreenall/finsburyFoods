finsburyFoods
=============

Finsbury Foods Stock Summary Tools

Installation:
==============
The code was built and tested on linux. The instructions supplied here are for linux, however it should
be straightforward to get the code working on Windows.
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
If you have nose installed, you can run the tests simply by typing `nosetests` in the project directory.

Alternatively, the tests are located in the `test` folder and can be run directly by running `python test/test_parseTransaction.py` etc.

Main Program:
=============

Run the main program as follows:


    ./finsburySummary.py <stockFilename> <transactionFilename>

You can try with the supplied demo files as follows:
 
    ./finsburySummary.py test/stocklistDemo.xml test/transactionDemo.csv


Discussion:
===========

All the functionality requirements in the brief have been fulfilled.

I created separate functions for parsing the csv and xml data. In both cases, entries with invalid ean are ignored. Optional parameter *warn* for each function toggles display of bad ean numbers to the commandline.
Other numeric / date fields in the files are parsed. If any errors are found in fields other than the ean, an exception is raised with clear description of where the problem is. I considered this to be better default behaviour than silent failure as bad data could indicate problems elsewhere in the pipeline.

In general, I have used list comprehensions and built-ins for any iterative operations where possible for speed. I created a class with which to hold the data that uses __slots__ in order to ensure memory usage and speed is as good as it can be when large xmls are supplied. I have left several fields in that class which are populated but currently not used as they could be useful if extra functionality is required. If memory is an issue, these fields could be pruned. I store *profit* and *margin* to simplify sorting later on. Again, if memory is an issue, either these values could be generated on the fly or the fields used to generate them could be pruned.

If you were to run the file on very large XML file (in order of GBs), there may be memory issues caused by the minidom module. Most XML libraries that I have experience of would have similar problems since they want parse the whole structure into memory. In this case, something custom could be done to parse the XML just like a text file line by line but it would be slightly messier and require more coding time. More likely, you would probably want to consider something other than XML for transmitting the data if it was of this magnitude.

One piece of additional functionality that I thought would be useful and added to the parseTransactionsCsv function was to enable searching within a date range. I tested this but did not expose it to the command line.

