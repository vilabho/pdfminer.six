.. _images:

How to extract images from a PDF
********************************

Through Command Line
============

Before you start, make sure you have :ref:`installed pdfminer.six<install>`.
The second thing you need is a PDF with images. If you don't have one,
you can download `this research paper
<https://www.robots.ox.ac.uk/~vgg/publications/2012/parkhi12a/parkhi12a.pdf>`_
with images of cats and dogs and save it as `example.pdf`::

    $ curl https://www.robots.ox.ac.uk/~vgg/publications/2012/parkhi12a/parkhi12a.pdf --output example.pdf

Then run the :ref:`pdf2txt<api_pdf2txt>` command::

    $ pdf2txt.py example.pdf --output-dir cats-and-dogs

This command extracts all the images from the PDF and saves them into the
`cats-and-dogs` directory.


Programmatically
============
pdfminer's high-level api has separate instance - `pdfminer.layout.LTImage` specifically for image objects in pdfs.

To extract only image objects from a given pdf, we can iterate over every object in the pdf
(recursively, since some objects are embedded within other object), and then check each object if it is of
`LTImage` type.


.. code-block:: python

    import pdfminer
    from pdfminer.image import ImageWriter
    from pdfminer.high_level import extract_pages


    def get_image(layout_object):
        # recursively locate Image objects in page_layout
        if isinstance(layout_object, pdfminer.layout.LTImage):
            # True, if layout object is of type - pdfminer.layout.LTImage
            return [layout_object]
        if isinstance(layout_object, pdfminer.layout.LTContainer):
            # True, if object is a container, which contains more object
            img_list = []
            for child in layout_object:
                img_list = img_list + get_image(child)
            return img_list
        else:
            return []


    def extract_pdf_img(pdf_filepath):
        # providing directory for image writing
        iw = ImageWriter('output_dir')

        # iterating through pdf pages
        for page_layout in extract_pages(pdf_filepath):
            image_list = get_image(page_layout)
            if len(image_list):
                for image in image_list:
                    iw.export_image(image)


    if __name__ == "__main__":
        pdf_filepath = r"C:\projects\git-repos\pdfminer.six\samples\SamplePdf.pdf"
        extract_pdf_img(pdf_filepath)

The function `extract_pdf_img` goes through each page and then it uses `get_image` function (recursively, since image objects
could be embedded in Container object.