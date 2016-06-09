# JsParser
A small tool to parse JavaScript segment. Before using this tool, make sure that your javascript code is strict mode.

JsParser requires [PLY](http://github.com/dabeaz/ply).

First install PLY:

>	pip install -r requirements.txt
	
usage:

>	python parser.py --JS_FILENAME

example:

>


### Example:
	define(['path'], function(para) {
	    var name = 'leon';
	    return {
	        'name' : name
	    };
	});	
	
#### Result:

	{'__type__': 'program',
	 'function': {'__type__': 'function',
	              'parameters': ['para'],
	              'statements': [{'__type__': 'statement',
	                              'statement': ['var',
	                                            ['name',
	                                             '=',
	                                             "'leon'"]]},
	                             {'__type__': 'statement',
	                              'statement': {"'name'": 'name'}}]},
	 'parameter': ["'path'"]}
	 