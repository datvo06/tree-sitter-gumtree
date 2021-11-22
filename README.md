# A Tree-Sitter - Gumtree Differentiation Co-packages

## Json object format for communicating between jars file
### Single json dict for description of an AST Tree:
- The input to `ast_diff.jar`  is as follows:
```json
"file1":{
	"nodes" {
		{
			"1": {
			}
		}
	}
}
```

## Running
### Download Jars file
[Download the `jars.zip` and unzip into `jars` folder](https://drive.google.com/file/d/18m3fhSdxhCuAS2aZuUROo2QLMSneuEcP/view?usp=sharing)
### Install requirements
```bash
pip install tree-sitter
pip install networkx
```
### Example
Get map by line
```bash
python3 get\_mapping\_by\_line <file1> <file2> <out_file>
```
