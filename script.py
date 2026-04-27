# -*- coding: utf-8 -*-
import time
import re
import datetime
import alfred3 as al
from thesmuggler import smuggle
import random
import pprint
import csv

# TODO: Pagetype?

content = smuggle("files/content.py")
screening = smuggle("files/exp_screening.py")
registration = smuggle("files/exp_registration.py")
informed_consent = smuggle("files/informed_consent.py")

exp = al.Experiment()


# Introduction
@exp.setup
def setup(exp):
    # Yoking
    exp.session_timeout = 3600


    randomizer = al.ListRandomizer(
        ("control", 45), ("process_accountability", 45), ("outcome_accountability", 45), exp=exp, inclusive=False,
        respect_version=True
    )

    exp.condition = randomizer.get_condition()
    exp.log.warning(exp.condition)
    exp.exclusion_list = list(exp.read_csv_tolist("files/exclusion_list.csv"))
    print(exp.condition)
    position1 = [6, 7]
    exp.first = random.choice(position1)


@exp.member
class ExpSection(al.Section):
    allow_forward = True
    allow_backward = False
    allow_jumpfrom = False
    allow_jumpto = False


@exp.member(of_section="ExpSection")
class LandingPage(al.Page):
    name = "landingpage"
    title = "Herzlich Willkommen zur Studie"

    def on_exp_access(self):
        if self.exp.condition == "outcome_accountability":
            self += al.Text(text=content.greeting_acc, position="center")
        elif self.exp.condition == "process_accountability":
            self += al.Text(text=content.greeting_acc, position="center")
        else:
            self += al.Text(text=content.greeting_acc, position="center")



@exp.member(of_section="ExpSection")
class InformedConsentPage(informed_consent.InformedConsent):
    content = content.informed_consent_content


@exp.member(of_section="ExpSection")
class Screening(screening.ScreeningPage):
    email_screening = True
    register_on_hiding = True
    mortimer_url = "https://alfredo3.psych.bio.uni-goettingen.de/mortimer3"
    content = content.screening_page_content


class InstructionPage1(al.Page):
    name = "instruction1"
    title = "Erläuterung der Schätzaufgabe"

    def on_exp_access(self):
        self += al.Text(content.instruction)


class InitialStressPage(al.Page):
    name = "initial"
    title = "Bevor es los geht"

    def on_exp_access(self):
        self += al.Text(content.instruction_STAI, align="center")
        STAI_items = [
            ("STAI_S_01", "Ich bin ruhig."),
            ("STAI_S_02", "Ich fühle mich geborgen."),
            ("STAI_S_03", "Ich fühle mich angespannt."),
            ("STAI_S_04", "Ich bin bekümmert."),
            ("STAI_S_05", "Ich fühle mich ungezwungen."),
            ("STAI_S_06", "Ich bin aufgeregt."),
            ("STAI_S_07", "Ich bin besorgt, dass etwas schiefgehen könnte."),
            ("STAI_S_08", "Ich fühle mich ausgeruht."),
            ("STAI_S_09", "Ich bin beunruhigt."),
            ("STAI_S_10", "Ich fühle mich wohl."),
            ("STAI_S_11", "Ich fühle mich selbstsicher."),
            ("STAI_S_12", "Ich bin nervös."),
            ("STAI_S_13", "Ich bin zappelig."),
            ("STAI_S_14", "Ich bin verkrampft."),
            ("STAI_S_15", "Ich bin entspannt."),
            ("STAI_S_16", "Ich bin zufrieden."),
            ("STAI_S_17", "Ich bin besorgt."),
            ("STAI_S_18", "Ich bin überreizt."),
            ("STAI_S_19", "Ich bin froh."),
            ("STAI_S_20", "Ich bin vergnügt.")
        ]

        for item in STAI_items:
            # Text element to display the item text
            # item_text = al.Text(item[1], width="full")

            # SingleChoiceBar for user input
            item_choice = al.SingleChoiceBar(
                "überhaupt nicht <br> 1", "ein wenig <br> 2", "ziemlich <br> 3", "sehr <br> 4",
                name=f"initial{item[0]}", leftlab=item[1], force_input=True)

            # Important: We use a Row element to arrange text and input horizontally
            self += al.Hline()
            self += item_choice

# @exp.member(of_section="ExpSection")
# class InstructionPage2(al.Page):
#    name = "instruction2"
#    title = "Einleitung Teil 2"
#
#    def on_exp_access(self):
#        self += al.Text(content.instruction)
#
#        if self.exp.condition == "process_accountability":
#            self += al.Text(content.process_accountability)
#
#        elif self.exp.condition == "outcome_accountability":
#            self += al.Text(content.outcome_accountability)
#
#        elif self.exp.condition == "control":
#            pass


