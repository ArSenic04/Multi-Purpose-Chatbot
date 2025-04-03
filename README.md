Amazon Ads Analysis Platform
============================

An interactive multi-agent system for Amazon Ads analysis, data processing, document querying, and code generation.

🚀 Features
-----------

*   **Amazon Ads Expertise**: Get insights on advertising strategies, campaign optimization, and bid management
    
*   **CSV Data Analysis**: Upload seller data files for analysis, filtering, and statistical insights
    
*   **PDF Document Querying**: Extract information from documents using natural language queries
    
*   **Code Generation**: Create custom code snippets for specific tasks
    
*   **Conversation Memory**: System remembers previous queries for faster responses
    

📋 Prerequisites
----------------

*   Python 3.7+
    
*   Groq API key
    
*   CodeGPT Plus API key
    
*   Required Python packages (see requirements.txt)
    

🔧 Installation
---------------

1.  git clone https://github.com/yourusername/amazon-ads-analysis.gitcd amazon-ads-analysis
    
2.  pip install -r requirements.txt
    
3.  GROQ\_API\_KEY=your\_groq\_api\_keyCODEGPT\_API\_KEY=your\_codegpt\_api\_key
    
4.  panel serve main.py
    
5.  Open your browser and navigate to http://localhost:5006
    

💻 Usage
--------

1.  Select your desired mode from the main menu:
    
    *   **Amazon Ads Queries**: For general Amazon advertising questions
        
    *   **Seller Queries**: For CSV data analysis
        
    *   **PDF Queries**: For document Q&A
        
    *   **Code Generation**: For generating code snippets
        
2.  For data analysis, upload your CSV or PDF files when prompted
    
3.  Type your queries in the chat interface
    
4.  For filtered data results, use the download button to export
    

📊 Example Queries
------------------

### Amazon Ads Queries

*   "What strategies can improve my sponsored product performance?"
    
*   "How do I optimize my bidding strategy for new products?"
    

### Seller Queries

*   "Show top 10 products by revenue"
    
*   "Filter orders with more than 3 units sold"
    
*   "Calculate average profit margin by category"
    

### PDF Queries

*   "What are the key points in the introduction?"
    
*   "Summarize the methodology section"
    

### Code Generation

*   "Create a script to analyze keyword performance"
    
*   "Write a function to calculate profit after Amazon fees"
    

🧰 Technologies Used
--------------------

*   **Panel**: Interactive web interface
    
*   **LangChain**: LLM integration framework
    
*   **Groq API**: LLM provider (Llama-3.3-70B)
    
*   **SQLAlchemy**: Database ORM
    
*   **HuggingFace**: Embeddings for document vectorization
    
*   **Chroma**: Vector database for document retrieval
    
*   **Pandas**: Data analysis and manipulation
    
*   **CodeGPT Plus**: Code generation capabilities
    

📁 Project Structure
--------------------

*   main.py: Main application file
    
*   uploads/: Directory for uploaded files
    
*   chroma\_db/: Vector database storage
    
*   conversation\_memory.db: SQLite database for conversation history
    

🔄 Contributing
---------------

Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
----------

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgements
-------------------

*   [Panel]() for the interactive interface
    
*   [LangChain]() for the LLM integration
    
*   [Groq]() for the LLM API
    
*   [Chroma]() for the vector database
