# from langchain_groq import ChatGroq
# from langchain_community.document_loaders import WebBaseLoader
# import chromadb
# from langchain_core.prompts import PromptTemplate

# llm = ChatGroq(
#     model="llama-3.1-70b-versatile",
#     temperature=0.0,
#     max_retries=2,
#     groq_api_key="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"
#     # other params...
# )

# response = llm.invoke("capital of nepal")
# print(response.content)


# chroma_client = chromadb.Client()
# collection = chroma_client.create_collection(name="my_collection")



# loader = WebBaseLoader("https://jobs.nike.com/job/R-43519?from=job%20search%20funnel")

# page_data=loader.load().pop().page_content
# print(page_data)



# # Instantiation using from_template (recommended)
# prompt_extract = PromptTemplate.from_template("""
#             ###scraped data from the website:
#             {page_data}
#             ###INSTRUCTION:
#             The scraped text is from the career's page of a website:
#             Your job is to extract the job postings and return them in JSON format containing the following keys:  `role`, `experience`, `skills` and `description`.
#             Only return the valid JSON with no preamble.
#             ### VALID JSON (NO PREAMBLE):
#             """

# )
# chain_extract = prompt_extract | llm

# res = chain_extract.invoke(input={'page_data': page_data})
# print(res.content)




import streamlit as st
from chain import chain
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader






def create_streamlit_app(llm, clean_text):
    st.title("Cold email generator")
    url_input = st.text_input("Enter the URL of the job posting")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader(url_input)

            data=clean_text(loader.load().pop().page_content)

            jobs = llm.extract_jobs  (data)
            email = llm.write_mail(jobs)
            st.code(email)
        except Exception as e:
            st.error(f"An error occured: {e}")



if __name__ == "__main__":
    chain = chain()
    st.set_page_config(layout="wide", page_title="Cold email generator", )
    create_streamlit_app(chain, clean_text)
