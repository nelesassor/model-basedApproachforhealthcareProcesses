from nltk.stem import WordNetLemmatizer
import xml.etree.ElementTree as ET
import nltk
from nltk.tokenize import word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Beispiel für Zuordnungstabellen basierend auf den extrahierten Daten
akteure_keywords = [
    'Actor', 'Person', 'Doctor', 'Patient', 'Pharmacist', 'Nurse', 'Therapist',
    'Psychotherapist', 'Relative', 'Patient Representative', 'General Practitioner', 'Emergency Doctor',
    'Licensed Health Professional', 'Specialist Doctor', 'Non-Licensed Health Professional', 'Geriatric Nurse',
    'Dietitian', 'Health and Nursing Assistant', 'Medical Assistant',
    'Emergency Paramedic', 'Diabetes Consultant', 'NäPaVERAH', 'Healthcare Provider', 'Physiotherapist',
    'Medical Professional', 'Healthcare Administrator', 'Medical Researcher', 'Health Informatician', 'Health Policy Maker', 'Social Worker', 'Healthcare Educator'
]

system_keywords = [
    'Medical Device Manufacturer', 'Digital Health Application Manufacturer', 'Implant Manufacturer', 'Laboratory',
    'Statutory Health Insurance', 'Nursing Care Insurance', 'Pension Insurance', 'Accident Insurance',
    'LEOrganization', 'Inpatient LEOrganization', 'Hospital', 'Inpatient Care', 'Inpatient Rehabilitation',
    'Outpatient LEOrganization', 'Emergency Clinic', 'Pharmacy', 'Emergency Service', 'Telemedical Center',
    'Emergency Medical Service', 'Outpatient Nursing Service', 'MVZ', 'Doctors Office', 'Local Pharmacy',
    'Online Pharmacy', 'Manufacturer', 'Sensor', 'Healthcare Information System', 'Electronic Health Record (EHR) System', 'Clinical Decision Support System', 'Patient Portal', 'Health Data Exchange Platform'
]

aufgabe_keywords = [
    'Open', 'Opens', 'Adjust', 'Adjusted', 'Dose', 'Dosed', 'Document', 'Documented',
    'Validate', 'Validated', 'Measure', 'Measured', 'Plan', 'Plans', 'Send', 'Sends',
    'Manual', 'Read', 'Reads', 'Enter', 'Enters', 'Display', 'Displays',
    'Evaluate', 'Evaluates', 'Save', 'Saves', 'Prepare', 'Prepared',
    'Accept', 'Accepts', 'Reject', 'Rejects', 'Register', 'Registers',
    'Administer', 'Administered', 'Initialize', 'Initialized', 'Analyze', 'Analyzed', 'Coordinate', 'Coordinates', 'Collaborate', 'Collaborates', 'Implement', 'Implements', 'Optimize', 'Optimizes', 'Integrate', 'Integrates'
]
daten_keywords = [
    'Data', 'Measurement Data', 'Code', 'Setting', 'Personal Data', 'Invitation', 'Release', 'File', 'Clinical Data', 'Health Records', 'Patient History', 'Laboratory Results', 'Imaging Data', 'Genomic Data', 'Biometric Data'
]
schritt_keywords = [
    'Guide', 'Guided', 'Record', 'Recorded', 'Advise', 'Advised', 'Assess', 'Assessed',
    'Diagnose', 'Diagnosed', 'Recommend', 'Recommended', 'Inform', 'Informed',
    'Coach', 'Coached', 'Administrative Recording', 'Medical Recording', 'Enable', 'Enabled',
    'Data Processing', 'Data Processed', 'Data Exchange', 'Data Exchanged', 'Data Presentation', 'Data Presented',
    'Data Collection', 'Data Collected', 'Data Interpretation', 'Data Interpreted', 'Data Storage', 'Data Stored',
    'Data Management', 'Data Managed', 'Document', 'Documented', 'Documentation for SGB Purposes', 'Self-documentation',
    'Remind', 'Reminded', 'Intervene', 'Intervened', 'Treat', 'Treated', 'Operate', 'Operated',
    'Physiotherapy', 'Rehabilitation', 'Rehabilitated', 'Prescribe', 'Prescribed', 'Measure', 'Measured',
    'Care', 'Cared', 'Plan', 'Planned', 'Educate', 'Educated', 'Self-inform', 'Informed',
    'Second Opinion', 'Second Opinion Obtained', 'Monitor', 'Monitored', 'Refer', 'Referred',
    'Administrative Management', 'Administratively Managed', 'Bill', 'Billed', 'Warn', 'Warned', 'Consult', 'Consulted', 'Refer', 'Refers', 'Follow-up', 'Followed-up', 'Reassess', 'Reassessed', 'Educate', 'Educated'

]
kommunikation_keywords = [
    'Communication Channel', 'Phone', 'Fax', 'Email', 'Video Call', 'Web Portal', 'Direct Contact',
    'Letter', 'KVConnect', 'KIM', 'TIM', 'ePA', 'ePrescription Service', 'Electronic Patient File',
    'Clinical Data Repository', 'Other Document Exchange', 'DiGA', 'BTLE', 'App', 'Server', 'Notification', 'Patient Engagement', 'Health Literacy', 'Patient Education', 'Clinical Communication', 'Healthcare Collaboration'
]