# TODO: check for time and weekend etc. does not work. Check why. Seems to work now
class AccountabilityInterviewPage(al.UnlinkedDataPage):
    name = "interview_date"
    title = "Interview-Termin"

    def on_first_show(self):
        if self.exp.condition == "outcome_accountability":
            self += al.Text(content.outcome_accountability)
        elif self.exp.condition == "process_accountability":
            self += al.Text(content.process_accountability)
        else:
            pass

        lab1 = al.Text("Termin 1", align="right")

        date1 = al.RegEntry(
            placeholder="Datum (dd.mm.)",
            pattern=r"[0123]\d\.[01]\d\.?",
            name="date1",
            suffix="2022",
            match_hint="Bitte wählen Sie einen Tag innerhalb der nächsten zwei Wochen.",
        )

        time1 = al.RegEntry(
            placeholder="Zeit (hh:mm)",
            pattern=r"(([01]\d)|([89])):[0-6]\d",
            name="time1",
            match_hint="Bitte wählen Sie eine Zeit zwischen 8 und 18 Uhr.",
            suffix="Uhr",
        )

        lab2 = al.Text("Termin 2", align="right")

        date2 = al.RegEntry(
            placeholder="Datum (dd.mm.)",
            pattern=r"[0123]\d\.[01]\d\.?",
            name="date2",
            suffix="2022",
            match_hint="Bitte wählen Sie einen Tag innerhalb der nächsten zwei Wochen.",
        )

        time2 = al.RegEntry(
            placeholder="Zeit (hh:mm)",
            pattern=r"(([01]\d)|([89])):[0-6]\d",
            name="time2",
            match_hint="Bitte wählen Sie eine Zeit zwischen 8 und 18 Uhr.",
            suffix="Uhr",
        )

        lab3 = al.Text("E-Mailadresse", align="right")
        mail = al.RegEntry(
            placeholder="max.mustermann@uni-goettingen.de",
            force_input=True,
            name="interview_email",
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            width="medium",
        )

        self += al.Row(lab1, date1, time1, layout=[3, 5, 4])
        self += al.Row(lab2, date2, time2, layout=[3, 5, 4])
        self += al.Row(lab3, mail, layout=[3, 5])
        self += al.Alert(
            category="info",
            text=content.accountability3,
        )

    def validate(self):

        date1 = self.validate_date(self.date1.input)
        date2 = self.validate_date(self.date2.input)

        timecheck = self.validate_time()

        return all([date1, date2, timecheck])

    def _trim(self, s):
        # remove_leading_zero
        return re.sub(r"^0", "", s)

    def get_date(self, input):
        parts = input.split(".")
        day = int(self._trim(parts[0]))
        month = int(self._trim(parts[1]))

        return day, month

    def get_datetime(self, date, time):
        day, month = self.get_date(date)
        timeparts = time.split(":")

        if timeparts[0][0] == "0":
            timeparts[0] = timeparts[0].replace("0", "")

        hour, minute = int(timeparts[0]), int(timeparts[1])

        return datetime.datetime(2022, month, day, hour, minute)

    def validate_time(self):
        dtime1 = self.get_datetime(self.date1.input, self.time1.input)
        dtime2 = self.get_datetime(self.date2.input, self.time2.input)

        check1 = self.validate_hours(dtime1)
        check2 = self.validate_hours(dtime2)
        check3 = self.validate_timediff(dtime1, dtime2)

        return all([check1, check2, check3])

    def validate_timediff(self, dtime1, dtime2):
        timediff = max([dtime1, dtime2]) - min([dtime1, dtime2])
        min15 = datetime.timedelta(0, 60 * 15)

        if timediff < min15:
            msg = "Bitte stellen Sie sicher, dass Ihre Eingaben mindestens 15 Minuten auseinander liegen."
            self.exp.post_message(msg, level="danger")
            return False

        return True

    def validate_hours(self, dtime):

        if not dtime.minute in [0, 15, 30, 45]:
            msg = f"Bitte wählen Sie eine Startzeit zur vollen, halben oder viertel Stunde. Ihre Eingabe: {dtime.hour}:{dtime.minute}"
            self.exp.post_message(msg, level="danger")
            return False

        start = datetime.time(8)
        end = datetime.time(17, 45)

        t = datetime.time(dtime.hour, dtime.minute)

        if t < start or t > end:
            msg = f"{t.hour}:{t.minute} liegt nicht innerhalb der Bürozeiten. Bitte wählen Sie eine Zeit zwischen 8 Uhr und 17:45 Uhr."
            self.exp.post_message(msg, level="danger")
            return False

        return True

    def validate_date(self, date):

        day, month = self.get_date(date)
        datum = datetime.date(2022, month, day)
        print(datum)
        two_weeks = datetime.timedelta(days=14)
        today = datetime.date.today()

        if datum > (today + two_weeks):
            msg = f"{datum.strftime('%d.%m.%Y')} liegt nicht innerhalb der kommenden zwei Wochen."
            self.exp.post_message(msg, level="danger")
            return False

        if datum < today:
            msg = f"{datum.strftime('%d.%m.%Y')} liegt in der Vergangenheit."
            self.exp.post_message(msg, level="danger")
            return False

        if datum.weekday() > 4:
            msg = f"{datum.strftime('%d.%m.%Y')} liegt am Wochenende."
            self.exp.post_message(msg, level="danger")
            return False

        return True

