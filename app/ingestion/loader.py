#take a PDF file path and return its text content, page by page.

from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_path : str):
    """
    Loads a PDF and returns a list of LangChain Document objects.
    Each Document = one page, with metadata like page number and source file.
    """
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return documents