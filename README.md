# Get started with Spark Streaming

## Installation
Follow this tutorial to install spark :
https://www.tutorialspoint.com/apache_spark/apache_spark_installation.htm

## A streaming example
Here we will just count the number of errors that occur on instantanously

### firstStreamApp.py
The example to run with python
```shell
# Import libs
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        sc = SparkContext(appName="StreamingErrorCount");
        # 2 is the batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        # Checkpoint for backups
        ssc.checkpoint("file:///tmp/spark")

        # Define the socket where the system will listen
        # Lines is not a rdd but a sequence of rdd, not static, constantly changing
        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))


        # Counting errors
        counts = lines.flatMap(lambda line: line.split(" "))\
                    .filter(lambda word:"ERROR" in word)\
                    .map(lambda word : (word, 1))\
                    .reduceByKey(lambda a, b : a + b)
        counts.pprint()
        ssc.start()
        ssc.awaitTermination()
```

### Open a socket
Open a socker on port 9999 using netcat in a shell
```shell
$ nc -l -p 9999
```

### Check if the port is opened
Open a socker on port 9999 using netcat
```shell
$ nc localhost 9999
```

### Submit the python script
Open a socker on port 9999 using netcat
```shell
$ spark-submit firstStreamApp.py localhost 9999
```

### You'll see time slots

```shell
$ spark-submit firstStreamApp.py localhost 9999
17/04/12 10:38:15 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
-------------------------------------------
Time: 2017-04-12 10:38:18
-------------------------------------------

-------------------------------------------
Time: 2017-04-12 10:38:20
-------------------------------------------

-------------------------------------------
Time: 2017-04-12 10:38:22
-------------------------------------------

-------------------------------------------
Time: 2017-04-12 10:38:24
-------------------------------------------

-------------------------------------------
Time: 2017-04-12 10:38:26
-------------------------------------------

-------------------------------------------
Time: 2017-04-12 10:38:28
-------------------------------------------

```

### Test
On the shell where netcat was launch, write textes with "ERROR" to check
```shell
ERROR is there
NOTHING HERE
Everything is ok
ERROR AGAIN
A LOT OF ERRORS



ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR
ERROR





```


### The output
On the shell where netcat was launch, write textes with "ERROR" to check
```shell
...
17/04/12 10:42:12 WARN RandomBlockReplicationPolicy: Expecting 1 replicas with only 0 peer/s.
17/04/12 10:42:12 WARN BlockManager: Block input-0-1491986532000 replicated to only 0 peer(s) instead of 1 peers
-------------------------------------------
Time: 2017-04-12 10:42:12
-------------------------------------------

17/04/12 10:42:13 WARN RandomBlockReplicationPolicy: Expecting 1 replicas with only 0 peer/s.
17/04/12 10:42:13 WARN BlockManager: Block input-0-1491986533200 replicated to only 0 peer(s) instead of 1 peers
[Stage 473:>                                                        (0 + 0) / 2]17/04/12 10:42:14 WARN RandomBlockReplicationPolicy: Expecting 1 replicas with only 0 peer/s.
17/04/12 10:42:14 WARN BlockManager: Block input-0-1491986534000 replicated to only 0 peer(s) instead of 1 peers
-------------------------------------------                                     
Time: 2017-04-12 10:42:14
-------------------------------------------
(u'ERROR', 2)

17/04/12 10:42:14 WARN RandomBlockReplicationPolicy: Expecting 1 replicas with only 0 peer/s.
17/04/12 10:42:14 WARN BlockManager: Block input-0-1491986534200 replicated to only 0 peer(s) instead of 1 peers
-------------------------------------------

....



-------------------------------------------
Time: 2017-04-12 10:44:10
-------------------------------------------

17/04/12 10:44:10 WARN RandomBlockReplicationPolicy: Expecting 1 replicas with only 0 peer/s.
17/04/12 10:44:10 WARN BlockManager: Block input-0-1491986650600 replicated to only 0 peer(s) instead of 1 peers
17/04/12 10:44:11 WARN RandomBlockReplicationPolicy: Expecting 1 replicas with only 0 peer/s.
17/04/12 10:44:11 WARN BlockManager: Block input-0-1491986651600 replicated to only 0 peer(s) instead of 1 peers
-------------------------------------------
Time: 2017-04-12 10:44:12
-------------------------------------------
(u'ERROR', 40)

-------------------------------------------
Time: 2017-04-12 10:44:14
-------------------------------------------


```




