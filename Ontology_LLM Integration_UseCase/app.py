import streamlit as st
from rdflib import Graph
from utils.query_generator import SPARQLQueryGenerator  # Import your class from the existing script

# Initialize the generator
generator = SPARQLQueryGenerator()

# Streamlit app
st.title("Chat with BIM Model")
st.write("Generate SPARQL queries from natural language and execute them against ontology data.")

# File uploaders for ontology files
schema_file = st.file_uploader("Upload Ontology Schema File (.ttl format):", type=["ttl"])
data_file = st.file_uploader("Upload Data Ontology File (.ttl format):", type=["ttl"])

if schema_file and data_file:
    try:
        # Load schema ontology
        schema_graph = Graph()
        schema_graph.parse(schema_file, format="turtle")
        st.success("Successfully loaded schema ontology.")

        # Load data ontology
        data_graph = Graph()
        data_graph.parse(data_file, format="turtle")
        st.success("Successfully loaded data ontology.")
    except Exception as e:
        st.error(f"Error parsing uploaded files: {str(e)}")
        st.stop()

    # User Input for Natural Language Question
    question = st.text_input("Enter your natural language question:")

    # Submit Button
    if st.button("Generate and Execute Query"):
        if question.strip():
            with st.spinner("Generating SPARQL query..."):
                try:
                    # Generate SPARQL query
                    sparql_query = generator.generate_sparql_query(question, schema_graph)
                    st.success("SPARQL Query Generated:")
                    st.code(sparql_query, language="sparql")

                    # Execute Query
                    with st.spinner("Executing SPARQL query..."):
                        success, explanation = generator.execute_query(sparql_query, data_graph)

                    if success and explanation:
                        st.success("Query Results Explanation:")
                        st.write(explanation)
                    else:
                        st.warning("No results found or query execution failed.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a valid question!")
else:
    st.info("Please upload both schema and data ontology files to proceed.")

# Footer
st.markdown("---")

