import streamlit as st
from pages.ontology_builder import OntologySession

def main():
    st.title("Streamlit Ontology Builder")
    session = OntologySession()

    st.subheader("Add New Class")
    parent = st.text_input("Parent Class Name", value="Thing")
    new_class = st.text_input("New Class Name", value="")
    if st.button("Create Class"):
        session.add_class(parent, new_class)
        st.success(f"Class '{new_class}' created under '{parent}'")

    st.subheader("Add Object Property")
    domain = st.text_input("Domain Class")
    range_ = st.text_input("Range Class")
    obj_prop = st.text_input("Object Property Name")
    if st.button("Create Object Property"):
        session.add_object_property(domain, range_, obj_prop)
        st.success(f"Object property '{obj_prop}' created")

    st.subheader("Add Data Property")
    dprop_domain = st.text_input("Domain Class (data)")
    dprop_name = st.text_input("Data Property Name")
    dprop_type = st.selectbox("Select Data Type", ["str", "int", "float", "bool"])
    if st.button("Create Data Property"):
        session.add_data_property(dprop_domain, dprop_name, dprop_type)
        st.success(f"Data property '{dprop_name}' created with range '{dprop_type}'")

    if st.button("Save Ontology"):
        session.save_ontology("streamlit_ontology.owl")
        st.success("Ontology saved as 'streamlit_ontology.owl'")

if __name__ == "__main__":
    main()