## UpdateStateByKey
Stateful transformation using Dstreams
### updateSateByKey.py
The script to be processed for a summary count. 
```shell
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        sc = SparkContext(appName="StreamingErrorCount");
        # 2 is the batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        # Checkpoint for backups
        ssc.checkpoint("file:///tmp/spark")

        # Define the socket where the system will listen
        # Lines is not a rdd but a sequence of rdd, not static, constantly changing
        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))



        # Update function
        def countWords(newValues, lastSum):
            if lastSum is None :
                lastSum = 0
            return sum(newValues, lastSum)

        word_counts = lines.flatMap(lambda line: line.split(" "))\
                    .map(lambda word : (word, 1))\
                    .updateStateByKey(countWords)

        word_counts.pprint()
        ssc.start()
        ssc.awaitTermination()

```

### Launch the netcat utility as previously
```shell
$ nc -l -p 9999
```

### Submit the python script 
Open a socker on port 9999 using netcat
```shell
$ spark-submit updateSateByKey.py localhost 9999
```





## countByWindow
Stateful transformation using Dstreams
### countByWindow .py
The script to be processed for a summary count. 
```shell
# Import libs
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        sc = SparkContext(appName="StreamingcountByWindow");
        # 2 is the batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        # Checkpoint for backups
        ssc.checkpoint("file:///tmp/spark")

        # Define the socket where the system will listen
        # Lines is not a rdd but a sequence of rdd, not static, constantly changing
        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

        ## window size = 10, sliding interval = 2
        counts = lines.countByWindow(10, 2)

        ## Display the counts
        ## Start the program
        ## The program will run until manual termination
        counts.pprint()
        ssc.start()
        ssc.awaitTermination()

```

### Launch the netcat utility as previously
```shell
$ nc -l -p 9999
```

### Submit the python script 
Open a socker on port 9999 using netcat
```shell
$ spark-submit updateSateByKey.py localhost 9999
```







## reduceByWindow
Stateful transformation using Dstreams
### reduceByWindow.py
The script to be processed for a summary count. 
```shell
# Import libs
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        sc = SparkContext(appName="StreamingreduceByWindow");
        # 2 is the batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        # Checkpoint for backups
        ssc.checkpoint("file:///tmp/spark")

        # Define the socket where the system will listen
        # Lines is not a rdd but a sequence of rdd, not static, constantly changing
        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

        ## summary function
        ## reverse function
        ## window size = 10
        ## sliding interval = 2
        sum = lines.reduceByWindow(
                lambda x, y: int(x) + int(y),
                lambda x, y: int(x) - int(y),
                10,
                2
        )

        ## Display the counts
        ## Start the program
        ## The program will run until manual termination
        sum.pprint()
        ssc.start()
        ssc.awaitTermination()

```

### Launch the netcat utility as previously
```shell
$ nc -l -p 9999
```

### Submit the python script 
Open a socker on port 9999 using netcat
```shell
$ spark-submit reduceByWindow.py localhost 9999
```



## reduceByKeyAndWindow
Stateful transformation using Dstreams
### reduceByKeyAndWindow.py
The script to be processed for a summary count. 
```shell


```

### Launch the netcat utility as previously
```shell
$ nc -l -p 9999
```

### Submit the python script 
Open a socker on port 9999 using netcat
```shell
$ spark-submit reduceByKeyAndWindow.py localhost 9999
```



StreamingreduceByKeyAndWindow