import streamlit as st
from src.processor import process_pdf
from src.llm_logic import generate_quiz
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
load_dotenv()
submitted=False
st.set_page_config(page_title="Grade 10 Study Assistant", layout="wide")
st.title("📚 Grade 10 Study Assistant")

# --- 1. Sidebar for File Uploads ---
with st.sidebar:
    st.header("Setup")
    uploaded_file = st.file_uploader("Upload Textbook (PDF)", type="pdf")
    # NEW: Dropdown instead of a slider
    # we use [1, 5, 10] as the options
    num_q = st.selectbox(
        "How many questions would you like?",
        options=[1, 5, 10],
        index=1  # This makes '5' the default starting choice
    )
    if uploaded_file:
        # Save and process only if not already processed
        if "retriever" not in st.session_state:
            with st.spinner("Processing textbook... please wait."):
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state.retriever = process_pdf("temp.pdf")
            st.success("Textbook Processed!")

# --- 2. Main Area: Quiz Generation ---
topic = st.text_input("Enter a topic (e.g., 'Metals and Non-metals')")


# Logic to generate and STORE the quiz so it doesn't disappear
if st.button("Generate Quiz"):
    if "retriever" in st.session_state:
        with st.spinner("Generating quiz..."):
            # Store the quiz data in session_state so it persists across reruns
            st.session_state.current_quiz = generate_quiz(st.session_state.retriever, topic,num_questions=num_q )
            # Reset answers if a new quiz is generated
            st.session_state.user_answers = {} 
    else:
        st.error("Please upload a PDF first!")

# --- 3. Display the Quiz (If it exists in state) ---
if "current_quiz" in st.session_state:
    st.divider()
    st.header(f"Quiz: {topic}")
    
    # Use a form to prevent the app from refreshing after every single click
    with st.form("quiz_form"):
        for i, q in enumerate(st.session_state.current_quiz.questions):
            st.write(f"**Q{i+1}: {q.question}**")
            
            # Use index=None so no option is pre-selected
            user_choice = st.radio(
                f"Select your answer for Q{i+1}:", 
                q.options, 
                key=f"radio_{i}",
                index=None 
            )
            st.session_state.user_answers[i] = user_choice
            st.write("---")
        
        # This button stays inside the form
        submitted = st.form_submit_button("Check All Answers")

    # --- 4. Scoring Logic ---
if submitted:
    score = 0
    st.write("### Results")
    for i, q in enumerate(st.session_state.current_quiz.questions):
        user_ans = st.session_state.user_answers.get(i)
            
        if user_ans:
                        
            # Find the full text of the correct option
            correct_option_text = ""
            for opt in q.options:
                if opt.startswith(q.answer):
                    correct_option_text = opt
                    break
            
            if user_ans == correct_option_text:
                st.success(f"**Q{i+1}: Correct!** 🎉")
                score += 1
            else:
                st.error(f"**Q{i+1}: Incorrect.**")
                st.write(f"Your answer: {user_ans}")
                st.write(f"Correct answer: {correct_option_text}")
        else:
            st.warning(f"**Q{i+1}: No answer selected.**")
    
    st.metric("Final Score", f"{score}/{len(st.session_state.current_quiz.questions)}")
# 2. Update the Chat Section at the bottom of app.py
st.divider()
st.header("💬 Chat with your Textbook")
user_question = st.text_input("Ask a specific question about the book:")

if user_question and "retriever" in st.session_state:
    with st.spinner("Searching textbook..."):
        # Setup the LLM
        llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo", 
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )

        # Define the prompt for answering questions
        
        prompt = ChatPromptTemplate.from_template(
            "Use the context below to answer the question.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "If you don't know the answer, say you don't know."
        )
       
        #   LCEL RAG PIPELINE
        rag_chain = (
            {
                "context": st.session_state.retriever,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        # Get the response
        # response = rag_chain.invoke({"input": user_question})
         # Run
        response = rag_chain.invoke(user_question)

        st.write("**Answer:**", response)
        # st.write("**Answer:**", response["answer"])
