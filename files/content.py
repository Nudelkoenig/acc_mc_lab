greeting = """
Vielen Dank, dass Sie sich für die Teilnahme an dieser Studie entschieden haben!<br>
+ Ihre Aufgabe wird es sein, den <b>Preis</b> von beschriebenen <b>Pauschalreisen</b> zu <b>schätzen</b>.
+ Die Bearbeitungszeit beträgt ca. <b>20 Minuten</b>.
+ Am Ende der Studie erhalten Sie <b>Feedback</b> zu Ihrer persönlichen Schätzleistung.
+ Die Teilnahme and dieser Studie wird mit <b>5€</b> per Überweisung oder <b>0,5 Versuchspersonenstunden</b> vergütet. 
+ Zusätzlich werden Rahmen dieser Studie <b>10 x 20€</b> und <b>10 x 10€</b> verlost unter allen Teilnehmer:innen verlost.<br>
"""

greeting_acc = """
Vielen Dank, dass Sie sich für die Teilnahme an dieser Studie entschieden haben!<br>
+ Ihre Aufgabe wird es sein, den <b>Preis</b> von beschriebenen <b>Pauschalreisen</b> zu <b>schätzen</b>.
+ Die Bearbeitungszeit beträgt ca. <b>20 Minuten</b>.
+ Am Ende der Studie erhalten Sie <b>Feedback</b> zu Ihrer persönlichen Schätzleistung.
+ Darüberhinaus werde zufällig einige Teilnehmer:innen dieser Studie für ein <b>zusätzliches Interview</b> mit einer erfahrenen 
Reisekauffrau und einem Psychologen ausgewählt. 
+ Dieses Interview dauert ca. <b>15 Minuten</b> und wird mittels des <b>Videokonferenzsystems (BigBlueButton)</b> der Universität Göttingen geführt werden.
+ Die Teilnahme an dieser Studie wird mit <b>5€</b> per Überweisung oder <b>0,5</b> Versuchspersonenstunden vergütet. 
+ Zusätzlich werden im Rahmen dieser Studie <b>10 x 20€</b> und <b>10 x 10€</b> unter allen Teilnehmer:innen verlost.<br>

"""

screening_page_content = dict(
    title="Screening",
    statustext="Klicken Sie auf 'Weiter', um mit dem Experiment zu beginnen",
    screening_info=(
        "Eine mehrmalige Teilnahme an dieser Studie ist leider nicht möglich. "
        "Um auszuschließen, dass Sie bereits im Vorfeld an dieser Studie teilgenommen haben, "
        "benötigen wir Ihre E-Mailadresse. "
    ),
    email_instruction="Bitte geben Sie Ihre E-Mailadresse ein",
    email_pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    email_match_hint="Bitte geben Sie eine gültige E-Mailadresse ein.",
    data_protection_info=(
        "Ihre E-Mail-Adresse wird getrennt von Ihrem Experimentaldatensatz und in einer Form, die "
        "keine Rückschlüsse auf Ihre tatsächliche E-Mailadresse ermöglicht, gespeichert. "
        "Sie wird ausschließlich für den Abgleich mit E-Mailadressen von "
        "vorherigen Teilnehmenden erhoben."
    ),
    exclusion_title="Sie sind ausgeschlossen worden!",
    exclusion_icon="times-circle",
    exclusion_message="Leider können Sie an diesem Experiment nicht teilnehmen.",
)

