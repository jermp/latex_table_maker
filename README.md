Latex Table Maker
--

A simple python script to parse json
into a latex table.
This is intended to provide a basic
table skeleton that to be then refined.

### Example

The command

	$ python create_table example.json example.tex > test.tex
	
creates a `example.tex` file from the json file
`example.json`
provided as an example and print a minimal
latex document into `test.tex` that can be
compiled with

	$ pdflatex test.tex


### Input data format

1. The input json file should contain a line for
each row of the table.

2. All lines should contain the same fields.

3. The first line of the file should indicate
the type of each field, e.g., `string`, `float`
or `int` field. (Floats are formatted using 2 decimal digits by default.)

See the file `example.json`.

	

