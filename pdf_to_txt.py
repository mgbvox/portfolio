import sys
import os
import numpy as np
import matplotlib.pyplot as plt


from pdf2image import convert_from_path
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

in_file = sys.argv[1]

if '.pdf' not in in_file:
    print('Could not read file. Please enclose pdf filename in quotation marks.')
else:
    print('Converting PDF to Images...')
    pages = convert_from_path(in_file, 500)
    print('Converted {} pages!'.format(len(pages)))
    print('Processing page images to text.')

    if not os.path.isdir('text'):
        os.mkdir('text')

    file = open('text/{}'.format(in_file.split('.')[0]+'.txt'), 'a+')
    for page_number, page in enumerate(pages):
        ppm = page
        plt.imsave('text/temp.jpg',np.array(ppm))
        img = Image.open('text/temp.jpg')
        txt = pytesseract.image_to_string(img)
        file.write(txt)
        print('Processed {} pages of {}'.format(page_number+1, len(pages)))
    file.close()

