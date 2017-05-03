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
        ## Split errors
        ## filter using the condition Error in splits
        ## put one for the concerned errors
        ## Counts the by accumulating the sum
        counts = lines.flatMap(lambda line: line.split(" "))\
                    .filter(lambda word:"ERROR" in word)\
                    .map(lambda word : (word, 1))\
                    .reduceByKey(lambda a, b : a + b)

        ## Display the counts
        ## Start the program
        ## The program will run until manual termination
        counts.pprint()
        ssc.start()
        ssc.awaitTermination()