class NoInterviewPage(al.Page):
    name = "no_interview_page"
    title = "Infos zum Interview"

    def on_exp_access(self):
        self += al.Text(text=content.no_acc, position="center")

class ManiCheckPrePage(al.Page):
    name = "mani_check_pre"
    title = "Ein paar Fragen"

    def on_first_show(self):
        self += al.Text(
            text="Bitte beantworten Sie noch die folgenden Fragen, bevor Sie mit den Schätzaufgaben beginnen ",
            align="center")
        self += al.Hline()
        self += al.SingleChoiceBar(
                "mein Vorgehen <br> 1", "2", "3", "4", "5", "6", "mein Ergebnis <br> 7",
                name=f"acc_pre", leftlab=content.acc_pre, force_input=True)
        self += al.Hline()
        self += al.SingleChoiceBar(
                "überhaupt nicht <br> 1", "2", "3", "4", "5", "6", " sehr <br> 7",
                name=f"justify", leftlab=content.justify_instr, force_input=True)
        if self.exp.condition == "outcome_accountability":
            self += al.Hline()
            self += al.SingleChoice(
                "mein Vorgehen", "mein Ergebnis", "beides gleichermaßen",
                name=f"interview_pre", leftlab=content.interview_pre, force_input=True)
        elif self.exp.condition == "process_accountability":
            self += al.Hline()
            self += al.SingleChoice(
                "mein Vorgehen", "mein Ergebnis", "beides gleichermaßen",
                name=f"interview_pre", leftlab=content.interview_pre, force_input=True)
        else:
            pass

class McStartPage(al.Page):
    name = "mc_start_page"
    title = "Bevor es losgeht!"
    def on_exp_access(self):
        self += al.Text(content.mc_begin, align="center")

@exp.member(of_section="ExpSection")
class InstructionSection(al.Section):
    allow_forward = True
    allow_backward = False
    allow_jumpfrom = False
    allow_jumpto = False

    def on_exp_access(self):
        self += InitialStressPage()


    def on_enter(self):
        if self.exp.condition == "process_accountability":
            self += AccountabilityInterviewPage()
            self += InstructionPage1()
            self += McStartPage()
            self += ManiCheckPrePage()

        elif self.exp.condition == "outcome_accountability":
            self += AccountabilityInterviewPage()
            self += InstructionPage1()
            self += McStartPage()
            self += ManiCheckPrePage()

        else:
            self += NoInterviewPage()
            self += InstructionPage1()
            self += McStartPage()
            self += ManiCheckPrePage()


@exp.member(of_section="ExpSection")
class MCQuestionnairePre2(al.Page):
    name = "epistemic_motivation"
    title = "Ein paar weitere Fragen"

    def on_exp_access(self):
        self += al.Text(content.epi_motiv_instr, align="center")
        self += al.Hline()
        choice_labels = [
            "trifft überhaupt nicht zu <br>1",
            "2",
            "3",
            "4",
            "trifft absolut zu <br> 5",
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv1,
            name="epistemic_motivation1",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv2,
            name="epistemic_motivation2",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv3,
            name="epistemic_motivation3",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv4,
            name="epistemic_motivation4",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv5,
            name="epistemic_motivation5",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv6,
            name="epistemic_motivation6",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv7,
            name="epistemic_motivation7",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv8,
            name="epistemic_motivation8",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv9,
            name="epistemic_motivation9",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.epi_motiv10,
            name="epistemic_motivation10",
            force_input=True,
            align="center",
        )

