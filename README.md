# Bug Buster #
Bug Buster is an implementation of a shape recognition exercise for ASCII art shapes.

## Task Description ##

Given a bug specification

	| |
	###O
	| |


the program should be able to spot three bugs in this landscape:

                                       
    | |                                
    ###O                               
    | |           | |                  
                  ###O                 
                  | |              | | 
                                   ###O
                                   | | 


Whitespaces are not part of the bug specification, hence these fields could contain other symbols in more complicated landscapes.

## Example Invocation ##

    $ python main.py test-res/bug.txt test-res/landscape.txt 
    3

## Running The Tests ##

    $ python tests.py

## Related: Bliffoscope ##

The task solved by Bug Buster is similar to **Bliffoscope**, which seems to be sort of an developer job interview exercise.

See [StackOverflow question](https://stackoverflow.com/questions/14246120/locate-an-ascii-art-image-inside-a-body-of-text-with-a-certain-toleration-for-er) and [an implementation on GitHub](https://github.com/samhart/bliffoscope).
