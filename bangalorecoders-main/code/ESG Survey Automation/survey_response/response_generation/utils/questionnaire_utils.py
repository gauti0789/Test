import asyncio
import io
import re
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from ..utils import (
  get_answer_from_pdf
)
import textwrap  

async def get_answer_async( question, is_citation):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, get_answer_from_pdf.answer,question['question'], is_citation)
    
async def read_questions_from_pdf(input_pdf_file):

    if input_pdf_file.size == 0:
        raise ValueError("Uploaded PDF file is empty")

    existing_pdf = PdfReader(input_pdf_file)
    questions = []
    question_pattern = re.compile(r"^\((C|F|S)[a-zA-Z0-9.-]+\)")

    for page in existing_pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        in_question = False
        
        for line in lines:
            if re.match(question_pattern, line.strip()):
                in_question = True
                questions.append(line.strip())
            elif in_question:
                questions[-1] += "\n" + line.strip()
                    
    return questions


async def generate_pdf_with_answers(input_pdf_path, output_pdf_path):
    questions = await read_questions_from_pdf(input_pdf_path)
    output = PdfWriter()

    # Get answers for each question
    for question in questions:
        # Call the asynchronous function to get the answer
        response_after_calling_GPT, citations, accuracy, confidence_scores = await get_answer_async({'question': question}, True)
        answer, _, _ = response_after_calling_GPT
        
        # Split answer into lines with word wrapping
        answer_lines = textwrap.wrap(answer, width=100)  # Adjust the width as needed
        
        # Write question and answer
        with io.BytesIO() as packet:
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFillColorRGB(136/255, 36/255, 108/255)  # Set RGB color for questions
            
            # Write question
            lines = question.split('\n')
            for i, line in enumerate(lines):
                y_position = 700 - i * 20
                can.drawString(10, y_position, line)
            
            # Set color back to black for writing answers
            can.setFillColorRGB(0, 0, 0)
            
            # Write answer
            for i, line in enumerate(answer_lines):
                y_position = 700 - (len(lines) + i + 1) * 20
                can.drawString(10, y_position, line)
            
            can.save()
            packet.seek(0)

            new_pdf = PdfReader(packet)
            output.add_page(new_pdf.pages[0])

    # Write the output PDF to file
    with open(output_pdf_path, "wb") as output_stream:
        output.write(output_stream)

