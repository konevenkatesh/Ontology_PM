from owlready2 import get_ontology, Thing, DataProperty, ObjectProperty, FunctionalProperty
import types

class OntologySession:
    def __init__(self, base_iri="http://example.org/streamlit_onto#"):
        self.onto = get_ontology(base_iri)

    def add_class(self, parent_name, class_name):
        with self.onto:
            parent_cls = self.onto.search_one(iri="*"+parent_name)
            if not parent_cls:
                parent_cls = types.new_class(parent_name, (Thing,))
            return types.new_class(class_name, (parent_cls,))

    def add_object_property(self, domain_name, range_name, prop_name):
        with self.onto:
            domain_cls = self.onto.search_one(iri="*"+domain_name)
            range_cls = self.onto.search_one(iri="*"+range_name)
            prop = types.new_class(prop_name, (ObjectProperty, FunctionalProperty))
            if domain_cls and range_cls:
                prop.domain = [domain_cls]
                prop.range = [range_cls]

    def add_data_property(self, domain_name, prop_name, data_type="str"):
        with self.onto:
            domain_cls = self.onto.search_one(iri="*"+domain_name)
            prop = types.new_class(prop_name, (DataProperty, FunctionalProperty))
            if domain_cls:
                prop.domain = [domain_cls]
            prop.range = [eval(data_type)]

    def save_ontology(self, filename="streamlit_ontology.owl"):
        self.onto.save(file=filename)