informed_consent_content = dict(
    experimenter_in_charge="Johannes Rollwage",
    experimenter_in_charge_email="rollwage@psych.uni-goettingen.de",
    privacy_officer="Herr Prof. Dr. Wiebe",
    privacy_officer_email="datenschutzvorfall@uni-goettingen.de",
    study_email="vacation.estimation@gmail.com",
    consent_accept_label="Akzeptieren",
    consent_reject_label="Ablehnen",
    # language=HTML
    title="Einverständniserklärung",
    statustext="",
    # language=HTML
    introduction="""<span style="font-size: large; "><b>Allgemeine Informationen 
    zum Datenschutz</b></span>""",
    # language=HTML
    experiment_info="""Bei der Durchführung von Experimenten werden durch die dabei zu 
    treffenden Entscheidungen der Teilnehmer:innen Daten generiert. Diese Daten werden 
    wissenschaftlich durch die Abteilung für Wirtschafts- und Sozialpsychologie des 
    Georg-Elias-Müller-Institutes für Psychologie ausgewertet. Dabei werden alle Forschungsdaten 
    grundsätzlich <b>getrennt</b> von personenbezogenen Daten gespeichert, die eine direkte 
    Identifizierung einzelner Teilnehmer:innen erlauben würden.""",
    # language=HTML
    anonymity_info="""<b>Eine nachträgliche Verknüpfung von Forschungsdaten mit Merkmalen, 
    die einen direkten Rückschluss auf Ihre Person zulassen, ist im vorliegenden Versuch 
    nicht möglich!</b>""",
    # language=HTML
    personal_data_info="""Auf der nächsten Seite dieses Versuchs werden wir Ihre E-Mailadresse abfragen, 
    um Ihre Teilnahme zu dokumentieren.
     Zusätzlich werden wir am Ende dieser Studie Ihren Vornamen, Nachnamen und nochmals Ihre 
    E-Mail-Adresse sowie ggf. Ihre Matrikelnummer abfragen, diese personenbezogenen Daten dienen dazu, 
    um Ihnen Ihre Versuchspersonenstunden auszustellen bzw. Sie im Fall eines Gewinnes bei der Verlosung zu
     kontaktieren. <br>
""",
    # language=HTML
    data_disclaimer="""Die <b>anonymen</b> Forschungsdaten werden für die Erstellung von 
    wissenschaftlichen Forschungsarbeiten und Vorträgen genutzt. Diese Arbeiten werden 
    veröffentlicht. In den Veröffentlichungen ist die Zuordnung von Forschungsdaten zu einzelnen 
    Personen ausgeschlossen. Anonymisierte Daten können ebenfalls im Sinne einer transparenten und 
    offenen Wissenschaft Dritten zur Verfügung gestellt werden. Personenbezogene Daten werden 
    grundsätzlich nicht an Dritte weitergegeben.""",
    # language=HTML
    consent="""<span style="font-size: large; "><b>Einwilligungserklärung zur Datenerhebung und Datenverarbeitung</b></span>
    <br><br>
    Ich erkläre mich damit einverstanden, dass im Rahmen dieser Studie mich betreffende 
    personenbezogene Daten/Angaben durch die Versuchsleitung erhoben und verarbeitet werden. 
    Mir ist bekannt, dass die erhobenen personenbezogenen Daten gelöscht werden, sobald dies 
    nach dem Forschungs- oder Statistikzweck möglich ist. Von dieser Löschung nicht betroffen 
    sind anonymisierte Daten, die keinen Rückschluss auf meine Person zulassen. <br>
    Ich bin auch damit einverstanden, dass die Studienergebnisse in anonymer Form 
    veröffentlicht werden. Mir ist bekannt, dass ich jederzeit mein Einverständnis ohne Angabe 
    von Gründen und ohne nachteilige Folgen für mich zurückziehen und eine Löschung der von 
    mir erhobenen Daten verlangen kann. Mir ist jedoch klar, dass eine Löschung bereits 
    anonymisierter Daten nicht mehr möglich sein wird. Mir ist bekannt, dass meine Angaben in 
    Übereinstimmung mit §4 BDSG behandelt werden.
    <br><br>
    Der Verantwortliche für diese Studie und die Datenerhebung ist:
    <br>
    {experimenter_in_charge} ({experimenter_in_charge_email}).
    <br><br>
    Der für diese Studie verantwortliche Datenschutzbeauftragte ist der Datenschutzbeauftragte 
    der Georg-August-Universität Göttingen, {privacy_officer}. <br>
    Datenschutzverstöße und -probleme kann ich jederzeit unter folgender E-Mail-Adresse melden:
    {privacy_officer_email}
    <br><br>
    Mir ist bekannt, dass ich bezogen auf die Verarbeitung meiner personenbezogenen Daten ein 
    Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde (Landesbeauftragte für den 
    Datenschutz Niedersachsen, Prinzenstraße 5, 30159 Hannover) habe. Mir ist zudem bekannt, 
    dass ich ein Recht auf Auskunft über meine verarbeiteten personenbezogenen Daten habe, 
    einschließlich einer unentgeltlichen Kopie dieser Daten. Dieses Auskunftsrecht besteht 
    gegenüber dem genannten Verantwortlichen. Weiterhin ist mir bekannt, dass ich ein Recht 
    auf Berichtigung sowie auf Löschung meiner verarbeiteten personenbezogenen Daten habe. 
    Ich willige ein, dass meine Angaben in Übereinstimmung mit Art. 6 DSGVO behandelt werden.
    <br> <br>
    Ich habe diesbezüglich keine weiteren Fragen mehr und willige hiermit in die dargestellte 
    Untersuchung ein. Alle mich interessierenden Fragen wurden ausreichend geklärt.
    <br><br>
    <b>Notiz:</b> Wenn Sie auf 'Akzeptieren' klicken, wird das Experiment sofort starten. Klicken 
    Sie auf 'Ablehnen', um das Experiment zu beenden, ohne dass Ihre persönlichen Daten 
    aufgezeichnet werden.""",
    consent_reject_title="Consent: Rejected",
    consent_reject_icon="times-circle",
    # The following text needs a {study_email} placeholder!
    # language=HTML
    consent_reject_message="""Sie haben das Experiment abgebrochen.
    <br><br>
    Sie können diese Seite jetzt schließen.
    <br><br>
    Wenn Sie Fragen haben, schreiben Sie uns bitte eine Mail an 
    <span style="color: blue; ">{study_email}</span>""",
)

