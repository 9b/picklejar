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
myjar.store('testObj', myobj)

# pull from the pickle jar
reloaded = myjar.get('testObj')

# enjoy!
print reloaded

</pre>
