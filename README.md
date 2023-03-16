Prep

```
pyenv virtualenv 3.10.6 gpt-export-3.10.6
echo "gpt-export-3.10.6" > .python-version
pip install -r requirements.txt
```


Get HTML from chat session by right-clicking on the chat and selecting "Save as HTML".


Then run


```
python script.py input/htmlfile.html
```

Output will be in output/ directory, and modified HTML will be in input/ directory for debugging purposes.