instruction = """
Im Rahmen dieser Studie werden Sie gebeten, den <b>Preis</b> von beschriebenen <b>Pauschalreisen</b> 
zu <b>schätzen</b>. Explizit soll der Preis pro Person in Euro geschätzt werden.<br><br>
Um Ihnen die Schätzung zu erleichtern, handelt es sich ausschließlich um Pauschalreisen, die 
+ in der <b>Hauptsaison</b> stattfinden. 
+ von dem <b>gleichen Flughafen</b> in Deutschland starten. 
+ als Reisende <b>zwei erwachsene Personen</b> beinhalten.
<br>

Bitte bearbeiten Sie die Aufgaben gewissenhaft und sorgfältig, um eine hohe Datenqualität 
zu gewährleisten. <br>
"""

# TODO: Beschreibungen überarbeiten
no_acc = """
<strong><p style="text-align: center; font-size:26px; bold">Sie wurden nicht für ein zusätzliches Interview ausgewählt.</p></strong><br>
"""

process_accountability = """
Sie wurden für ein zusätzliches Interview ausgewählt. Nach Abschluss der Schätzaufgaben wird der Versuchsleiter einen
 Interviewtermin mit Ihnen vereinbaren und gemeinsam mit einer erfahrenen Reisekauffrau durchführen. 
 <br> <br>
In diesem Interview werden Sie hinsichtlich der von Ihnen bei den Schätzungen eingesetzen <b>Strategie</b> evaluiert.
Im Rahmen dieser Evaluation Ihres <b>Arbeitsprozesses</b> werden Sie gebeten werden zu rechtfertigen auf welchem Weg Sie zu 
ihren Einschätzungen gekommen sind. Dabei geht ausschließlich um Ihre <b>Vorgehen</b> bei den Schätzungen, die 
Interviewer sind nur daran interessiert wie Sie zu Ihren Einschätzungen gekommen sind. Das Ergebnis, d.h. die 
Genauigkeit Ihrer Schätzungen wird dabei keine Rolle spielen.
 <br> <br>
Bitte geben Sie hierzu zwei Termine die Ihnen für dieses Interview passen würden und Ihre E-Mailadresse an.
Diese beiden Termine sollten wochentags (Montag - Freitag) zwischen 08:00 und 18:00 Uhr und innerhalb der nächsten
 zwei Wochen liegen.
 <br> <br>
 """

