#Cleanscan

A document image cleaner.

Cleanscan attempts to clean up an image of a document. It can for instance be used to improve the performance of subsequent optical character recognition (OCR). 

## Installation

```bash
pip3 install git+https://github.com/troelsfrostholm/cleanscan.git
```

## Usage

```bash
cleanscan <input-image> <output-image>
```

input-image is the path to an image of the document you want to clean up
output-image is the path of the cleaned up image that is generated

Cleanscan looks for the outline of the document and fails if it can't be found. So it only works on a rectangular piece of paper, with the entire paper in the picture, and preferably a contrast with the background. 
