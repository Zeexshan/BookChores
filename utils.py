import fitz  # pymupdf
import google.generativeai as genai
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_file, page_number):
    """
    Takes the uploaded file object and page index.
    Returns the string text of that page.
    Handle errors if the page doesn't exist.
    """
    try:
        # Use getvalue() to get bytes from Streamlit UploadedFile
        doc = fitz.open(stream=pdf_file.getvalue(), filetype="pdf")
        
        if page_number < 0 or page_number >= len(doc):
            return "Error: Page number out of range."
            
        page = doc.load_page(page_number)
        text = page.get_text()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def generate_image_prompt(page_text, api_key):
    """
    Connects to google.generativeai. Configures the model gemini-1.5-flash.
    Sends the page_text with a system instruction.
    Returns the generated prompt string.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        system_instruction = (
            "You are an artistic director. Read this book page and describe the main visual scene "
            "in a vivid, detailed, cinematic image prompt (max 40 words). "
            "Do not include character names, just visual descriptions."
        )
        
        full_prompt = f"{system_instruction}\n\nBook Page Text:\n{page_text}"
        
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating prompt: {str(e)}"

def get_pollinations_url(prompt):
    """
    Takes the prompt string and returns a URL for Pollinations.ai.
    The format must be: https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true
    Ensure the prompt is URL-encoded.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
