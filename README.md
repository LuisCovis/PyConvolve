# PyConvolve
This project consists of an application that can apply the convolution operation to analyze the system's 
response to a given input, knowing its reactive response

## Todo list

* ~~Quick user input cleaning~~
    * ~~Block quotes to avoid scaping the eval() function~~
    * ~~Block special characters such as "{´`$%\\}"~~

* Parse said input to generate the desired function inside Python
    * ~~Given the user input, generate a string that can be evaluated for any input~~
    * ~~Detect if the function is undefined between the desired range of observation~~
    * ~~Graph the functions with a given range of input values for testing~~
    * Add extra parsing functionality (constants and functions (dirac and unit step))
* Apply convolution between functions
    * Take inputs to modify the output behaviour (global variables)
    * Graph the system response
