
from rdflib import Graph
from dotenv import load_dotenv
from openai import OpenAI
import logging
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SPARQLQueryGenerator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        
    def _prepare_prompt(self, question: str, ontology_serialization: str) -> str:
        """Prepare the prompt for OpenAI."""
        return f"""
        The following is an ontology graph with classes and properties:
        
        {ontology_serialization}
        
        Using this ontology, convert the following natural language question to a SPARQL query:
        
        Question: "{question}"
        
        Return only the SPARQL query without any additional text or markdown formatting.
        """
    
    def generate_sparql_query(self, question: str, schema_graph: Graph) -> str:
        """Generate a SPARQL query from a natural language question."""
        try:
            # Serialize the ontology schema
            ontology_serialization = schema_graph.serialize(format='turtle')
            
            # Prepare the prompt
            prompt = self._prepare_prompt(question, ontology_serialization)
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for generating SPARQL queries. Return only the SPARQL query without any additional text or markdown formatting."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            
            # Extract and clean the query
            query = response.choices[0].message.content.strip()
            cleaned_query = query.replace("```sparql", "").replace("```", "").strip()
            
            logger.info("Successfully generated SPARQL query")
            return cleaned_query
            
        except Exception as e:
            logger.error(f"Error generating SPARQL query: {str(e)}")
            raise ValueError(f"Failed to generate SPARQL query: {str(e)}")

    def format_results_with_llm(self, results: list, query: str) -> str:
        """Format SPARQL query results using OpenAI."""
        try:
            # Prepare prompt for LLM
            prompt = f"""
            The following SPARQL query was executed:
            
            {query}
            
            The query results are:
            {results}
            
            Please format these results into a human-readable explanation.
            """
            
            # Get formatted response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Your task is to format query results into a simple tabular form and convert uri form to word"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            formatted_response = response.choices[0].message.content.strip()
            logger.info("Successfully formatted results with LLM")
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error formatting results with LLM: {str(e)}")
            raise ValueError(f"Failed to format results: {str(e)}")

    def execute_query(self, query: str, data_graph: Graph) -> Tuple[bool, Optional[str]]:
        """Execute a SPARQL query, process results with LLM, and return the explanation."""
        try:
            # Execute query on the data graph
            results = list(data_graph.query(query))
            logger.info(f"Successfully executed query. Found {len(results)} results.")
            
            # Format results with LLM
            explanation = self.format_results_with_llm(results, query)
            return True, explanation
            
        except Exception as e:
            logger.error(f"Error executing SPARQL query: {str(e)}")
            return False, None