@exp.member(of_section="ExpSection")
class McQuestionnairePre3(al.Page):
    name = "systematic_information_processing"
    title = "Noch ein paar Fragen"

    def on_exp_access(self):
        self += al.Text(text="Auf dieser Seite finden Sie einige Aussagen die sich auf Ihre geplannte Vorgehensweise bei der "
                             "gleich folgenden Schätzaufgabe beziehen. Wählen Sie dazu die auf Sie passende Antwort durch"
                             " anklicken aus. Es gibt keine richtigen oder falschen Antworten. Überlegen Sie bitte "
                             "nicht lange und entscheiden Sie dann, wie stark Sie denken, dass das jeweils beschriebene Vorgehen "
                             "bei Ihrer eigenen Arbeitsweise vorhanden sein wird.", align="center")
        self += al.Hline()
        choice_labels = [
            "gar nicht <br> 1",
            "2",
            "3",
            "4",
            "sehr häufig <br> 5"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.systematic_information_processing1,
            name="systematic_information_processing1",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme absolut nicht zu <br> 1",
            "2",
            "3",
            "4",
            "stimme absolut zu <br> 5"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.systematic_information_processing2,
            name="systematic_information_processing2",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "nie <br> 1",
            "2",
            "3",
            "4",
            "immer <br> 5"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.systematic_information_processing3,
            name="systematic_information_processing3",
            force_input=True,
            align="center",
        )


@exp.member(of_section="ExpSection")
class MCQuestionnairePre4(al.Page):
    name = "MC_accountability"
    title = "Ein paar letzte Fragen noch bevor es losgeht."

    def on_exp_access(self):
        self += al.Text(text="Auf dieser Seite finden Sie einige Aussagen die sich auf den von Ihnen geplanten Fokus während der "
                             "nachfolgenden Aufgabe beziehen. Wählen Sie dazu die auf Sie passende Antwort durch "
                             "anklicken aus. Es gibt keine richtigen oder falschen Antworten. Überlegen Sie bitte nicht"
                             " lange und entscheiden Sie dann, wie stark die Aussagen jeweils für Sie persönlich"
                             "zutreffen.", align="center")
        self += al.Hline()
        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.MC_PA1,
            name="MC_PA_1",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            # *choice,
            # toplab=top_labels,
            leftlab=content.MC_OA1,
            name="MC_OA_1",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.MC_PA2,
            name="MC_PA_2",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            # *choice,
            # toplab=top_labels,
            leftlab=content.MC_OA2,
            name="MC_OA_2",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.MC_PA3,
            name="MC_PA_3",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            # *choice,
            # toplab=top_labels,
            leftlab=content.MC_OA3,
            name="MC_OA_3",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            leftlab=content.MC_PA4,
            name="MC_PA_4",
            force_input=True,
            align="center",
        )

        self += al.Hline()

        choice_labels = [
            "stimme überhaupt nicht zu <br> 1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "stimme vollkommen zu <br> 7"
        ]
        self += al.SingleChoiceBar(
            *choice_labels,
            # *choice,
            # toplab=top_labels,
            leftlab=content.MC_OA4,
            name="MC_OA_4",
            force_input=True,
            align="center",
        )


@exp.member(of_section="ExpSection")
class TaskCompletedPage(al.Page):
    name = "task_start_page"
    title = "Jetzt geht es los!"
    def on_exp_access(self):
        self += al.Text(content.task_begin, align="center")


