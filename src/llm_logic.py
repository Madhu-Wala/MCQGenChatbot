import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

class MCQ(BaseModel):
    question: str = Field(description="The question text")
    options: List[str] = Field(description="4 multiple choice options")
    answer: str = Field(description="The correct option (A, B, C, or D)")

class Quiz(BaseModel):
    questions: List[MCQ]

def generate_quiz(retriever, topic,num_questions=5):
    # Using OpenRouter with GPT-3.5 Turbo
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo", 
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7
    )
    
    parser = PydanticOutputParser(pydantic_object=Quiz)
    
    context_docs = retriever.invoke(topic)
    context_text = "\n".join([doc.page_content for doc in context_docs])
    
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert Grade 10 teacher.
        Using the context provided below, create exactly {num} multiple-choice questions 
        about the topic: {topic}.
        
        Context: {context}
        
        {format_instructions}
        """
    )
    
    chain = prompt | llm | parser
    return chain.invoke({
        "context": context_text, 
        "topic": topic,
        "num": num_questions,
        "format_instructions": parser.get_format_instructions()
    })