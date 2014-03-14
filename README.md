# Bug Buster #
Bug buster is an implementation of a small shape recognition exercise for ASCII art shapes.

## Basic Description ##

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

## Extra features ##

In addition, I plan on adding further features and handling for edge cases, like:
* Handling corrupted input and partially covered bugs using a detection threshold
* Bug rotation (?) or multiple types of bugs
* Colorized output to distinguish bugs next to each other

## Related: Bliffoscope ##

The task solved by Bug Buster is similar to **Bliffoscope**, which seems to be sort of an developer job interview exercise.

See [StackOverflow question](https://stackoverflow.com/questions/14246120/locate-an-ascii-art-image-inside-a-body-of-text-with-a-certain-toleration-for-er) and [an implementation on GitHub](https://github.com/samhart/bliffoscope).
