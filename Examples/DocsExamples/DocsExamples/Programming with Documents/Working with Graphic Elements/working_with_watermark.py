import unittest
import os
import sys

base_dir = os.path.abspath(os.curdir) + "/"
base_dir = base_dir[:base_dir.find("Aspose.Words-for-Python-via-.NET")]
base_dir = base_dir + "Aspose.Words-for-Python-via-.NET/Examples/DocsExamples/DocsExamples"
sys.path.insert(0, base_dir)

import docs_examples_base as docs_base

import aspose.words as aw
import aspose.pydrawing as drawing

class WorkWithWatermark(docs_base.DocsExamplesBase):
    
    def test_add_text_watermark_with_specific_options(self) :
        
        #ExStart:AddTextWatermarkWithSpecificOptions
        doc = aw.Document(docs_base.my_dir + "Document.docx")

        options = aw.TextWatermarkOptions()
            
        options.font_family = "Arial"
        options.font_size = 36
        options.color = drawing.Color.black
        options.layout = aw.WatermarkLayout.HORIZONTAL
        options.is_semitrasparent = False
            

        doc.watermark.set_text("Test", options)

        doc.save(docs_base.artifacts_dir + "WorkWithWatermark.add_text_watermark_with_specific_options.docx")
        #ExEnd:AddTextWatermarkWithSpecificOptions
        

#if NET462
    def test_add_image_watermark_with_specific_options(self) :
        
        #ExStart:AddImageWatermarkWithSpecificOptions
        doc = aw.Document(docs_base.my_dir + "Document.docx")

        options = aw.ImageWatermarkOptions()
            
        options.scale = 5
        options.is_washout = False
            

        doc.watermark.set_image(docs_base.images_dir + "Transparent background logo.png", options)

        doc.save(docs_base.artifacts_dir + "WorkWithWatermark.add_image_watermark.docx")
        #ExEnd:AddImageWatermarkWithSpecificOptions
        

    def test_remove_watermark_from_document(self) :
        
        #ExStart:RemoveWatermarkFromDocument
        doc = aw.Document()

        # Add a plain text watermark.
        doc.watermark.set_text("Aspose Watermark")

        # If we wish to edit the text formatting using it as a watermark,
        # we can do so by passing a TextWatermarkOptions object when creating the watermark.
        textWatermarkOptions = aw.TextWatermarkOptions()
        textWatermarkOptions.font_family = "Arial"
        textWatermarkOptions.font_size = 36
        textWatermarkOptions.color = drawing.Color.black
        textWatermarkOptions.layout = aw.WatermarkLayout.DIAGONAL
        textWatermarkOptions.is_semitrasparent = False

        doc.watermark.set_text("Aspose Watermark", textWatermarkOptions)

        doc.save(docs_base.artifacts_dir + "Document.text_watermark.docx")

        # We can remove a watermark from a document like this.
        if (doc.watermark.type == aw.WatermarkType.TEXT) :
            doc.watermark.remove()

        doc.save(docs_base.artifacts_dir + "WorkWithWatermark.remove_watermark_from_document.docx")
        #ExEnd:RemoveWatermarkFromDocument
        
#endif

    #ExStart:AddWatermark
    def test_add_and_remove_watermark(self) :
        
        doc = aw.Document(docs_base.my_dir + "Document.docx")

        self.insert_watermark_text(doc, "CONFIDENTIAL")
        doc.save(docs_base.artifacts_dir + "TestFile.watermark.docx")

        self.remove_watermark_text(doc)
        doc.save(docs_base.artifacts_dir + "WorkWithWatermark.remove_watermark.docx")
        

    # <summary>
    # Inserts a watermark into a document.
    # </summary>
    # <param name="doc">The input document.</param>
    # <param name="watermarkText">Text of the watermark.</param>
    def insert_watermark_text(self, doc : aw.Document, watermarkText : str) :
        
        # Create a watermark shape, this will be a WordArt shape.
        watermark = aw.drawing.Shape(doc, aw.drawing.ShapeType.TEXT_PLAIN_TEXT)
        watermark.name = "Watermark" 

        watermark.text_path.text = watermarkText
        watermark.text_path.font_family = "Arial"
        watermark.width = 500
        watermark.height = 100

        # Text will be directed from the bottom-left to the top-right corner.
        watermark.rotation = -40

        # Remove the following two lines if you need a solid black text.
        watermark.fill_color = drawing.Color.gray 
        watermark.stroke_color = drawing.Color.gray

        # Place the watermark in the page center.
        watermark.relative_horizontal_position = aw.drawing.RelativeHorizontalPosition.PAGE
        watermark.relative_vertical_position = aw.drawing.RelativeVerticalPosition.PAGE
        watermark.wrap_type = aw.drawing.WrapType.NONE
        watermark.vertical_alignment = aw.drawing.VerticalAlignment.CENTER
        watermark.horizontal_alignment = aw.drawing.HorizontalAlignment.CENTER

        # Create a new paragraph and append the watermark to this paragraph.
        watermarkPara = aw.Paragraph(doc)
        watermarkPara.append_child(watermark)

        # Insert the watermark into all headers of each document section.
        for sect in doc.sections :
            sect = sect.as_section()
            # There could be up to three different headers in each section.
            # Since we want the watermark to appear on all pages, insert it into all headers.
            self.insert_watermark_into_header(watermarkPara, sect, aw.HeaderFooterType.HEADER_PRIMARY)
            self.insert_watermark_into_header(watermarkPara, sect, aw.HeaderFooterType.HEADER_FIRST)
            self.insert_watermark_into_header(watermarkPara, sect, aw.HeaderFooterType.HEADER_EVEN)
            
        

    def insert_watermark_into_header(self, watermarkPara : aw.Paragraph, sect : aw.Section, headerType : aw.HeaderFooterType) :
        
        header = sect.headers_footers.get_by_header_footer_type(headerType)

        if (header == None) :
            
            # There is no header of the specified type in the current section, so we need to create it.
            header = aw.HeaderFooter(sect.document, headerType)
            sect.headers_footers.add(header)
            

        # Insert a clone of the watermark into the header.
        header.append_child(watermarkPara.clone(True))
        
    #ExEnd:AddWatermark
        
    #ExStart:RemoveWatermark
    def remove_watermark_text(self, doc : aw.Document) :
        
        for hf in doc.get_child_nodes(aw.NodeType.HEADER_FOOTER, True) :
            hf = hf.as_header_footer()

            for shape in hf.get_child_nodes(aw.NodeType.SHAPE, True) :
                shape = shape.as_shape()

                if shape.name.find("WaterMark") >= 0 :
                    shape.remove()
                    
                
    #ExEnd:RemoveWatermark
    


if __name__ == '__main__':
    unittest.main()