outcome_accountability = """
Sie wurden für ein zusätzliches Interview ausgewählt. Nach Abschluss der Schätzaufgaben wird der Versuchsleiter einen
 Interviewtermin mit Ihnen vereinbaren und gemeinsam mit einer erfahrenen Reisekauffrau durchführen. Bitte geben Sie 
 hierzu zwei Termine zwischen 08:00 und 18:00 Uhr an, die innerhalb der nächsten
 zwei Wochen liegen und die Ihnen für dieses Interview passen würden, sowie Ihre E-Mailadresse an.
 <br> <br>
  In diesem Interview werden Sie hinsichtlich Ihres <b>Ergebnisses</b>, d.h. der Genauigkeit Ihrer Schätzungen evaluiert.
  Dabei geht ausschließlich um Ihre <b>Genauigkeit</b>, die Interviewer sind nur daran interessiert wie gut Ihre
  Schätzungen waren. Die Vorgehensweise, d.h. Ihr Arbeitsprozess bei den Schätzungen wird dabei keine Rolle spielen. 
  <br> <br>
Bitte geben Sie hierzu zwei Termine die Ihnen für dieses Interview passen würden und Ihre E-Mailadresse an.
Diese beiden Termine sollten wochentags (Montag - Freitag) zwischen 08:00 und 18:00 Uhr und innerhalb der nächsten
 zwei Wochen liegen.
"""

accountability3 = " Das etwa 15-minütige Interview wird mithilfe des Videokonferenzsystems der Universität Göttingen " \
                  "geführt. Hierzu ist keine Registrierung erforderlich. Sie erhalten einen Einladungslink zu der " \
                  "Videokonferenz per E-Mail. " \
                  "<br> " \
                  "Die konkrete Terminfestlegung erfolgt im Anschluss an das Experiment."

justify_instr = """ Für wie wahrscheinlich halten Sie es, dass Sie im Anschluss an die Aufgabe Ihre Entscheidung rechtfertigen müssen?"""

interview_pre = """ In dem zusätzlichen Interview wird es vorrangig um ... gehen."""

acc_pre = "Währenden der Aufgabe werde ich mich eher konzentrieren auf..."

task_begin = """ 
Auf der nächsten Seite beginnen die Schätzaufgaben zu den Preisen von Pauschalreisen."""

mc_begin = """ 
Bevor die Schätzaufgaben zu den Preisen von Pauschalreisen beginnen, haben wir auf den nächsten Seiten noch ein paar Fragen an Sie."""

task_complet = """ 
Sie haben nun die Preise von allen Pauschalreisen geschätzt. Die Studie ist fast geschafft. <br><br> 
Auf den folgenden Seiten haben wir noch einige Fragen zu Ihrem aktuellen Gemütszustand und Ihrem Fokus bei der 
Aufgabenbearbeitung."""

acc_post = """ Wofür haben Sie sich während der Aufgabenbearbeitung verantwortlich gefühlt?"""

interview_post = """ In dem kommenden Interview wird es vorrangig um ... gehen. """

systematic_information_processing1 = """
Ich werde versuchen alle möglichen Perspektiven bei der Einschätzung der Reisekosten einzunehmen.
"""

systematic_information_processing2 = """
Ich werde versuchen meine Einschätzungen so gründlich wie möglich zu machen.
"""

systematic_information_processing3 = """
Ich werde mir ausführliche Gedanken machen bevor ich eine Schätzung abgeben werde.
"""

epi_motiv_instr = """
Auf dieser Seite finden Sie einige Aussagen die sich auf Ihre geplante Vorgehensweise bei der folgende Aufgabe beziehen.
Wählen Sie dazu die auf Sie passende Antwort durch anklicken aus. Es gibt keine richtigen oder falschen
  Antworten. Überlegen Sie bitte nicht lange und entscheiden Sie dann, wie stark Sie denken, dass das jeweils beschriebene Vorgehen 
   bei Ihrer eigenen Arbeitsweise vorhanden sein wird.
"""

epi_motiv1 = """
Ich werde mich darum bemüht, alles sorgfältig zu durchdenken.
"""

epi_motiv2 = """
Ich werde diese Aufgabe systematisch angehen.
"""

epi_motiv3 = """
Ich werde versuchen, den logischen Zusammenhang zwischen den Eigenschaften und dem Preis der Reisen herauszufinden.
"""

