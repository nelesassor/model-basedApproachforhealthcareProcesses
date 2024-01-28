from nltk.stem import WordNetLemmatizer
import xml.etree.ElementTree as ET
import nltk
from nltk.tokenize import word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Beispiel für Zuordnungstabellen basierend auf den extrahierten Daten
akteure_keywords = [
    'Akteur', 'Person', 'Arzt', 'Patient', 'Apotheker', 'Pfleger', 'Therapeut',
    'Psychotherapeut', 'Angehörige', 'PatientenVertreter', 'Hausarzt', 'Notarzt',
    'ApprobierterHeilberufler', 'Facharzt', 'NichtApprobierterHeilberufler', 'AltenPfleger',
    'Diätassistent', 'GesundheitsUndKrankenpfleger', 'MedizinischeFachangestellte',
    'Notfallsanitäter', 'Diabetesberater', 'NäPaVERAH', 'Heilmittelerbringer', 'Physiotherapeut',
    'HilfsmittelHersteller', 'DigaHersteller', 'ImplantateHersteller', 'Labor', 'SOZV',
    'GesetzlicheKrankenversicherung', 'Pflegeversicherung', 'Rentenversicherung',
    'Unfallversicherung', 'LEOrganistaion', 'StationäreLEOrganisation', 'Krankenhaus',
    'StationärePflege', 'StationäreReha', 'AmbulanteLEOrganisation', 'Notfallambulanz',
    'Apotheke', 'Rettungsdienst', 'TelemedizinischesZentrum', 'KassenärztlicherBereitschaftsdienst',
    'AmbulanterPflegedienst', 'MVZ', 'Arztpraxis', 'VorOrtApotheke', 'OnlineApotheke',
    'Hersteller', 'Sensor', 'Medizinisches Fachpersonal'
]
aufgabe_keywords = [
    'Öffnen', 'Öffnet', 'Einstellen', 'Eingestellt', 'Dosieren', 'Dosiert', 'Dokumentieren', 'Dokumentiert',
    'Validieren', 'Validiert', 'Messen', 'Gemessen', 'Planen', 'Plant', 'Senden', 'Sendet',
    'Manuell', 'Ablesen', 'Liest ab', 'Eingeben', 'Gibt ein', 'Anzeigen', 'Zeigt an',
    'Auswerten', 'wertet aus', 'Speichern', 'speichert', 'Aufbereiten', 'Aufbereitet',
    'Annehmen', 'nimmt an', 'Ablehnen', 'lehnt ab', 'Anmelden', 'meldet an',
    'Applizieren', 'Appliziert', 'Initialisieren', 'Initialisiert', 'analyisieren', 'analysiert'
]
daten_keywords = [
    'Daten', 'Messdaten', 'Code', 'Einstellung', 'Personendaten', 'Einladung', 'Freigabe', 'Datei'
]
schritt_keywords = [
    'Anleiten', 'Angeleitet', 'Aufnehmen', 'Aufgenommen', 'Beraten', 'Beraten', 'Bewerten', 'Bewertet',
    'Diagnostizieren', 'Diagnostiziert', 'Empfehlen', 'Empfohlen', 'Informieren', 'Informiert',
    'Coachen', 'Gecoacht', 'AdministrativAufnehmen', 'MedizinischAufnehmen', 'Befähigen', 'Befähigt',
    'DatenVerarbeiten', 'DatenVerarbeitet', 'DatenAustauschen', 'DatenAusgetauscht', 'DatenDarstellen', 'DatenDargestellt',
    'DatenErheben', 'DatenErhoben', 'DatenInterpretieren', 'DatenInterpretiert', 'DatenSpeichern', 'DatenGespeichert',
    'DatenVerwalten', 'DatenVerwaltet', 'Dokumentieren', 'Dokumentiert', 'DokumentierenZuZweckenDesSGB', 'Selbstdokumentation',
    'Erinnern', 'Erinnert', 'Intervenieren', 'Interveniert', 'Behandeln', 'Behandelt', 'Operieren', 'Operiert',
    'Physiotherapie', 'Rehabilitation', 'Rehabilitiert', 'Verordnen', 'Verordnet', 'Messen', 'Gemessen',
    'Pflegen', 'Gepflegt', 'Planen', 'Geplant', 'Schulen', 'Geschult', 'SichInformieren', 'Informiert',
    'ZweitmeinungEinholen', 'ZweitmeinungEingeholt', 'Überwachen', 'Überwacht', 'Überweisen', 'Überwiesen',
    'AdministartivVerwalten', 'AdministrativVerwaltet', 'Abrechnen', 'Abgerechnet', 'Warnen', 'Gewarnt'
]
kommunikation_keywords = [
    'Kommunikationsweg', 'Telefon', 'Fax', 'EMail', 'VideoCall', 'WebPortal', 'DirekterKontakt',
    'Brief', 'KVConnect', 'KIM', 'TIM', 'ePA', 'eRezeptFachdienst', 'ElektronischeFallakte',
    'ClinicalDataRepository', 'SonstigerDokumentenaustausch', 'DiGA', 'BTLE', 'App', 'Server', 'Benachrichtigung'
]

information_keywords = [
    'Wahrnehmen', 'Wahrgenommen', 'Suchen', 'Gesucht', 'Aufzeichen', 'Aufgezeichnet', 'Präsentieren', 'Präsentiert',
    'Kommentieren', 'Kommentiert', 'Abfragen', 'Abgefragt', 'Entdecken', 'Entdeckt', 'Lokalisieren', 'Lokalisiert'
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
            'Akteure': akteure_keywords, 'Aufgabe': aufgabe_keywords,
            'Daten': daten_keywords, 'Schritt': schritt_keywords,
            'Kommunikation': kommunikation_keywords,
            'Information': information_keywords
        }.items():
            # Für die Kategorie "Aufgabe" wird das lemmatisierte Wort verglichen
            if category == 'Aufgabe' and lemma in [k.lower() for k in keywords]:
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
modify_bpmn_labels('/Users/nelesassor/PycharmProjects/bpmnMapping/diagrams/ParkinsonGo_Modell_V3.bpmn',
                   '/diagrams/results_modified_diagrams/ParkinsonGo_Modell_V3_modified.bpmn')
