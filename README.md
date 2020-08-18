# pagerank
An implementation of PageRank Algorithm for course CS6200

## Intructions to run code
Run the pageranktask.py from the command prompt as follows:
```
python pageranktask.py <edges-file> <vertices-file>
```
Example:

``` 
python pageranktask.py edges-edu.txt vertices-edu.txt
```
## Input
Input for this program has to arranged in the form of two files that describe vertice and edge information.
Follwing sample input files have been included:
* edges-file : edges-edu.txt, toy-edges.txt
* vertices-file : vertices-edu.txt, toy-vertices.txt

## Results
Running the above produces the following output:
* Proportion of source pages
* Proportion of sink pages
* Proportion of pages with pagerank less than initial pagerank values
* Top 50 pages sorted by their pagerank values
* Top 50 pages sorted by their inlink counts

## Requirements
Python 3.6+ is required to run this program. No additional modules have to be installed as the program makes use of inbuilt modules only. 
