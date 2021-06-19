# Marking points tool

![Alt Text](https://media.giphy.com/media/lUSXwryh9sVx86GsNa/giphy.gif)

## How to run
Put files into `data/` and run `python app.py`

## Output format
The tool will create `result` folder and put there json files.
The content of json is a list of normalized coordinates in range [0,1].
```
[[x1, y1], [x2, y2], ...]
```

## Supported formats
- jpg
- png
- mp4
- mkv

For video, the tool will take the first frame for labeling.
