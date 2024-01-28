from xml.etree import ElementTree as ET

# Parse the BPMN file and extract labels
# Updating the function to also consider activities, pools, lanes, and events in BPMN file
def extract_bpmn_labels_updated(bpmn_file_path):
    bpmn_tree = ET.parse(bpmn_file_path)
    bpmn_root = bpmn_tree.getroot()

    # Common tags for activities, pools, lanes, and events in BPMN files
    relevant_tags = ['task', 'userTask', 'serviceTask', 'sendTask', 'receiveTask',
                     'manualTask', 'businessRuleTask', 'scriptTask', 'callActivity',
                     'subProcess', 'transaction', 'event', 'startEvent', 'endEvent',
                     'intermediateThrowEvent', 'intermediateCatchEvent', 'boundaryEvent',
                     'pool', 'lane']

    labels = []
    for element in bpmn_root.iter():
        if any(tag in element.tag for tag in relevant_tags):
            # Extracting the name attribute which typically contains the label
            name = element.get('name')
            if name:
                labels.append(name)

    return labels

# Function to clean up extracted labels, removing irrelevant entries like whitespaces and line breaks
def clean_bpmn_labels(labels):
    cleaned_labels = labels
    return cleaned_labels

# Extracting labels again considering activities, pools, lanes, and events
updated_bpmn_labels = extract_bpmn_labels_updated('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/ParkinsonGo_Modell_V3.bpmn')
cleaned_updated_bpmn_labels = clean_bpmn_labels(updated_bpmn_labels)
cleaned_updated_bpmn_labels[:10000000]  # Displaying the cleaned labels for a preview


# Extracting labels from the BPMN file
bpmn_labels = extract_bpmn_labels_updated('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/ParkinsonGo_Modell_V3.bpmn')
bpmn_labels[:10000000]  # Displaying the first few labels for a preview



# Cleaning the BPMN labels
cleaned_bpmn_labels = clean_bpmn_labels(bpmn_labels)
cleaned_bpmn_labels[:10000000]  # Displaying the cleaned labels for a preview

# Updating the function to extract class and package names based on the observed file structure
def extract_uml_class_and_package_names_updated(uml_file_path):
    uml_tree = ET.parse(uml_file_path)
    uml_root = uml_tree.getroot()

    # Updated extraction logic based on the observed file structure
    classes = []
    packages = []

    for element in uml_root.iter():
        if element.get('{http://www.omg.org/spec/XMI/20131001}type') == 'uml:Class':
            classes.append(element.get('name'))
        elif element.get('{http://www.omg.org/spec/XMI/20131001}type') == 'uml:Package':
            packages.append(element.get('name'))

    return classes, packages

# Extracting class and package names from the UML file again with the updated logic
uml_classes_updated, uml_packages_updated = extract_uml_class_and_package_names_updated('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/DIGAPro1.uml')
(uml_classes_updated[:10000000], uml_packages_updated[:10000000])  # Displaying the first few for a preview


import difflib

# Function to check if a word in BPMN label matches at least 80% with any class name in UML
def check_similarity_and_update_label(label, uml_classes, uml_packages):
    words = label.split()
    updated_words = []

    for word in words:
        for uml_class in uml_classes:
            # Calculate similarity
            similarity = difflib.SequenceMatcher(None, word, uml_class).ratio()
            if similarity >= 0.8:  # 80% similarity
                # Find the package for the class
                for uml_package in uml_packages:
                    if uml_class in uml_package:  # Simplistic check for package
                        updated_word = f"{word}:: {uml_class} :: {uml_package}"
                        break
                else:
                    updated_word = f"{word}:: {uml_class}"
                break
        else:
            updated_word = word

        updated_words.append(updated_word)

    return ' '.join(updated_words)

# Update BPMN labels based on the similarity check
updated_bpmn_labels = [check_similarity_and_update_label(label, uml_classes_updated, uml_packages_updated) for label in cleaned_bpmn_labels]
updated_bpmn_labels[:10000]  # Displaying the updated labels for a preview

print(updated_bpmn_labels)


# Function to generate RDF triples from the updated BPMN labels
def generate_rdf_triples(bpmn_labels, uml_classes, uml_packages):
    rdf_triples = []

    for label in bpmn_labels:
        words = label.split('::')
        if len(words) > 1:
            # Extracting BPMN label, UML class, and UML package
            bpmn_label = words[0].strip()
            uml_class = words[1].strip()

            # Finding the corresponding package for the class
            uml_package = next((package for package in uml_packages if uml_class in package), None)

            # Creating RDF triple
            rdf_triple = (bpmn_label, "is type of", f"{uml_class} in {uml_package}")
            rdf_triples.append(rdf_triple)

    return rdf_triples

# Generating RDF triples
rdf_triples = generate_rdf_triples(updated_bpmn_labels, uml_classes_updated, uml_packages_updated)
rdf_triples[:10000000]  # Displaying the first few triples for a preview
print(rdf_triples)