epi_motiv4 = """
Ich werde die Aufgabe analytisch angehen.
"""

epi_motiv5 = """
Ich werde mich sehr auf die einzelnen Schritte konzentriert, die zur Bewältigung dieser Aufgabe nötig sind.
"""

epi_motiv6 = """
Ich werde versuchen Regeln herauszufinden, auf die ich meine Schätzung gründen kann.
"""

epi_motiv7 = """
Ich werde mich sehr darauf konzentieren was ich tue, um eine Antwort auf die Schätzungaufgabe zu finden.
"""

epi_motiv8 = """
Ich werde mir meines Denkprozesses sehr bewusst sein.
"""

epi_motiv9 = """
Ich werde Einschätzungen machen, indem ich sorgfältig alle Informationen analysier, die mir zur verfügung stehen.
"""

epi_motiv10 = """
Ich werde klare Regeln verwenden.
"""

## Manipulationskontrolle nach Zhang & Mittal (2005)
MC_PA1 = """
Während ich meine Schätzungen abgebe, werde ich mich hauptsächlich auf den Prozess meiner Entscheidungsfindung konzentrieren.
"""

MC_OA1 = """
Während ich meine Schätzungen abgebe, werde ich mich hauptsächlich auf das Ergebnis meiner Entscheidungen konzentrieren.
"""

MC_PA2 = """
Ich werde meinen Entscheidungsprozess rechtfertigen müssen.
"""

MC_OA2 = """
Ich werde die Ergebnisse meiner Schätzungen rechtfertigen müssen.
"""

MC_PA3 = """
Ich werde mich bemühen eine gute Strategie für meine Schätzungen zu finden und nicht möglichst gute Schätzungen abzugeben.
"""

MC_OA3 = """
Ich werde mich bemühen möglichst gute Schätzungen abzugeben und nicht eine möglichst gute Strategie für die Schätzungen zu verfolgen.
"""

MC_PA4 = """
Ich werde hauptsächlich auf eine möglichst gute Strategie für meine Schätzungen achten.
"""

MC_OA4 = """
Ich werde hauptsächlich auf das Abgeben möglichst guter Schätzungen achten.
"""

instruction_STAI ="""
Auf dieser Seite finden sie einige Gefühlsbeschreibungen, bitte geben Sie an wie sehr diese <b>im Moment </b> 
auf Sie zu treffen? Wählen Sie dazu die auf Sie passende Antwort durch anklicken aus. Es gibt keine richtigen oder 
falschen Antworten. Überlegen Sie bitte nicht lange und entscheiden Sie dann, wie stark das betreffende Gefühl im Moment
 bei Ihnen vorhanden ist.
"""

STAI_S1 = """
Ich bin ruhig.
"""

STAI_S2 = """
Ich fühle mich geborgen.
"""

STAI_S3 = """
Ich fühle mich angespannt.
"""

STAI_S4 = """
Ich bin bekümmert.
"""

STAI_S5 = """
Ich fühle mich ungezwungen.
"""

STAI_S6 = """
Ich fühle mich ungezwungen.
"""

STAI_S7 = """
Ich bin besorgt, dass etwas schiefgehen könnte.
"""

STAI_S8 = """
Ich fühle mich ausgeruht.
"""

STAI_S9 = """
Ich bin beunruhigt.
"""

STAI_S10 = """
Ich fühle mich wohl.
"""

STAI_S11 = """
Ich fühle mich selbstsicher.
"""

STAI_S12 = """
Ich bin nervös.
"""

STAI_S13 = """
Ich bin zappelig.
"""

STAI_S14 = """
Ich bin verkrampft.
"""

STAI_S15 = """
Ich bin entspannt.
"""

STAI_S16 = """
Ich bin zufrieden.
"""

STAI_S17 = """
Ich bin besorgt.
"""

STAI_S18 = """
Ich bin überreizt.
"""

STAI_S19 = """
Ich bin froh.
"""

STAI_S20 = """
Ich bin vergnügt.
"""

suspicion_check = """
Was glauben Sie, war das Ziel dieser Studie?
"""

comments = """
Haben Sie noch weitere Anmerkungen?
"""


