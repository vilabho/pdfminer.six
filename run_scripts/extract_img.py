import pdfminer
from pdfminer.image import ImageWriter
from pdfminer.high_level import extract_pages


def get_image(layout_object):
    # recursively locate Image objects in page_layout
    if isinstance(layout_object, pdfminer.layout.LTImage):
        return [layout_object]
    if isinstance(layout_object, pdfminer.layout.LTContainer):
        img_list = []
        for child in layout_object:
            img_list = img_list + get_image(child)
        return img_list
    else:
        return []


def extract_pdf_img(pdf_filepath):
    iw = ImageWriter('output_dir')
    for page_layout in extract_pages(pdf_filepath):
        image_list = get_image(page_layout)
        if len(image_list):
            for image in image_list:
                iw.export_image(image)


if __name__ == "__main__":
    pdf_filepath = r"C:\projects\git-repos\pdfminer.six\samples\simple1.pdf"
    extract_pdf_img(pdf_filepath)
