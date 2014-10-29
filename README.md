PickleJar helps you keep track of all your pickled items and makes it easy to restore things you previously pickled. 

Usage is simple:

from picklejar import PickleJar
myjar = PickleJar()
jarMeta = myjar.pickles() # returns metadata about the jar
myobj = { 'one': 1, 'two': 2, 'three': 3 }
myjar.store('testObj', myobj)
reloaded = myjar.get('testObj')
print reloaded