registration_selection_content = dict(
    title="Vergütung",
    statustext="Klicken Sie auf 'Weiter', wenn Sie eine Auswahl getroffen haben.",
    instr_selection="<b>Folgende Vergütungsoptionen stehen zur Auswahl:</b>",
    instr_choice="Bitte entscheiden Sie sich für eine Vergütungsoption",
    # The following option needs to be set to the number of options
    # in this dictionary. There can be more options in the dictionary
    # than are shown on the page. You can add configuration blocks for
    # more options and update the available_options setting, whenever
    # necessary
    available_options=5,
    show_option_1=True,
    option_1_instruction="<u>Überweisung: </u><br>"
                         "Zusätzlich zur Teilnahme an der Geldverlosung erhalten Sie 5€ in Form einer Überweisung "
                         " Sofern Sie sich für diese Vergütungsoption entscheiden, "
                         "benötigen wir auf der nächsten Seite die Eingabe persönlicher"
                         " Informationen (Name, Vorname, E-Mail-Adresse, IBAN, BIC, Wohnanschrift). "
                         "Die von Ihnen angegebenen Informationen werden vertraulich behandelt und dienen "
                         "ausschließlich dazu Sie für Ihre Teilnahme zu vergüten.",
    option_1_label="Überweisung & Verlosung",
    option_1_register_name=True,
    option_1_register_birth_date=False,
    option_1_register_email=True,
    option_1_register_phone=False,
    option_1_register_iban=True,
    option_1_register_address=True,
    option_1_register_various=False,
    option_1_register_payout=False,

    show_option_2=True,
    option_2_instruction="<u>Versuchspersonen-Stunden: </u><br>"
                         "Zusätzlich zur Teilnahme an der Geldverlosung haben Sie als "
                         "Göttinger Psychologie-Student*in die Möglichkeit, sich die "
                         "Teilnahme mit 0,5 Versuchspersonenstunden vergüten zu lassen."
                         " Sofern Sie sich für diese Vergütungsoption entscheiden, "
                         "benötigen wir auf der nächsten Seite die Eingabe persönlicher"
                         " Informationen (Matrikelnummer, Name, Vorname, "
                         "E-Mail-Adresse). Die von Ihnen angegebenen Informationen "
                         "werden vertraulich behandelt und dienen ausschließlich der "
                         "Ausstellung ihrer Versuchspersonenstunden.",
    option_2_label="VP-Stunden & Verlosung",
    option_2_register_name=True,
    option_2_register_birth_date=False,
    option_2_register_email=True,
    option_2_register_phone=False,
    option_2_register_iban=False,
    option_2_register_address=False,
    option_2_register_various=True,
    option_2_register_payout=False,

    show_option_3=True,
    option_3_instruction="<u>Keine Verlosungs-Teilnahme</u><br>"
                         "Sie können die Teilnahme an der Verlosung auch ablehnen. In "
                         "diesem Fall werden keine weiteren persönlichen Informationen "
                         "erfragt.",
    option_3_label="Teilnahme ablehnen",
    option_3_register_name=False,
    option_3_register_birth_date=False,
    option_3_register_email=False,
    option_3_register_phone=False,
    option_3_register_iban=False,
    option_3_register_address=False,
    option_3_register_various=False,
    option_3_register_payout=False,

    show_option_4=False,
    option_4_instruction="<b>4. Spende: </b>"
                         "Bei der Auswahl dieser Vergütungsoption, werden keinerlei persönliche"
                         "Angaben benötigt. Ein Pauschalbetrag von X € wird an Y pro Auswahl dieser"
                         "Option gespendet.",
    option_4_label="4. Spende",
    option_4_register_name=True,
    option_4_register_birth_date=False,
    option_4_register_email=True,
    option_4_register_phone=False,
    option_4_register_iban=False,
    option_4_register_address=False,
    option_4_register_various=False,
    option_4_register_payout=False,

    show_option_5=False,
    option_5_instruction="This is the instruction for option 5.",
    option_5_label="Itemlabel Option 5",
    option_5_register_name=True,
    option_5_register_birth_date=False,
    option_5_register_email=True,
    option_5_register_phone=False,
    option_5_register_iban=False,
    option_5_register_address=False,
    option_5_register_various=False,
    option_5_register_payout=False,
)