# Task
# TODO: The attention checks do not work currently have to rewrite parts of this. works now
@exp.member(of_section="ExpSection")
class TaskSection(al.Section):
    allow_forward = True
    allow_backward = False
    allow_jumpfrom = False
    allow_jumpto = False

    def on_exp_access(self):
        with open(self.exp.path / "files/reisedaten.csv") as reisen_wahre_werte_data:
            csv_reader = csv.reader(reisen_wahre_werte_data, delimiter=";")
            reisen_werte = list(csv_reader)
            reisen_werte.pop(0)
            random.shuffle(reisen_werte)
        for i, r in enumerate(range(len(reisen_werte)), 1):
            page_name = f"task_page_{i}"
            image = self.exp.path / reisen_werte[r][16]
            Aufgabenpage = al.Page(name=page_name, title=f"Aufgabe {i}")

            img = al.Image(
                path=image,
                position="center",
                name=f"image_{i}_{reisen_werte[r][23]}",
                align="center",
                width="full",
            )

            Aufgabenpage += img

            Aufgabenpage += al.Value(img.name, name=f"task_trial_{i}")

            Aufgabenpage += al.Hline()

            if i == self.exp.first:
                screener = al.Text(
                    text=" Um zu zeigen, dass Sie diesen Text gelesen haben, "
                    "geben Sie bei dieser Schätzung bitte 0 Euro an. ",
                    name=f"first_screener",
                )

            else:
                screener = al.Text(text=" ", name=f"no_screener")

            reise_beschreibung1 = al.Text(
                text=(
                    f"Genießen Sie eine fantastische <b>{reisen_werte[r][2]}-tägige</b> Auszeit "
                    f"{reisen_werte[r][17]} <b>{reisen_werte[r][0]}.</b> <br> "
                    f"Lassen Sie sich im <b>{reisen_werte[r][7]}-Sterne</b> Hotel "
                    f"<b>{reisen_werte[r][5]}</b> "
                    f"von dem zuvorkommenden Personal verwöhnen."
                    f" {reisen_werte[r][18]} Fliegen Sie mit der Airline "
                    f"<b>{reisen_werte[r][4]}</b> in Ihren Traumurlaub."
                    + screener.text
                    + f"In "
                    f"<b>{reisen_werte[r][6]}</b> wartet {reisen_werte[r][20]} komfortable "
                    f"<b>{reisen_werte[r][9]}</b> auf Sie. Zusätzlich ist in diesem unschlagbaren "
                    f"Angebot {reisen_werte[r][22]} <b>{reisen_werte[r][8]}</b> beinhaltet, "
                    f"sodass Sie die Köstlichkeiten des Hauses "
                    f"probieren können und sich um nichts sorgen"
                    f" müssen. {reisen_werte[r][19]}"
                ),
                name=f"mask1_{i}",
            )

            reise_beschreibung2 = al.Text(
                text=(
                    f"Sie haben Lust auf eine <b>{reisen_werte[r][2]}-tägige</b> Auszeit "
                    f"{reisen_werte[r][17]} <b>{reisen_werte[r][0]}</b>? <br> "
                    f"Dann lassen Sie sich von der Airline <b>{reisen_werte[r][4]}</b> zu Ihrem"
                    f" Traumurlaub in <b>{reisen_werte[r][6]}</b> fliegen."
                    f" Hier wartet im <b>{reisen_werte[r][7]}-Sterne</b> Hotel "
                    f"<b>{reisen_werte[r][5]}</b> {reisen_werte[r][20]} bezaubernde"
                    f" <b>{reisen_werte[r][9]}</b> auf Sie."
                    + screener.text
                    + f"{reisen_werte[r][18]}"
                    f" Da in diesem Angebot {reisen_werte[r][22]} "
                    f"<b>{reisen_werte[r][8]}</b> inbegriffen ist, können Sie sich vollkommen auf "
                    f"Ihre Erholung konzentrieren. {reisen_werte[r][19]}"
                ),
                name=f"mask2_{i}",
            )
            reise_beschreibung3 = al.Text(
                text=(
                    f"Ein <b>{reisen_werte[r][2]}-tägiger</b> Aufenthalt "
                    f"{reisen_werte[r][17]} <b>{reisen_werte[r][0]}</b> wartet"
                    f" auf Sie. <br> "
                    f"Lassen Sie sich von der Airline <b>{reisen_werte[r][4]}</b> sicher "
                    f"in Ihren"
                    f" Traumurlaub in <b>{reisen_werte[r][6]}</b> fliegen."
                    f" Im <b>{reisen_werte[r][7]}-Sterne</b> Hotel "
                    f"<b>{reisen_werte[r][5]}</b> steht Ihnen {reisen_werte[r][20]} "
                    f" wunderschöne <b>{reisen_werte[r][9]}</b> zur Verfügung."
                    + screener.text
                    + f"{reisen_werte[r][18]}"
                    f" In diesem unvergleichlichen Angebot ist "
                    f"{reisen_werte[r][22]} <b>{reisen_werte[r][8]}</b> enthalten. Folglich können Sie"
                    f" die Sorgen des Alltags hinter sich lassen und sich auf einen unvergesslichen"
                    f" Urlaub konzentrieren. {reisen_werte[r][19]}"
                ),
                name=f"mask3_{i}",
            )
            reise_beschreibung4 = al.Text(
                text=(
                    f"Wenn Ihr Fernweh Sie nach <b>{reisen_werte[r][6]}</b> {reisen_werte[r][17]}"
                    f" <b>{reisen_werte[r][0]}</b> zieht, dann ist dieses Angebot perfekt für Sie "
                    f"geeignet. Kommen Sie im <b>{reisen_werte[r][7]}-Sterne</b> Hotel "
                    f"<b>{reisen_werte[r][5]}</b> zur Ruhe."
                    + screener.text
                    + f"Genießen Sie"
                    f" {reisen_werte[r][22]} im Angebot inbegriffene"
                    f" <b>{reisen_werte[r][8]}</b> und lassen Sie sich verwöhnen. Ihr "
                    f"Urlaub beginnt mit dem freundlichen Personal der Fluggesellschaft "
                    f"<b>{reisen_werte[r][4]}</b>. Im Hotel erwartet Sie {reisen_werte[r][20]} "
                    f"hinreißende <b>{reisen_werte[r][9]}</b>. {reisen_werte[r][18]} "
                    f"{reisen_werte[r][19]} Zögern Sie nicht und sichern Sie sich jetzt Ihre "
                    f"wohlverdiente <b>{reisen_werte[r][2]}-tägige</b> Auszeit."
                ),
                name=f"mask4_{i}",
            )
            reise_beschreibung5 = al.Text(
                text=(
                    f"<b>{reisen_werte[r][6]}</b> {reisen_werte[r][17]} <b>{reisen_werte[r][0]}</b> "
                    f"wartet auf Sie! Kommen Sie in den Genuss des <b>{reisen_werte[r][7]}-Sterne</b> "
                    f"Hotels <b>{reisen_werte[r][5]}</b>. {reisen_werte[r][18]}"
                    + screener.text
                    + f"Im Hotel "
                    f"steht für Sie {reisen_werte[r][22]} <b>{reisen_werte[r][8]}</b> und {reisen_werte[r][20]} "
                    f"herrliche  <b>{reisen_werte[r][9]}</b> bereit. Sie müssen sich lediglich von der"
                    f" Fluggesellschaft <b>{reisen_werte[r][4]}</b> in Ihren "
                    f"<b>{reisen_werte[r][2]}-tägigen</b> Traumurlaub fliegen lassen und entspannen. "
                    f"{reisen_werte[r][19]}"
                ),
                name=f"mask5_{i}",
            )
            reise_beschreibung6 = al.Text(
                text=(
                    f"Lassen Sie Ihre Seele {reisen_werte[r][17]} <b>{reisen_werte[r][0]}</b> "
                    f"baumeln. Erleben Sie einen unvergesslichen Urlaub in "
                    f"<b>{reisen_werte[r][6]}</b>. Das <b>{reisen_werte[r][7]}-Sterne</b> Hotel "
                    f"<b>{reisen_werte[r][5]}</b> wartet mit <b>{reisen_werte[r][8]}</b> auf Sie. "
                    f"{reisen_werte[r][18]}"
                    + screener.text
                    + f"{reisen_werte[r][19]} Zögern Sie nicht, sondern lassen Sie sich von der "
                    f"Fluggesellschaft <b>{reisen_werte[r][4]}</b> in Ihre "
                    f"<b>{reisen_werte[r][2]}-tägige</b> Auszeit fliegen. Vor Ort wartet "
                    f"{reisen_werte[r][20]} wunderschöne <b>{reisen_werte[r][9]}</b> auf Sie."
                ),
                name=f"mask6_{i}",
            )

            beschreibung = [
                reise_beschreibung1,
                reise_beschreibung2,
                reise_beschreibung3,
                reise_beschreibung4,
                reise_beschreibung5,
                reise_beschreibung6,
            ]
            reise_beschreibung = random.choice(beschreibung)

            Aufgabenpage += reise_beschreibung

            Aufgabenpage += al.Value(
                reise_beschreibung.name, name=f"description_trial_{i}"
            )

            Aufgabenpage += al.Value(screener.name, name=f"screener_trial{i}")

            Aufgabenpage += al.NumberEntry(
                name=f"estimation_{i}",
                toplab="<br>Bitte geben Sie Ihre Schätzung des Preises pro Person in Euro an:",
                ndecimals=2,
                position="center",
                align="center",
                suffix="€",
                force_input=True,
                width="medium",
            )
            Aufgabenpage += al.Value(reisen_werte[r][12], name=f"true_value_{i}")
            self += Aufgabenpage


