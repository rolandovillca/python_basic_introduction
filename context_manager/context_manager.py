'''
Context Managers:

Context managers allow setup and cleanup actions to be taken for objects when
their creation is wrapped with a with statement. The behavior of the context
manager is determined by two magic methods:

__enter__(self):
Defines what the context manager should do at the beginning of the block created
by the with statement. Note that the return value of __enter__ is bound to the
target of the with statement, or the name after the as.

__exit__(self, exception_type, exception_value, traceback)
Defines what the context manager should do after its block has been executed
(or terminates). It can be used to handle exceptions, perform cleanup,
or do something always done immediately after the action in the block.
If the block executes successfully, exception_type, exception_value,
and traceback will be None. Otherwise, you can choose to handle the exception
or let the user handle it; if you want to handle it, make sure __exit__ returns
True after all is said and done. If you don't want the exception to be handled
by the context manager, just let it happen.

__enter__ and __exit__ can be useful for specific classes that have well-defined
and common behavior for setup and cleanup. You can also use these methods to
create generic context managers that wrap other objects.

The defining feature of a context manager is that it has two special methods:
__enter__() and __exit__(). These are used by the with statement to enter and
exit the context, (think of it as a try-finally block).
'''

# EXAMPLE 1:
# ==============================================================================
class DatabaseConnection(object):
    # Make database connection and return it.
    def __enter__(self):
        return self.dbconn

    # Make sure the database connecton gets closed.
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbconn.close()

with DatabaseConnection() as mydbconn:
    # Do stuff.


# EXAMPLE 2:
# ==============================================================================
class Rectangle:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
    
    def __enter__(self):
        print 'in __enter__'
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        print '__exit__'

    def device_by_zero(self):
        # Causes ZeroDivisionError exception
        return self.width / 0

with Rectangle(3, 4) as rectangle:
    # Exception successfully pass to __exit__
    rectangle.device_by_zero()

# Output should be:
# "in __enter__"
# "in __exit__"
# Traceback (most recent call last):
#   File "e0235.py", line 27, in <module>
#     r.divide_by_zero()


# EXAMPLE 3:
# ==============================================================================
class MyClass(object):
    def __enter__(self):
        if moon_phase > 0:
            self.returnval = 123
        else:
            self.returnval = 456
        return returnval

    def __exit__(self, *args):
        number = self.returnval
        print 'End of block with', number

with MyClass() as x:
    print x   # 123
    with MyClass() as y:
        print x, 'and', y   # 123 and 456

    print x   # 123


# EXAMPLE 4: Using contextlib module contains utilities:
# ==============================================================================
'''
The contextlib module contains utilities for working with context managers and the with statement.

Note Context managers are tied to the with statement.
Since with is officially part of Python 2.6,
you have to import it from __future__ before using contextlib in Python 2.5.

A context manager is enabled by the with statement, and the API involves two methods.
The __enter__() method is run when execution flow enters the code block inside the with.
It returns an object to be used within the context.
When execution flow leaves the with block, the __exit__() method of the context manager
is called to clean up any resources being used.
'''
class Context(object):

    def __init__(self):
        print '__init__()'

    def __enter__(self):
        print '__enter__()'
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print '__exit__()'
        
with Context():
    print 'Doing work in the context'


# EXAMPLE 5: Return a context manager that closes thing upon completion of the block:
# ==============================================================================
# Creating a Context Manager using contextlib.
from contextlib import contextmanager

@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()

# And lets you write code like this:
from contextlib import closing
import urllib

with closing(urllib.urlopen('http://www.python.org')) as page:
    for line in page:
        print line
# without needing to explicitly close page.
# Even if an error occurs, page.close() will be called when the with block is exited.


# EXAMPLE 6: Return a context manager that closes thing upon completion of the block:
# ==============================================================================
'''
Context managers allow you to allocate and release resources precisely when you want to.
The most widely used example of context managers is the with statement.
Suppose you have two related operations which you’d like to execute as a pair,
with a block of code in between. Context managers allow you to do specifically that.
'''
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)

    def __enter__(self):
        return self.file_obj


    def __exit__(self, type, value, traceback):
        self.file_obj.close()

# Just by defining __enter__ and __exit__ methods we can use it in a with statement.
with File('demo.txt', 'w') as opened_file:
    opened_file.write('Hola!')


# EXAMPLE 7:
# ==============================================================================
import sqlite3

class DataConn(object):

    # Constructor
    def __init__(self, db_name):
        self.db_name = db_name

    # Open the database connection
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    # Close connection
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

if __name__ == "__main__":
    db = '/home/mdriscoll/test.db'
    with DataConn(db) as conn:
        cursor = conn.cursor()

# EXAMPLE 8: Creating a Context Manager using contextlib:
# ==============================================================================
'''
Python 2.5 not only added the with statement, but it also added the contextlib module.
This allows us to create a context manager using contextlib’s contextmanager function as a decorator.
'''
from contextlib import contextmanager

@contextmanager
def file_open(path):
    try:
        f_obj = open(path, 'w')
        yield f_obj
    except OSError:
        print 'We had an error!'
    finally:
        print 'closing the file'
        f_obj.cose()

# Implement example 8:
if __name__ == '__main__':
    with file_open('/home/mdriscoll/test.txt') as fobj:
        fobj.write('Testing context manager')