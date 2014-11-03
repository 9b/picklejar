# PickleJar

PickleJar helps you keep track of all your pickled items and makes it easy to restore things you previously pickled.

Using the jar is simple:

<pre>
from picklejar import PickleJar

# create a new jar instance
myjar = PickleJar()

# provide location of your pickles or use the default (/picklejar)
jarMeta = myjar.meta() # returns metadata about the jar

# sample data
myobj = { 'one': 1, 'two': 2, 'three': 3 }

# store your object with an id
myjar.put('testObj', myobj)

# pull from the pickle jar
reloaded = myjar.get('testObj')

# enjoy!
print reloaded

</pre>

# Using Brine

Brine provides a decorator for a function that inspects the local variables for the items you wish to pickle. This functionality is provided using the scope parameter.

There are three types of scope:

| Scope             | Explanation                                                      |
|-------------------|------------------------------------------------------------------|
| __all__           | Attempts to save all variables using their name as the unique ID |
| [ 'a', 'b', 'c' ] | Attempts to save all variables listed within the scope           |
| None              | Attempts to only save the variables named "_dill" and "_id"      |

Here's a test function:

<pre>
from picklejar import brine

@brine(scope=['__all__'])
def getWebsite(url):
    website = requests.get(url) # item to pickle
    return website

getWebsite('https://www.google.com')
</pre>

If you are not using the default location for your jar, then you will need to pass your jar instance to the brine method (after scope)