@exp.member(of_section="ExpSection")
class FQSection(al.Section):
    allow_forward = True
    allow_backward = True
    allow_jumpfrom = False
    allow_jumpto = False

@exp.member(of_section="FQSection")
class TaskCompletedPage(al.Page):
    name = "task_completed_page"
    title = "Fast geschafft!"
    def on_exp_access(self):
        self += al.Text(content.task_complet)


@exp.member(of_section="FQSection")
class FinalStressPage(al.Page):
    name = "final_stress"
    title = "Abschlussfragen 1"

    def on_exp_access(self):
        self += al.Text(content.instruction_STAI, align="center")

        STAI_items = [
            ("STAI_S_01", "Ich bin ruhig."),
            ("STAI_S_02", "Ich fühle mich geborgen."),
            ("STAI_S_03", "Ich fühle mich angespannt."),
            ("STAI_S_04", "Ich bin bekümmert."),
            ("STAI_S_05", "Ich fühle mich ungezwungen."),
            ("STAI_S_06", "Ich bin aufgeregt."),
            ("STAI_S_07", "Ich bin besorgt, dass etwas schiefgehen könnte."),
            ("STAI_S_08", "Ich fühle mich ausgeruht."),
            ("STAI_S_09", "Ich bin beunruhigt."),
            ("STAI_S_10", "Ich fühle mich wohl."),
            ("STAI_S_11", "Ich fühle mich selbstsicher."),
            ("STAI_S_12", "Ich bin nervös."),
            ("STAI_S_13", "Ich bin zappelig."),
            ("STAI_S_14", "Ich bin verkrampft."),
            ("STAI_S_15", "Ich bin entspannt."),
            ("STAI_S_16", "Ich bin zufrieden."),
            ("STAI_S_17", "Ich bin besorgt."),
            ("STAI_S_18", "Ich bin überreizt."),
            ("STAI_S_19", "Ich bin froh."),
            ("STAI_S_20", "Ich bin vergnügt.")
        ]

        for item in STAI_items:
            # Text element to display the item text
            # item_text = al.Text(item[1], width="full")

            # SingleChoiceBar for user input
            item_choice = al.SingleChoiceBar(
                "überhaupt nicht <br> 1", "ein wenig <br> 2", "ziemlich <br> 3", "sehr <br> 4",
                name=f"final{item[0]}", leftlab=item[1], force_input=True)

            # Important: We use a Row element to arrange text and input horizontally
            self += al.Hline()
            self += item_choice

