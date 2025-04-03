Amazon Ads Analysis Platform
============================

Overview
--------

This project is a comprehensive analysis platform designed to assist with Amazon Ads data processing, CSV data analysis, PDF document querying, and code generation. It provides a user-friendly interface with multiple agents specialized in different tasks:

1.  **Amazon Ads Query Agent**: Provides expertise on Amazon advertising strategies, campaign optimization, and bid management
    
2.  **Seller Query Agent**: Analyzes CSV data, performs filtering, and generates insights from seller data
    
3.  **PDF Query Agent**: Extracts and answers questions about information contained in uploaded PDF documents
    
4.  **Code Generation Agent**: Creates code snippets based on user requirements
    

The application is built with Panel for the user interface and leverages LangChain with the Groq API for natural language processing capabilities.

System Architecture
-------------------

### Components

*   **User Interface**: Built with Panel, providing intuitive chat interfaces and file upload capabilities
    
*   **Database**: SQLite database for conversation memory and caching of responses
    
*   **Agents**:
    
    *   GeneralAgent (Amazon Ads expertise)
        
    *   SellerAgent (CSV data analysis)
        
    *   PDFQueryAgent (PDF document querying)
        
    *   DHI\_CodeBot (Code generation)
        
*   **Vector Store**: Chroma DB for document embeddings and similarity search
    
*   **LLM Integration**: Uses Groq's LLama-3.3-70B-Versatile model for natural language processing
    

### Data Flow

1.  User selects the desired agent mode using the UI buttons
    
2.  For data analysis, user uploads relevant files (CSV/PDF)
    
3.  User submits queries via the chat interface
    
4.  The system routes the query to the appropriate agent
    
5.  The agent processes the query and returns results
    
6.  Results are stored in the conversation memory database for future reference
    

Features
--------

### Amazon Ads Expertise

*   General queries about Amazon advertising strategies
    
*   Campaign optimization advice
    
*   Bid management guidance
    

### CSV Data Analysis

*   Uploads CSV files with seller data
    
*   Processes natural language queries about the data
    
*   Performs filtering, sorting, and aggregation operations
    
*   Generates downloadable filtered datasets
    
*   Provides statistical insights and data visualizations
    

### PDF Document Querying

*   Uploads PDF documents
    
*   Creates vector embeddings of document content
    
*   Answers specific questions about document contents
    
*   Retrieves relevant information from documents
    

### Code Generation

*   Creates code snippets based on user requirements
    
*   Uses specialized CodeGPTPlus agent for code generation
    

### Conversation Memory

*   Caches previous queries and responses
    
*   Improves response time for repeated queries
    
*   Maintains conversation history
    

Technical Details
-----------------

### Dependencies

*   Panel: For building the interactive web interface
    
*   LangChain: For creating and managing language model chains
    
*   SQLAlchemy: For database operations and ORM
    
*   HuggingFace Embeddings: For document vectorization
    
*   Chroma: Vector database for document storage and retrieval
    
*   Groq API: For accessing the Llama-3.3-70B model
    
*   Pandas: For data manipulation and analysis
    
*   CodeGPT: For code generation capabilities
    

### Database Schema

The application uses a simple SQLite database with a single table:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   conversations  - id (Integer, Primary Key)  - query (String, Indexed)  - result (Text)  - filename (String, Indexed)   `

This table stores previous queries and their responses for faster retrieval.

### File Management

*   Uploaded files are stored in an uploads directory
    
*   Filtered CSV data can be exported and downloaded
    
*   Vector embeddings are persisted in a chroma\_db directory
    

Installation and Setup
----------------------

### Prerequisites

*   Python 3.7+
    
*   Panel
    
*   LangChain
    
*   SQLAlchemy
    
*   HuggingFace Transformers
    
*   Groq API access
    
*   CodeGPT Plus access
    

### Environment Variables

Create a .env file with:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   GROQ_API_KEY=your_groq_api_key  CODEGPT_API_KEY=your_codegpt_api_key   `

### Installation Steps

1.  Clone the repository
    
2.  Install required packages: pip install -r requirements.txt
    
3.  Set up environment variables in .env
    
4.  Run the application: panel serve main.py
    

Usage Guide
-----------

1.  Open the application in a web browser
    
2.  Select the desired mode:
    
    *   **Amazon Ads Queries**: For general Amazon advertising questions
        
    *   **Seller Queries**: For CSV data analysis (requires CSV upload)
        
    *   **PDF Queries**: For document Q&A (requires PDF upload)
        
    *   **Code Generation**: For generating code snippets
        
3.  If needed, upload relevant files
    
4.  Type queries in the chat interface
    
5.  For filtered data, use the download button to export results
    

### Example Queries

#### Amazon Ads Queries

*   "What are the best strategies for optimizing PPC campaigns?"
    
*   "How can I improve my ACoS on Amazon?"
    

#### Seller Queries

*   "Show me sales data for January"
    
*   "List products with more than 100 units sold"
    
*   "What's the average profit margin across all products?"
    

#### PDF Queries

*   "What does the document say about return policies?"
    
*   "Summarize the main points in section 3"
    

#### Code Generation

*   "Write a Python function to analyze keyword performance"
    
*   "Create a script to calculate profit margins from Amazon seller reports"
    

Future Improvements
-------------------

*   Add multi-user support with authentication
    
*   Implement more visualization options for data analysis
    
*   Add support for additional file formats
    
*   Improve conversation context management
    
*   Add export functionality for conversation history