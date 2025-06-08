import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class SentenceTransformerEmbeddings:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def embed_query(self, text: str):
        # Use the encode method of SentenceTransformer
        return self.model.encode(text).tolist()


class ChatbotComponent:
    def __init__(self, open_api_key, pinecone_api, csv_file=None, data_dict=None):
        self.open_api_key = open_api_key
        self.pinecone_api = pinecone_api
        self.qa_chain = self._initialize_rag(csv_file, data_dict)

    def _process_data_dict(self, data_dict):
        df = pd.read_csv(data_dict)
        return [Document(page_content=str(row)) for row in df.astype(str).values.tolist()]

    def _initialize_rag(self, csv_file, data_dict):
        # Initialize documents
        documents = []
        if data_dict:
            documents = self._process_data_dict(data_dict)
        elif csv_file:
            df = pd.read_csv(csv_file)
            documents = [Document(page_content=str(row)) for row in df.astype(str).values.tolist()]

        # Split documents
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = text_splitter.split_documents(documents)

        # Initialize SentenceTransformer embeddings
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # Set the API key as an environment variable
        os.environ["PINECONE_API_KEY"] = self.pinecone_api
        environment = "us-east1-gcp"  # Replace with your environment

        # Initialize Pinecone connection
        pinecone = Pinecone(environment=environment)

        # Create PineconeVectorStore instance
        docsearch = PineconeVectorStore.from_existing_index(
            index_name="heart-deistes",
            embedding=embeddings,
            # pinecone_client=pinecone  # Pass the Pinecone instance
        )

        # Initialize OpenAI model
        llm = ChatOpenAI(model_name="gpt-4", temperature=0, api_key=self.open_api_key)

        # Define the system prompt
        system_prompt = (
            """You are a specialized  data analyst focusing on heart disease statistics and trends. Follow these guidelines strictly:

DATA INTERPRETATION:
- Base all answers exclusively on the provided context data
- Round all numerical values to 3 decimal places
- Present statistics in a clear, organized manner
- If analyzing trends, mention the specific time period or geographic scope from the context
- Note that all rates are per 100,000

RESPONSE STRUCTURE:
- Begin responses with the key findings or direct answer to the query
- Support claims with specific numbers from the context
- When comparing groups or regions, use clear comparative language
- For complex queries, break down the analysis into logical segments

ACCURACY AND LIMITATIONS:
- If the context doesn't contain sufficient information to answer fully, explicitly state this
- Do not make assumptions beyond the provided data
- If asked about causation, only state correlations present in the data
- Flag any potential data limitations or caveats mentioned in the context

MEDICAL CONTEXT:
- Use proper medical terminology when present in the context
- Explain medical terms if they appear in technical form
- Maintain clinical accuracy while being accessible to non-medical readers
- Highlight any critical health indicators or risk factors present in the data

STATISTICAL REPORTING:
- Present percentages alongside absolute numbers when available
- Include sample sizes when relevant
- Clearly state any demographic breakdowns
- Note any significant correlations or patterns in the data

PROHIBITED:
- Do not make medical recommendations or provide medical advice
- Do not extrapolate beyond the provided data
- Do not combine information from outside knowledge
- Do not speculate about causation unless explicitly stated in the context

Context: {context}

Remember: Your role is to analyze and present the data accurately, not to provide medical advice or draw conclusions beyond the provided context."""


        )

        # Create a ChatPromptTemplate with the system and human messages
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        # Create the RetrievalQA chain with the prompt
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=docsearch.as_retriever(),
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},  # Pass the ChatPromptTemplate here
        )

        return qa_chain

    def ask_question(self, query):
        return self.qa_chain.run(query)

    def create_layout(self):
        return html.Div(
            [
                html.Button(
                    "💬 Chat",
                    id="chat-button",
                    n_clicks=0,
                    style={
                        "position": "fixed",
                        "bottom": "20px",
                        "right": "20px",
                        "background": "#007bff",
                        "color": "white",
                        "border": "none",
                        "padding": "10px 15px",
                        "border-radius": "20px",
                        "cursor": "pointer",
                    },
                ),
                html.Div(
                    id="chat-container",
                    children=[
                        html.Div(
                            [
                                html.Img(
                                    src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
                                    style={"width": "50px", "border-radius": "50%"},
                                ),
                                html.Span(
                                    "Heart Disease",
                                    style={"font-weight": "bold", "margin-left": "10px"},
                                ),
                                html.Span(
                                    "🟢 Online", style={"color": "green", "margin-left": "10px"}
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                                "margin-bottom": "10px",
                            },
                        ),
                        html.Div(
                            id="chat-history",
                            children=[],
                            style={
                                "border": "1px solid #ccc",
                                "padding": "10px",
                                "height": "300px",
                                "overflowY": "scroll",
                                "background": "#f9f9f9",
                                "border-radius": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="user-input",
                                    type="text",
                                    placeholder="Enter your message...",
                                    style={
                                        "flex": "1",
                                        "padding": "10px",
                                        "border": "1px solid #ccc",
                                        "border-radius": "5px",
                                    },
                                ),
                                html.Button(
                                    "➤",
                                    id="send-button",
                                    n_clicks=0,
                                    style={
                                        "background": "#007bff",
                                        "color": "white",
                                        "border": "none",
                                        "padding": "10px 15px",
                                        "border-radius": "5px",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                            style={"display": "flex", "margin-top": "10px"},
                        ),
                    ],
                    style={
                        "display": "none",
                        "position": "fixed",
                        "bottom": "70px",
                        "right": "20px",
                        "width": "400px",
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "border-radius": "10px",
                        "box-shadow": "0px 0px 10px rgba(0,0,0,0.1)",
                        "background": "white",
                    },
                ),
            ],
            style={"position": "relative"},
        )

    def register_callbacks(self, app):
        @app.callback(
            Output("chat-container", "style"),
            Input("chat-button", "n_clicks"),
            State("chat-container", "style"),
        )
        def toggle_chatbot(n_clicks, current_style):
            if n_clicks % 2 == 1:
                return {**current_style, "display": "block"}
            return {**current_style, "display": "none"}

        @app.callback(
            Output("chat-history", "children"),
            Input("send-button", "n_clicks"),
            State("user-input", "value"),
            State("chat-history", "children"),
            prevent_initial_call=True,
        )
        def update_chat(n_clicks, user_message, chat_history):
            if not user_message:
                return chat_history if chat_history else []

            chatbot_response = self.ask_question(user_message)

            new_chat = html.Div(
                [
                    html.Div(
                        f"You: {user_message}",
                        style={
                            "background": "#007bff",
                            "color": "white",
                            "padding": "10px",
                            "border-radius": "10px",
                            "margin": "5px 0",
                        },
                    ),
                    html.Div(
                        f"Response: {chatbot_response}",
                        style={
                            "background": "#e9ecef",
                            "padding": "10px",
                            "border-radius": "10px",
                            "margin": "5px 0",
                        },
                    ),
                ]
            )

            return chat_history + [new_chat] if chat_history else [new_chat]