# TODO: add instruction text!
@exp.member(of_section="FQSection")
class ManiCheckPostPage(al.Page):
    name = "mani_check_post"
    title = "Abschlussfragen 2"

    def on_first_show(self):
        self += al.Text(text="Bitte beantworten Sie die folgenden Fragen", align="center")
        self += al.Hline()

        self += al.SingleChoiceBar(
                "mein Vorgehen <br> 1", "2", "3", "4", "5", "6", "mein Ergebnis <br> 7",
                name=f"acc_post", leftlab=content.acc_post, force_input=True)

        if self.exp.condition == "outcome_accountability":
            self += al.Hline()
            self += al.SingleChoice(
                "mein Vorgehen", "mein Ergebnis", "beides gleichermaßen",
                name=f"interview_post", leftlab=content.interview_post, force_input=True)

        elif self.exp.condition == "process_accountability":
            self += al.Hline()
            self += al.SingleChoice(
                "mein Vorgehen", "mein Ergebnis", "beides gleichermaßen",
                name=f"interview_post", leftlab=content.interview_post, force_input=True)

        else:
            pass


@exp.member(of_section="FQSection")
class SusCheckPage(al.Page):
    name = "suspicion_check"
    title = "Abschlussfragen 3"

    def on_exp_access(self):
        self += al.TextArea(
                toplab=content.suspicion_check,
                name="suspicion",
                force_input=True,
            )

        self += al.Hline()

        self += al.TextArea(
            toplab=content.comments,
            name="comments",
            force_input=False,
        )



# TODO: add instruction text!
@exp.member(of_section="FQSection")
class FinalQuestionnaire5(al.Page):
    name = "demographics"
    title = "Demographische Angaben"

    def on_exp_access(self):
        self += al.Text(text="Zum Abschluss haben wir noch einige Fragen zu Ihren demographischen Daten", align="center")

        self += al.Hline()

        choice_list = ["noch nicht ausgewählt", "weiblich", "männlich", "divers"]

        self += al.SingleChoiceList(
            leftlab="Bitte wählen Sie das Geschlecht aus, zu dem Sie sich zugehörig fühlen.",
            *choice_list,
            name="gender",
            force_input=True,
        )

        self += al.Hline()

        self += al.NumberEntry(
            leftlab="Bitte geben Sie Ihr Alter an.",
            suffix="Jahre",
            name="age",
            force_input=True,
        )

        self += al.Hline()

        self += al.TextEntry(
            leftlab="Bitte tragen Sie Ihren Studiengang ein.",
            force_input=True,
            name="course_of_studies",
        )



