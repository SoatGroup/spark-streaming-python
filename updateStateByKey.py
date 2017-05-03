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



        # Update function
        def countWords(newValues, lastSum):
            if lastSum is None :
                lastSum = 0
            return sum(newValues, lastSum)

        word_counts = lines.flatMap(lambda line: line.split(" "))\
                    .map(lambda word : (word, 1))\
                    .updateStateByKey(countWords)

        ## Display the counts
        ## Start the program
        ## The program will run until manual termination
        word_counts.pprint()
        ssc.start()
        ssc.awaitTermination()