registration_page_content = dict(
    title="Registrierung",
    statustext="Um Ihre Registrierung zu abzuschließen, klicken Sie auf 'Weiter'.",
    instr_no_registration="Wir benötigen keine persönlichen Daten von Ihnen. "
                          "Sie können auf 'Weiter' klicken.",
    instr_registration="Bitte geben Sie die folgenden persönlichen Informationen ein.",
    first_name_instr="Bitte geben Sie Ihren Vornamen ein",
    last_name_instr="Bitte geben Sie Ihren Nachnamen ein",
    birth_date_instr="Bitte geben Sie Ihr Geburtsdatum ein",
    birth_date_pattern=r"^(0[1-9]|[12][0-9]|3[01])[-/.](0[1-9]|1[012])[-/.](19|20)\d\d$",
    birth_date_suffix="TT.MM.JJJJ",
    birth_date_match_hint="Dies ist der Match-Hinweis für das Feld Geburtsdatum.",
    email_instr="Bitte geben Sie Ihre E-Mail-Adresse ein",
    email_pattern=r"[^@]+@[^@]+\.[^@]+",
    email_match_hint="Bitte geben Sie eine gültige E-Mail-Adresse ein.",
    iban_instr="Bitte geben Sie Ihre IBAN ein",
    iban_pattern=r"^[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?:[ ]?[0-9]{1,2})?$",
    iban_match_hint="Fehler: Bitte überprüfen Sie Ihre Eingabe.",
    bic_instr="Bitte geben Sie Ihren BIC ein",
    bic_pattern=r"^[a-zA-Z]{6}[0-9a-zA-Z]{2}([0-9a-zA-Z]{3})?$",
    bic_match_hint="Fehler: Bitte überprüfen Sie Ihre Eingabe.",
    tax_office_instr="Bitte geben Sie den Sitz Ihres Finanzamtes an.",
    phone_instr="Bitte geben Sie Ihre Telefonnummer ein",
    phone_pattern=r"^\+?(?:[0-9]\x20?){6,14}[0-9]$",
    phone_match_hint="Fehler: Bitte überprüfen Sie Ihre Eingabe.",
    street_instr="Bitte geben Sie den Straßennamen ein",
    house_number_instr="Bitte geben Sie die Hausnummer ein",
    postal_code_instr="Bitte geben Sie die Postleitzahl ein",
    postal_code_pattern=r"(?i)^[a-z0-9][a-z0-9\- ]{0,10}[a-z0-9]$",
    postal_code_match_hint="Fehler: Bitte überprüfen Sie Ihre Eingabe.",
    city_instr="Bitte geben Sie den Stadtnamen ein",
    country_instr="Bitte geben Sie den Ländernamen ein",
    various_instr="Bitte geben Sie Ihre Matrikelnummer ein",
    various_pattern=r"^..*$",  # Anything but empty
    various_match_hint="Fehler: Bitte überprüfen Sie Ihre Eingabe.",
    privacy_info="This is a dummy text for privacy information",
    repeated_title="Anscheinend haben Sie bereits an dem Experiment teilgenommen",
    repeated_text="This is a dummy text for the repeated participation page",
    repeated_participation_title="Erneute Teilnahme detektiert",
    repeated_participation_icon="times-circle",
    repeated_participation_message="Es tut uns leid, aber eine wiederholte Teilnahme an diesem "
                                   "Experiment ist nicht erlaubt. Ihre persönlichen Daten werden "
                                   "nicht gespeichert",
)



disclaimerregistr = """<b>Hinweis:</b> Die Verlosung erfolgt, sobald die Datenerhebung abgeschlossen ist. Dies kann 
noch ein paar Wochen dauern. Im Gewinnfall benachrichtigen wir Sie per E-Mail. Die Überweisungen und das Ausstellen der
Versuchspersonenstunden finden blockweise statt. Daher kann es auch hierbei zu Wartezeiten von ein bis zwei Wochen 
kommen. Wir senden Ihne die Bescheinigung über das Ableisten der Versuchspersonenstunde per E-Mail. 
Herzlichen Dank für Ihr Verständnis.
"""