class SelectionPage(registration.SelectionPage):
    content = content.registration_selection_content

    pass


# TODO: Check which information we need.
class RegistrationPage(registration.RegistrationPage):
    content = content.registration_page_content



@exp.member(of_section="ExpSection")
class SelRegSection(al.Section):
    allow_forward = True
    allow_backward = True
    allow_jumpfrom = False
    allow_jumpto = False

    def on_exp_access(self):
        self += SelectionPage()
        self += RegistrationPage()

class FeedbackPage(al.Page):
    title = "Feedback"
    name = "feedback"

    def on_first_show(self):

        estimation = []
        true_values = []
        for x in range(1, 11):
            if self.exp.values[f"screener_trial{x}"] == "no_screener":
                estimation.append(
                    self.exp.values[f"estimation_{x}"]
                    )
                # print(self.exp.values[f"estimation_{x}"])
                true_values.append(
                    float(self.exp.values[f"true_value_{x}"].replace(",", "."))
                    )
            else:
                pass
            estimation_list = list(estimation)
            true_values_list = list(true_values)
            # print(estimation_list)
            # print(true_values_list)

            ape_values = []
        for z in range(len(estimation_list)):
            ape = (
                    abs(
                        (true_values_list[z] - estimation_list[z]) / true_values_list[z]
                    )
                    * 100
                )
            self += al.Value(ape, name=f"ape_{z}")
            ape_values.append(ape)

        ape_list = list(ape_values)
        mape = round((sum(ape_list)) / len(ape_list))

        all_data = self.exp.all_exp_data
        # print(all_data)
        data = [s for s in all_data if s["exp_session_id"] != self.exp.session_id]
        # print(data)
        data_finished = [r for r in data if r["exp_finished"] == True]
        # print(data_finished)
        all_mape = [q["mean_ape"] for q in data_finished]
        # print(all_mape)
        if len(all_mape) == 0:
            avg_mape = 0
            biggest_mape = 0
            smallest_mape = 0
        else:
            avg_mape = round((sum(all_mape)) / len(all_mape))
            biggest_mape = max(all_mape)
            smallest_mape = min(all_mape)

        self += al.Alert(
                category="info",
                text="Der <b>Mean Absolute Percentage Error (MAPE)</b> ist ein statistisches Maß,"
                " um die mittlere absolute prozentuale Abweichung zu bestimmen.<br>"
                "Der MAPE gibt hier konkret an, wie stark die geschätzten Preise von den "
                "wahren (=tatsächlichen) Preisen durchschnittlich abweichen. "
                "Bei perfekter Übereinstimmung mit den wahren Preisen beträgt der MAPE 0% (perfekte Übereinstimmung),"
                "umso stärker die Schätzungen vom wahren Preis abweichen desto größer wird der MAPE, es gibt dabei "
                "nach oben keine Grenze, der MAPE kann unendlich groß werden. <br>"
                "Es gilt also: Je kleiner der MAPE, desto akkurater ist die durchschnittliche "
                "Schätzung.",
            )

        self += al.Value(mape, name=f"mean_ape")
        self += al.Text(text=f"<b>Ihr MAPE beträgt: {mape}%</b>", name=f"mape", align="center", font_size="big")

        self += al.Text(text=f"<i>Der bisher niedrigeste MAPE (beste durchschnittliche Schätzungen) betrug: {smallest_mape}%</i>",
                        name=f"smallest_mape", align="center", font_size="big")

        self += al.Text(text=f"<i>Der durchschnittliche MAPE aller bisherigen Teilnehmer:innen betrug: {avg_mape}%</i>",
                        name=f"average_mape", align="center", font_size="big")

        self += al.Text(text=f"<i>Der bisher höchste MAPE (schlechteste durchschnittliche Schätzungen) betrug: {biggest_mape}%</i>",
                        name=f"biggest_mape", align="center", font_size="big")



@exp.member(of_section="ExpSection")
class FeedbackSection(al.Section):
    allow_forward = True
    allow_backward = False
    allow_jumpfrom = False
    allow_jumpto = False

    def on_exp_access(self):
        self += FeedbackPage()

if __name__ == "__main__":
    exp.run()
