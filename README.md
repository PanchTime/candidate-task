# Grigori Panciohin candidate task

## Description
This is a test task for Grigori Panciohin. The task is to create an XML parser that parses specific XML files.

1. The parser accepts a path to the XML file as an argument.
2. The parser parses the XML file and prints the result to the console.
3. Bonus features:
   1. Implement conditional filtering of the output.
   2. Accept conditional filtering as JSON file in an argument. Output only values and attributes that match the conditions.
   3. Save output in a txt file. Save logs in a separate file including relevant information about the parsing process.
   4. Come up with DB structure for the parsed data.

## How to use

### Prerequisites
- DEB-based Linux distribution
- docker and docker-compose (Optional)
- python >= 3.7
- create `data` directory in the root and put the test XML file there

### Run with docker
Make sure you have docker and docker-compose installed. Then run the following commands:
```bash
docker-compose up --build
```
To specify which file to parse and other settings change variables in the `docker-compose.yml` file.

### Run without docker
Make sure you have python >= 3.7 installed. Then run the following commands:

Create a virtual environment:
```bash
python3 -m venv venv
```
Activate the virtual environment:
```bash
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the parser:
```bash
python run.py --f ./data/F000016EPD.xml
```

## Notes
Using `filter_config.json` to apply filters and print only the desired data,
`rules` should include at `path` and one of `text` or `attr_name` keys.


# TODO
- [ ] Add more tests
