import os
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

# 1. Define the exact structure we want the LLM to extract (Reproducibility)
class ResearchPipeline(BaseModel):
    data_ingestion: str = Field(description="Steps required to ingest and clean the data")
    transformation: str = Field(description="Data normalization and feature engineering steps")
    modeling: str = Field(description="The specific statistical or ML models to be trained")
    validation: str = Field(description="How the model will be evaluated")

def parse_research_to_pipeline(filepath: str) -> ResearchPipeline:
    """
    Takes a vague research methodology and uses an LLM agent to extract 
    a highly structured, reproducible data engineering pipeline.
    """
    print(f"Reading unstructured research methodology from {filepath}...\n")
    with open(filepath, 'r') as file:
        text = file.read()

    # Initialize the LLM (Using a lightweight model for the PoW)
    llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")
    parser = PydanticOutputParser(pydantic_object=ResearchPipeline)

    # The Agentic Prompt: Turning vague text into a strict Data Science scope
    prompt = PromptTemplate(
        template="You are a senior Data Scientist helping a university researcher. "
                 "Extract the reproducible data pipeline steps from the following text.\n"
                 "{format_instructions}\n\nResearch Text: {research_text}",
        input_variables=["research_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    print("Agent is structuring the research into a reproducible workflow...\n")
    chain = prompt | llm | parser
    structured_pipeline = chain.invoke({"research_text": text})
    
    return structured_pipeline

if __name__ == "__main__":
    # Simulate a DSI intake meeting with a Principal Investigator
    pipeline = parse_research_to_pipeline("sample_methodology.txt")
    
    print("✅ WORKFLOW SCOPE GENERATED:")
    print(f"1. Ingestion: {pipeline.data_ingestion}")
    print(f"2. Transformation: {pipeline.transformation}")
    print(f"3. Modeling: {pipeline.modeling}")
    print(f"4. Validation: {pipeline.validation}")
    
    print("\nNext Step: Generating starter Python script for the research team...")
    # In a full app, this would automatically generate the Python boilerplate.