# Updating the function to extract class and package names with proper association
def extract_uml_class_package_associations(uml_file_path):
    uml_tree = ET.parse(uml_file_path)
    uml_root = uml_tree.getroot()

    # Dictionary to hold class-package associations
    class_package_associations = {}

    # Iterating through the UML elements to find packages and classes
    for element in uml_root.iter():
        if element.get('{http://www.omg.org/spec/XMI/20131001}type') == 'uml:Package':
            package_name = element.get('name')
            # Finding all class elements within the package
            for class_element in element.findall('.//{*}Class'):
                class_name = class_element.get('name')
                class_package_associations[class_name] = package_name

    return class_package_associations

# Extracting class-package associations from the UML file
class_package_associations = extract_uml_class_package_associations('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/DIGAPro1.uml')

# Re-generating RDF triples with the correct package names
rdf_triples_corrected = []

for label in updated_bpmn_labels:
    words = label.split('::')
    if len(words) > 1:
        # Extracting BPMN label and UML class
        bpmn_label = words[0].strip()
        uml_class = words[1].strip()

        # Finding the corresponding package for the class
        uml_package = class_package_associations.get(uml_class, "Unknown")

        # Creating RDF triple
        rdf_triple = (bpmn_label, "is associated with", f"{uml_class} in {uml_package}")
        rdf_triples_corrected.append(rdf_triple)

rdf_triples_corrected[:10000000]  # Displaying the first few triples for a preview



import xml.etree.ElementTree as ET

# Funktion zum Extrahieren von Klassen-Paket-Zuordnungen aus der UML-Datei
def extract_uml_class_package_associations_corrected(uml_file_path):
    uml_tree = ET.parse(uml_file_path)
    uml_root = uml_tree.getroot()

    class_package_associations = {}
    class_parent_relations = {}

    # Zuordnung von Klassen zu Paketen und Erfassung der Vererbungsbeziehungen
    for element in uml_root.iter():
        if element.get('{http://www.omg.org/spec/XMI/20131001}type') == 'uml:Package':
            current_package = element.get('name')
            for child in element:
                if child.get('{http://www.omg.org/spec/XMI/20131001}type') == 'uml:Class':
                    class_name = child.get('name')
                    class_package_associations[class_name] = current_package
                for gen in child.iter('{http://www.eclipse.org/uml2/5.0.0/UML}generalization'):
                    subclass = child.get('name')
                    superclass = gen.get('general')  # Sie müssen die ID in einen Klassennamen umwandeln
                    class_parent_relations[subclass] = superclass

    # Funktion, um das Paket einer Klasse rekursiv zu finden
    def find_package(class_name):
        if class_name in class_package_associations:
            return class_package_associations[class_name]
        parent_class = class_parent_relations.get(class_name)
        if parent_class:
            return find_package(parent_class)
        return None

    # Aktualisieren der Klassen-Paket-Zuordnungen unter Berücksichtigung der Vererbung
    for class_name in class_parent_relations:
        if class_name not in class_package_associations:
            class_package_associations[class_name] = find_package(class_name)

    return class_package_associations

# Extrahieren der Klassen-Paket-Zuordnungen
class_package_associations_corrected = extract_uml_class_package_associations_corrected('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/DIGAPro1.uml')

# Funktion zum Generieren der RDF-Triples
def generate_rdf_triples(bpmn_labels, class_package_associations):
    rdf_triples = []

    for label in bpmn_labels:
        words = label.split('::')
        if len(words) > 1:
            bpmn_label = words[0].strip()
            uml_class = words[1].strip()
            uml_package = class_package_associations.get(uml_class, "Unknown")

            rdf_triple = (bpmn_label, "is associated with", f"{uml_class} in {uml_package}")
            rdf_triples.append(rdf_triple)

    return rdf_triples

# Generieren der RDF-Triples mit den korrekten Paketnamen
rdf_triples_with_correct_packages = generate_rdf_triples(updated_bpmn_labels, class_package_associations_corrected)


# Re-generating RDF triples with the correct package names using the corrected class-package associations
rdf_triples_with_correct_packages_v2 = []

for label in updated_bpmn_labels:
    words = label.split('::')
    if len(words) > 1:
        # Extracting BPMN label and UML class
        bpmn_label = words[0].strip()
        uml_class = words[1].strip()

        # Correctly finding the corresponding package for the class
        uml_package = class_package_associations_corrected.get(uml_class, "Unknown")

        # Creating RDF triple with the corrected package name
        rdf_triple = (bpmn_label, "is type of", f"{uml_class} in {uml_package}")
        rdf_triples_with_correct_packages_v2.append(rdf_triple)

rdf_triples_with_correct_packages_v2[:10000000]  # Displaying the first few triples for a preview


print(rdf_triples_with_correct_packages_v2)