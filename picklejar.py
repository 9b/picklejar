import cPickle, os, datetime, sys, hashlib, functools
    
class PickleJar():
    LOCATION = '/picklejar'
    PICKLEJAR = 'picklejar.pickle'
    
    def __init__(self, location=None):
        self.__jarContents = {
            'overwrite': True,
            'mappings': {},
            'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated': None,
            'pickles': 0,
            'savePoint': None
        }
        self.__writePoint = None
        
        if not location:
            location = self.LOCATION
        if location.endswith('/'): location[:-1]    
        
        check = location + '/' + self.PICKLEJAR
        if os.path.exists(location):
            if os.path.isfile(check):
                with open(check, "rb") as jarMap:
                    self.__jarContents = cPickle.load(jarMap)
                jarMap.close()
            else:
                self.__save(check)
        else:
            os.makedirs(location)
            self.__save(check)
            
        self.__writePoint = location + '/'
        
    def __save(self, check=None):
        '''
        Save the jar mapping as a pickle inside our jar
        '''
        if not check:
            check = self.__jarContents['savePoint']
        
        self.__jarContents['pickles'] = len(self.__jarContents['mappings'].keys())
        self.__jarContents['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__jarContents['savePoint'] = check
        
        with open(check, "wb") as jarMap:
            cPickle.dump(self.__jarContents, jarMap)
        jarMap.close()
    
    def meta(self, location=None):
        '''
        Create or open a picklejar for editing and use the map as a guide
        @returns    metadata describing the jar and its contents
        '''
        return self.__jarContents
        
    def put(self, id, pickle):
        '''
        Take a data object and try to pickle it in our jar
        1) attempt to pickle
        2) collect meta about the pickle
        3) derive a mapping
        4) store the pickle in the jar
        5) update our jar map
        '''
        try: 
            cPickle.dumps(pickle)
        except cPickle.PicklingError: 
            raise ValueError('NOTAPICKLE', 'Your data cannot be pickled')
         
        meta = { 
            'id': id,
            'dir': dir(pickle),
            'module': pickle.__module__,
            'type': type(pickle).__name__,
            'size': sys.getsizeof(pickle)
        } 
        
        pid = hashlib.sha256(id).hexdigest()
        location = self.__writePoint + pid + '.pickle'
        if os.path.isfile(location) and not self.__jarContents['overwrite']:
            raise ValueError('OVERWRITE', 'Your jar is not set to overwrite pickles. Set this option and retry or pick a different ID')
            
        with open(location, "wb") as pickled:
            cPickle.dump(pickle, pickled)
        pickled.close()
        
        self.__jarContents['mappings'][pid] = meta
        self.__save()
    
    def get(self, id):
        '''
        Grab the pickle from the jar
        @returns    the actual unpickled value
        '''
        id = hashlib.sha256(id).hexdigest()
        if self.__jarContents['mappings'].has_key(id):
            pname = id + '.pickle'
            with open(self.__writePoint + pname, "rb") as brined:
                contents = cPickle.load(brined)
            brined.close()
            return contents
        else:
            raise ValueError('NOTFOUND', 'The pickle ID you specified does not exist inside this jar')

    @property
    def writePoint(self):
        return self.__writePoint
        
class brine(object):
    def __init__(self, jar=PickleJar()):
        self.__locals = {}
        self.__jar = jar

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            def tracer(frame, event, arg):
                if event=='return':
                    self.__locals = frame.f_locals.copy()
                
            # tracer is activated on next call, return or exception
            sys.setprofile(tracer)
            try: res = fn(*args, **kwargs) # trace the function call
            finally: sys.setprofile(None) # disable tracer and replace with old one
            self.__handle(self) # see if we have a pickle
            return res
        return decorated

    def __handle(self, context):
        if not context.__locals.has_key('_dill'): return
        if not context.__locals.has_key('_pid'): return
        try: context.__jar.put(context.__locals['_pid'], context.__locals['_dill'])
        except: pass
        return True
