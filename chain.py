import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
os.getenv("GROQ_API_KEY")



class chain:
    def __init__(self):
        # genai.configure(api_key=os.getenv("API_KEY"))
        # self.llm= ChatGroq(model="llama-3.1-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"), temperature=0.0, max_retries=2,)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("API_KEY"),
            temperature=0.0,
            max_retries=2
        )


    def extract_jobs(self, cleaned_text):
        # Define the prompt template for extracting job postings
        prompt_extract = PromptTemplate.from_template("""
            ###scraped data from the website:
            {page_data}
            ###INSTRUCTION:
            The scraped text is from the career's page of a website:
            Your job is to extract the job postings and return them in JSON format containing the following keys:  `role`, `experience`, `skills` and `description`.
            Only return the valid JSON with no preamble. In output I only want the json format without any preambles
            ### VALID JSON (NO PREAMBLE):
            """)
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Unable to parse job")
        return res if isinstance(res, list) else res


    def write_mail(self, job):
        prompt_extract = PromptTemplate.from_template("""
            ###Job description
            {json_res}
            ###INSTRUCTION:
            Your name is Mukesh, and you are working as software engineer at msg global solutions.
            Write a cold email to the hiring manager based on the above job description.
            Only write the cold email with no preamble.
            make sure I don't have to provide any modification in the email like company name or anything.
            make sure it doesn't look like it is AI generated.
            ### cold email (NO PREAMBLE):
            """)
        chain_extract = prompt_extract | self.llm
        cold_email = chain_extract.invoke(input={'json_res': job})
        return cold_email.content
