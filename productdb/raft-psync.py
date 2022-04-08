# The MIT License (MIT)

# Copyright (c) 2016 Filipp Ozinov

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#https://github.com/bakwc/PySyncObj/blob/master/LICENSE.txt 



from pysyncobj import SyncObj
from pysyncobj.batteries import ReplCounter, ReplDict

counter1 = ReplCounter()
counter2 = ReplCounter()
dict1 = ReplDict()
syncObj = SyncObj('34.135.156.30:4321', ['35.238.251.17:4321','34.67.154.45:4321'], consumers=[counter1, counter2, dict1])

counter1.set(42, sync=True) # set initial value to 42, 'sync' means that operation is blocking
counter1.add(10, sync=True) # add 10 to counter value
counter2.inc(sync=True) # increment counter value by one
#dict1.set('testKey1', 'testValue1', sync=True)
#dict1['testKey2'] = 'testValue2' # this is basically the same as previous, but asynchronous (non-blocking)
print(counter1, counter2, dict1['testKey1'], dict1.get('testKey2'))