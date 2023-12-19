= First install the dependencies using requirements.txt
    pip3 install -r requirements.txt

= to run the code, use the following command, where <filename> is the name of the XML file
    python3 main.py <filename>

= Code Explanation
Each order book has been maintained as a class, where two members are self.buyOrders and self.sellOrders
which have been implemented as Red-Black Trees, which offer the benefit of search trees and balanced trees.
The invariant is that the maximum element is self.buyOrders is less than the minimum element of self.sellOrders
at the end of every iteration. Between iterations we find matches in the trees, and then reduce the volume accordingly,
and remove and add nodes from the trees as per requirement.

Currently, the code streams the XML file into memory and maintains the OrderBooks, and bookMap = {} is dictionary which
has the OrderBook given their bookId as key.

= Improvements
Since each bookId and its OrderBook is seperate we could use multithreading and multiprocessing to do them in parallel.
However due to python's limitaion in multithreading due to the GIL, it is better to utilize all the CPU cores using multiprocessing

However, we could also use distributed programming using dask. We can maintain OrderBooks at different computers, and one computer
reads the XML file and assigns the Order using its bookId to a computer. This is very efficient and scales really well.