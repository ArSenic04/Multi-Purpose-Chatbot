import os
import re
import uuid
import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent

from database.models import session, Conversation
from utils.helpers import ensure_uploads_dir

class SellerAgent:
    def __init__(self, csv_path: str = None):
        if csv_path:
            self.df = pd.read_csv(csv_path)
            self.csv_path = csv_path
        else:
            self.df = None
            self.csv_path = None
        self.llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
        
        # Enhanced prefix with clearer instructions for formatting
        self.prefix = """
        You are a helpful data analysis assistant. Your task is to analyze the provided CSV data carefully.
        
        Follow these guidelines when answering:
        1. Always check if a query involves filtering, sorting, or aggregating data
        2. If the query involves filtering by a specific value or term, create a filtered dataframe and save it
        3. Provide clear, concise answers with relevant statistics
        4. For "list" or "show" queries, return actual data, not just summaries
        5. Always look for exact matches when filtering by keywords
        6. Show the first 10 rows of results for listing queries, with a total count
        
        IMPORTANT: Always follow this exact format:
        Thought: <your reasoning>
        Action: python_repl_ast
        Action Input: <your Python code>
        
        After you get observation results, continue with:
        Thought: <your interpretation of results>
        Action: python_repl_ast
        Action Input: <any follow-up code>
        
        Finally:
        Thought: <your final reasoning>
        Answer: <your final answer>
        
        Remember to execute the correct pandas operations and evaluate your results before responding.
        """
        
        self.agent = create_pandas_dataframe_agent(
            llm=self.llm,
            df=self.df if self.df is not None else pd.DataFrame(),
            verbose=True,
            handle_parsing_errors=True,
            allow_dangerous_code=True,
            prefix=self.prefix
        )

    def query(self, question: str) -> str:
        from ui.components import update_layout_with_download_button
        
        if self.df is None or self.df.empty:
            return "❌ Please upload a valid CSV file before querying."
        try:
            existing = session.query(Conversation).filter_by(query=question).first()
            if existing:
                return f"🧠 (From memory) {existing.result}"
            
            # Check if the query involves filtering
            filter_keywords = ["filter", "where", "find", "list", "show", "contain", "match", "include"]
            is_filter_query = any(keyword in question.lower() for keyword in filter_keywords)
            
            # Generate a UUID-based filename for filtered data
            export_filename = f"filtered_data_{uuid.uuid4().hex[:8]}.csv"
            filtered_csv_path = os.path.join("uploads", export_filename)
            
            # Add a specialized instruction for the agent to return the filtered data
            if is_filter_query:
                custom_question = f"""
                {question}
                
                After executing this query, if you've filtered the data in any way, show the first few rows of your filtered result and the total number of rows.
                Also, in your Python code, assign your filtered dataframe to the variable '_FILTERED_RESULT_' so I can extract it.
                """
                
                try:
                    response = self.agent.run(custom_question)
                except Exception as parse_error:
                    # Handle parsing errors by extracting useful information
                    error_message = str(parse_error)
                    match = re.search(r'Could not parse LLM output: `(.*)`', error_message, re.DOTALL)
                    if match:
                        # Return the raw output from the LLM without parsing
                        raw_output = match.group(1)
                        response = f"I analyzed your request: {raw_output}\n\nHere's a summary of what I found in your data."
                    else:
                        # If we can't extract the output, run a simpler query
                        simple_question = f"Please analyze this data: {question}"
                        response = self.agent.run(simple_question)
                
                # Extract the filtered dataframe result from the agent's response
                filtered_df = self._extract_filtered_dataframe(response)
            else:
                try:
                    response = self.agent.run(question)
                except Exception as parse_error:
                    # Handle parsing errors by extracting useful information
                    error_message = str(parse_error)
                    match = re.search(r'Could not parse LLM output: `(.*)`', error_message, re.DOTALL)
                    if match:
                        # Return the raw output from the LLM without parsing
                        raw_output = match.group(1)
                        response = f"I analyzed your request and found: {raw_output}"
                    else:
                        # Return a simplified error message
                        response = f"❌ I had trouble parsing the analysis results. Please try rephrasing your question. Error details: {str(parse_error)[:100]}..."
                filtered_df = None
            
            # Create and save the filtered dataframe if it exists
            if filtered_df is not None and not filtered_df.empty:
                # Ensure uploads directory exists
                ensure_uploads_dir()
                
                # Save the filtered dataframe to CSV
                filtered_df.to_csv(filtered_csv_path, index=False)
                
                # Update the UI with a download button
                update_layout_with_download_button(filtered_csv_path, len(filtered_df))
                
                # Enhance the response
                response += f"\n\n✅ Filtered data is ready for download! Found {len(filtered_df)} matching rows."
            
            session.add(Conversation(query=question, result=response, filename=self.csv_path))
            session.commit()
            return response
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in SellerAgent.query: {error_details}")
            return f"❌ Error processing query: {str(e)}"
    
    def _extract_filtered_dataframe(self, response):
        """Extract filtered dataframe from the agent's response"""
        # Try to extract from code blocks
        code_blocks = re.findall(r'```python(.*?)```', response, re.DOTALL)
        if not code_blocks:
            # Try alternate code block format if the first regex doesn't match
            code_blocks = re.findall(r'```(.*?)```', response, re.DOTALL)
        
        filtered_df = None
        # Execute each code block to get the filtered dataframe
        for code_block in code_blocks:
            # Clean up the code block and check for the filtered result variable
            code = code_block.strip()
            if "_FILTERED_RESULT_" in code:
                # Create a local namespace to execute the code
                local_vars = {"df": self.df.copy(), "_FILTERED_RESULT_": None, "pd": pd}
                try:
                    # Execute the code to get the filtered dataframe
                    exec(code, globals(), local_vars)
                    if local_vars["_FILTERED_RESULT_"] is not None and isinstance(local_vars["_FILTERED_RESULT_"], pd.DataFrame):
                        filtered_df = local_vars["_FILTERED_RESULT_"]
                except Exception as exec_error:
                    print(f"Error executing code block: {exec_error}")
        
        # If we couldn't extract the filtered dataframe from code blocks, try to parse the result for keyword filtering
        if filtered_df is None:
            filtered_df = self._try_alternative_extraction(response)
            
        return filtered_df
    
    def _try_alternative_extraction(self, response):
        """Try alternative methods to extract a filtered dataframe"""
        try:
            # Look for patterns like "df[df['column'] == 'value']"
            filter_patterns = re.findall(r"df\[(.*?)\]", response, re.DOTALL)
            if filter_patterns:
                for pattern in filter_patterns:
                    try:
                        # Create a safe execution environment
                        local_vars = {"df": self.df.copy(), "pd": pd, "re": re, "np": pd.np}
                        # Try to execute the filter
                        exec(f"_FILTERED_RESULT_ = df[{pattern}]", globals(), local_vars)
                        if "_FILTERED_RESULT_" in local_vars and isinstance(local_vars["_FILTERED_RESULT_"], pd.DataFrame):
                            return local_vars["_FILTERED_RESULT_"]
                    except Exception:
                        continue
        except Exception as extract_error:
            print(f"Error extracting filter conditions: {extract_error}")
        
        # Try keyword-based filtering as a last resort
        return self._try_keyword_filtering(response)
    
    def _try_keyword_filtering(self, response):
        """Try keyword-based filtering from the query"""
        question = response  # In this context, we just use the response text
        search_terms = []
        for keyword in ["contain", "filter", "where", "find", "match"]:
            if keyword in question.lower():
                # Extract the term after the keyword
                match = re.search(f"{keyword}\\s+(.+?)(?:\\s|$)", question.lower())
                if match:
                    search_terms.append(match.group(1).strip('"\'.,;:'))
        
        # Apply filtering based on extracted search terms
        if search_terms:
            string_cols = self.df.select_dtypes(include=['object']).columns
            filter_condition = pd.Series([False] * len(self.df))
            
            for term in search_terms:
                for col in string_cols:
                    filter_condition = filter_condition | self.df[col].astype(str).str.contains(term, case=False, na=False)
            
            return self.df[filter_condition].copy()
        
        return None