# Digital Communication Methods
digital_communication_keywords = [
    'Email', 'Video Call', 'Web Portal', 'KVConnect', 'KIM', 'TIM', 'ePA',
    'ePrescription Service', 'Electronic Patient File', 'Clinical Data Repository',
    'Other Document Exchange', 'DiGA', 'BTLE', 'App', 'Server', 'Notification'
]

# Analog Communication Methods
analog_communication_keywords = [
    'Communication Channel', 'Phone', 'Fax', 'Direct Contact', 'Letter'
]

information_keywords = [
    'Perceive', 'Perceived', 'Search', 'Searched', 'Record', 'Recorded', 'Present', 'Presented', 'Compare', 'Evaluate'
    'Comment', 'Commented', 'Query', 'Queried', 'Discover', 'Discovered', 'Locate', 'Localized', 'Analyze', 'Analyzed', 'Synthesize', 'Synthesized', 'Interpret', 'Interpreted', 'Report', 'Reported', 'Summarize', 'Summarized'
]


def classify_task_description(description):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(description)
    words_pos = nltk.pos_tag(words)

    modified_description = []
    for word, pos in words_pos:
        # Lemmatisierung nur für Verben
        lemma = lemmatizer.lemmatize(word.lower(), 'v') if pos.startswith('VB') else word.lower()

        matched = False
        for category, keywords in {
            'Participant': akteure_keywords, 'Task': aufgabe_keywords,
            'Data': daten_keywords, 'Schritt': schritt_keywords,
            'Communication-digital': digital_communication_keywords,
            'Communication-analoge': analog_communication_keywords,
            'Information': information_keywords,
            'System': system_keywords
        }.items():
            # Für die Kategorie "Aufgabe" wird das lemmatisierte Wort verglichen
            if category == 'Task' and lemma in [k.lower() for k in keywords]:
                modified_description.append(f"{lemma} :: ({category})")
                matched = True
                break
            # Für andere Kategorien wird das Originalwort verglichen
            elif word.lower() in [k.lower() for k in keywords]:
                modified_description.append(f"{word} :: ({category})")
                matched = True
                break

        if not matched:
            modified_description.append(word)

    return ' '.join(modified_description)


# Beispiel
description = "Patient sendet Nachricht über WebPortal"
result = classify_task_description(description)
print(result)


# Anpassen der modify_bpmn_labels Funktion
def modify_bpmn_labels(bpmn_file_path, output_file_path):
    bpmn_tree = ET.parse(bpmn_file_path)
    bpmn_root = bpmn_tree.getroot()

    relevant_tags = ['task', 'userTask', 'serviceTask', 'sendTask', 'receiveTask',
                     'manualTask', 'businessRuleTask', 'scriptTask', 'callActivity',
                     'subProcess', 'transaction', 'event', 'startEvent', 'endEvent',
                     'intermediateThrowEvent', 'intermediateCatchEvent', 'boundaryEvent',
                     'laneSet', 'lane', 'participant']

    for element in bpmn_root.iter():
        if any(tag in element.tag for tag in relevant_tags):
            name = element.get('name')
            if name:
                modified_label = classify_task_description(name)
                element.set('name', modified_label)

    bpmn_tree.write(output_file_path)

# Beispiel für die Verwendung
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/parkinson_go_structured/parkinsonGo_Order.bpmn',
                   '/diagrams/results_modified_diagrams/ParkinsonGo_order_modified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/parkinson_go_structured/ParkinsonGoDailyUsage.bpmn',
                   '/diagrams/results_modified_diagrams/ParkinsonGo_DailyUsage_modified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/parkinson_go_structured/ParkinsonGoDoctorConsultation.bpmn',
                   '/diagrams/results_modified_diagrams/ParkinsonGoDoctorConsultation_modified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/parkinson_go_structured/parkinsongoInitialAssessment.bpmn',
                   '/diagrams/results_modified_diagrams/ParkinsonGoDoctorInitialAssessment_modified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/parkinson_go_structured/ParkinsonGoRemote.bpmn',
                   '/diagrams/results_modified_diagrams/ParkinsonGoRemote_modified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/parkinson_go_structured/ParkinsonGoSensorSetup.bpmn',
                   '/diagrams/results_modified_diagrams/ParkinsonGoSensorSetup_modified.bpmn')


modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/ProHerzDailyUsage.bpmn',
                   '/diagrams/results_modified_diagrams/ProHerzDailyUsageModified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/ProHerzSetUp.bpmn',
                   '/diagrams/results_modified_diagrams/ProHerzSetup_modified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/ProHerzDataExtract.bpmn',
                   '/diagrams/results_modified_diagrams/ProHerzDataExtract_modified.bpmn')
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/ProHerzDataSharing.bpmn',
                   '/diagrams/results_modified_diagrams/ProHerzDataSharing_modified.bpmn')
