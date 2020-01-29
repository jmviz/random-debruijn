# random-debruijn

Python code for generating random [de Bruijn sequences](https://en.wikipedia.org/wiki/De_Bruijn_sequence).  

## Command line usage
Generate a random de Bruijn sequence of order 4 on an alphabet of size 2:
```Shell
python debruijn.py 2 4
```
Example output:
```Shell
0010100110111100
```

Generate a 2-fold random de Bruijn sequence of order 2 on an alphabet of size 4:
```Shell
python debruijn.py 4 2 -f 2
```
Example output:
```Shell
22131320301010311233300020232112
```

## Generating trial sequences for experiments
Say you have an experiment where each trial has 2 factors, each with 2 levels, making a total of 2 × 2 = 4 trial types. To generate a de Bruijn block of trials where each length-2 subsequence of trial types occurs exactly once:
```Python
import debruijn
probe = [True, False]
orientation = ["left", "right"]
sequencer = debruijn.Sequencer(2, probe, orientation)
block = sequencer.block()
print(block)
```
Example output:

```
[(True, 'right'), (False, 'right'), (False, 'right'), (False, 'left'), (True, 'right'), (True, 'left'), (True, 'left'), (False, 'right'), (True, 'left'), (False, 'left'), (False, 'left'), (True, 'left'), (True, 'right'), (True, 'right'), (False, 'left'), (False, 'right')]
```

See comments in code for more details and options.
