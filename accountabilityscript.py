import time
import random
import re
import datetime

import jinja2

import alfred3 as al
import alfred3_interact as ali

from thesmuggler import smuggle

instr = smuggle("py/instructions.py")
consent = smuggle("py/consent.py")
screening = smuggle("py/screening.py")

exp = al.Experiment()


class InactivePage(al.Page):
    title = instr.mm_inactive_title

    def on_exp_access(self):

        ic = al.icon("user-check", size="80pt")
        self += al.VerticalSpace("50px")
        self += al.Html(ic, align="center")
        self += al.VerticalSpace("100px")
        self += al.Text(instr.mm_inactive_msg, align="center")


class FullPage(al.Page):
    title = instr.condition_full_page_title

    def on_exp_access(self):
        ic = al.icon("user-check", size="80pt")
        self += al.VerticalSpace("50px")
        self += al.Html(ic, align="center")
        self += al.VerticalSpace("100px")
        self += al.Text(instr.condition_full_page_msg, align="center")



class WaitingTimeoutPage(al.Page):
    title = "Wartezeit überschritten"
    name = "waiting_timeout"

    def on_exp_access(self):
        self += al.VerticalSpace("50px")
        self += al.Html(al.icon("user-clock", size="80pt"), align="center")
        self += al.VerticalSpace("100px")
        self += al.Text(
            "Ihre Wartezeit oder die Ihres Gegenübers ist abgelaufen. \
            Wir bitten um Verzeihung für die Unannehmlichkeiten. \
            Bitte melden Sie sich bei der Versuchsleitung unter \
            online-verhandlung@gmx.de.",
            align="center",
        )

class WaitingExceptionPage(al.Page):
    title = "Experiment abgebrochen"
    name = "waiting_exception"

    def on_exp_access(self):
        self += al.VerticalSpace("50px")
        self += al.Html(al.icon("user-clock", size="80pt"), align="center")
        self += al.VerticalSpace("100px")
        self += al.Text(
            "Das Experiment wurde abgebrochen. Vermutlich liegt das daran, dass \
            ihr Gegenüber zu lange warten musste. \
            Wir bitten um Verzeihung für die Unannehmlichkeiten. \
            Bitte melden Sie sich bei der Versuchsleitung unter \
            online-verhandlung@gmx.de.",
            align="center",
        )


@exp.setup
def setup(exp):
    roles = ["seller", "buyer"]

    exp.plugins.mm_male = ali.MatchMaker(
        *roles,
        exp=exp,
        id="mm_male",
        admin_pw="admin",
        active=True,
        inactive_page=InactivePage(name="inactive_page_male"),
    )

    if not exp.plugins.mm_male.admin_mode:
        exp.plugins.mm_female = ali.MatchMaker(
            *roles,
            exp=exp,
            id="mm_female",
            admin_pw="admin",
            active=True,
            inactive_page=InactivePage(name="inactive_page_female"),
        )
    

exp += al.ForwardOnlySection(name="main")


@exp.member(of_section="main")
class Welcome(al.Page):
    title = "Herzlich willkommen"

    def on_exp_access(self):
        self += al.Text(instr.welcome)

    def on_first_hide(self):
        if self.exp.client_data["client_device_type"] != "Desktop":
            self.exp.abort(
                reason="not_desktop",
                title="Desktop-Gerät erforderlich",
                msg="Für dieses Experiment benötigen Sie die volle Breite eines Laptop- oder Computerbildschirms. Bitte wechseln Sie das Gerät und starten Sie das Experiment neu.",
            )
        self.exp.plugins.mm_male._check_activation()
        self.exp.plugins.mm_female._check_activation()


exp.main += consent.InformedConsent(content=instr.informed_consent_content)

@exp.member(of_section="main")
class Screening(screening.ScreeningPage):
    email_screening = True
    register_on_hiding = True
    mortimer_url = "https://alfredo3.psych.bio.uni-goettingen.de/mortimer3"
    content = instr.screening_page_content


@exp.member(of_section="main")
class Demographics(al.Page):
    title = "Angaben zu Ihrer Person"

    def on_exp_access(self):
        self += al.Text(instr.demographics)

        self += al.VerticalSpace("20px")

        self += al.NumberEntry(
            leftlab=al.Label("Alter*", align="left"),
            force_input=True,
            name="age",
            suffix="Jahre",
            # width="wide",
        )

        self += al.VerticalSpace("20px")

        self += al.SingleChoiceButtons(
            al.icon("venus") + " weiblich",
            al.icon("mars") + " männlich",
            al.icon("transgender-alt") + " divers",
            leftlab=al.Label("Geschlecht*", align="left"),
            force_input=True,
            name="gender",
            # width="wide",
        )

        self += al.VerticalSpace("20px")

        self += al.TextEntry(
            leftlab=al.Label("Studienfach (falls zutreffend)", align="left"),
            name="study_programme",
            # width="wide",
        )

    def on_first_hide(self):
        if self.exp.values.get("gender") == 3:
            self.exp.abort(
                reason="gender_diverse",
                title=instr.demographics_diverse_page_title,
                msg=instr.demographics_diverse_page_msg,
                icon="user-check",
            )


alert_msg = """### Wichtig

Bitte nutzen Sie auf dieser Seite weder den **Aktualisieren**, noch den 
**Zurück** Button ihres Browsers. 

Durch Nutzung dieser Buttons kann es zu Fehlern in der Zuordnung von 
Gruppen kommen, so dass Sie das Experiment in diesem Fall möglicherweise 
nicht abschließen können.

Da der ordnungsgemäße Ablauf eines interaktiven Experiments von vielen
Faktoren abhängt, besteht generell das Risiko, dass es an manchen Stellen
nicht mehr weitergeht. Kontaktieren Sie in solchen Fällen bitte die
Versuchsleitung unter online-verhandlung@gmx.de.
"""


@exp.member(of_section="main")
class Match(ali.page.MatchingPage):

    title = "Verhandlungspartner:in wird gesucht"
    wait_msg = instr.matching
    wait_timeout = 60 * 10

    wait_timeout_page = WaitingTimeoutPage()
    wait_exception_page = WaitingExceptionPage()

    def wait_for(self):
        if self.exp.values.get("gender", None) == 1:  # male
            mm = self.exp.plugins.mm_female
        else:
            mm = self.exp.plugins.mm_male

        timeout_page = al.Page(title="Zuteilung fehlgeschlagen", name="nomatch_page")
        timeout_page += al.Text(instr.resultnomatch)

        # match to group
        group = mm.match_groupwise()
        self.exp.plugins.group = group

        # determine condition
        randomizer = al.ListRandomizer(
            ("process_accountability", 37),
            ("no_accountability", 3),
            exp=self.exp,
            id=group.group_id,
            abort_page=FullPage(name="full_page"),
            respect_version=True
        )

        self.exp.condition = randomizer.get_condition()
        return True
    
    def on_exp_access(self):
        super().on_exp_access()
        self += al.Alert(alert_msg, "info")


@exp.member(of_section="main")
class Success(al.Page):
    title = "Zuteilung erfolgreich"

    def on_first_show(self):

        self += al.VerticalSpace("30px")
        self += al.Text(":balloon: :tada: :balloon:", align="center", font_size=70)
        self += al.VerticalSpace("20px")

        self += al.Text(instr.resultmatch, align="center")


@exp.member(of_section="main")
class Prerole(al.Page):
    title = "Rollenbeschreibung"
    minimum_display_time = "30s"

    def on_first_show(self):
        self += al.Text(instr.prerole)

        if self.exp.plugins.group.me.role == "buyer":
            self += al.Text(instr.rolebuyer)
        else:
            self += al.Text(instr.roleseller)


@exp.member(of_section="main")
class Points(al.Page):

    responsive_width = "95%, 85%, 85%, 75%"

    title = "Wichtige Informationen zur Verhandlung und Vergütung"

    def on_first_show(self):

        self += al.VerticalSpace("30px")

        t = al.Text(instr.instrtable)

        r = self.exp.plugins.group.me.role

        tab1 = self.exp.read_csv_tolist(f"files/table1{r}.csv", delimiter=";")
        tab1_el = self.build_tab(tab1, row_layout=[6, 3, 3])

        tab2 = self.exp.read_csv_tolist(f"files/table2{r}.csv", delimiter=";")
        tab2_el = self.build_tab(tab2, row_layout=[4, 4, 4])

        r = al.Row(
            al.Stack(t, al.VerticalSpace("100px"), tab2_el, al.VerticalSpace("50px")),
            tab1_el,
            valign_cols=["top"],
        )

        r.layout.width_md = [12, 12]
        r.layout.width_xl = [7, 5]

        self += r

        self += al.Style(".Text-element p {margin-bottom: 0;}")

    def build_tab(self, tab, row_layout) -> al.Stack:
        stacklist = []
        for i, row in enumerate(tab):
            if i == 0:
                desc = al.Text(f"**{row[0]}**")  # print heading bold
                opt = al.Text(f"**{row[1]}**")
                pt = al.Text(f"**{row[2]}**")
            else:
                desc = al.Text(row[0])
                opt = al.Text(row[1])
                pt = al.Text(row[2])

            row_el = al.Row(desc, opt, pt, valign_cols=["top", "center", "center"])
            row_el.layout.width_sm = row_layout
            stacklist.append(row_el)
            if (i == 0) or (i % 5 == 0) and not i == 20:
                stacklist.append(al.Hline())
        return al.Stack(*stacklist)


@exp.member(of_section="main")
class Accountability(al.Page):
    title = "Interview-Termin"

    showif = {"exp_condition": "process_accountability"}

    def on_first_show(self):

        self += al.Text(instr.accountability1)
        self += al.Text(instr.accountability2)
        self += al.Text(instr.accountability3)

        lab1 = al.Text("Termin 1", align="right")

        date1 = al.RegEntry(
            placeholder="Datum (dd.mm.)",
            pattern=r"[0123]\d\.[01]\d\.?",
            name="date1",
            suffix="2021",
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
            suffix="2021",
            match_hint="Bitte wählen Sie einen Tag innerhalb der nächsten zwei Wochen.",
        )

        time2 = al.RegEntry(
            placeholder="Zeit (hh:mm)",
            pattern=r"(([01]\d)|([89])):[0-6]\d",
            name="time2",
            match_hint="Bitte wählen Sie eine Zeit zwischen 8 und 18 Uhr.",
            suffix="Uhr",
        )

        self += al.Row(lab1, date1, time1, layout=[3, 5, 4])
        self += al.Row(lab2, date2, time2, layout=[3, 5, 4])

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

        return datetime.datetime(2021, month, day, hour, minute)

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
        datum = datetime.date(2021, month, day)

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


class FixedPie(al.Page):

    responsive_width = "85%, 85%, 85%, 55%"
    prefix_element_names = True

    def on_first_show(self):

        r = self.exp.plugins.group.me.role
        n = 1 if self.vargs.get("pre_negotiation", False) else 2
        text = getattr(instr, f"fixedpie{r}{n}")

        self += al.Text(text)

        tab = self.exp.read_csv_tolist(f"files/table1{r}.csv", delimiter=";")
        for i, row in enumerate(tab):
            if i == 0:
                continue

            guess = al.NumberEntry(
                leftlab=row[1],
                rightlab=f"Sie erhalten **{row[2]} Punkte**",
                placeholder="Ihr Gegenüber erhält",
                name=row[3],
                suffix="Punkte",
                force_input=True,
                min=0,
                layout=[2, 6, 4],
            )

            if i == 1 or ((i - 1) % 5 == 0):
                self += al.Hline()
                self += al.Text(f"**{row[0]}**", align="center", width="full")

            self += guess


exp.main += FixedPie(name="fixedpie1", title="Vor der Verhandlung", vargs={"pre_negotiation": True})

@exp.member(of_section="main")
class NegotiationInstructions(al.Page):
    title = "Auf der nächsten Seite beginnt die Verhandlung"

    def on_exp_access(self):
        self += al.Text(instr.negotiationinstr)

    def on_first_hide(self):
        self += al.Value(True, name="ready")



@exp.member(of_section="main")
class Wait(ali.WaitingPage):
    title = "Wartezimmer"
    wait_msg = "Bitte warten Sie, bis Ihr:e Verhandlungspartner:in bereit ist.\nDie maximale Wartezeit beträgt 10 Minuten."
    wait_timeout = 60 * 10

    wait_timeout_page = WaitingTimeoutPage()
    wait_exception_page = WaitingExceptionPage()

    def wait_for(self):
        you = self.exp.plugins.group.you
        fixedpie_complete = you.values.get("ready", False)

        if self.exp.plugins.group.me.role == "buyer":
            self.exp.plugins.group.shared_data["end"] = time.time() + 60 * 20
            return fixedpie_complete

        else:
            negotiation_end_time = self.exp.plugins.group.shared_data.get("end", False)
            return fixedpie_complete and negotiation_end_time
    
    def on_exp_access(self):
        super().on_exp_access()
        self += al.Alert(alert_msg, "info")

class SubmitNegotiation(al.SubmittingButtons):
    def added_to_page(self, page):
        super(al.SubmittingButtons, self).added_to_page(page)
        self._js_code = []
        js = self.exp.subpath("js/negotiation_submit.txt").read_text()
        self.add_js(js)


class SubmitNegotiation2(al.SubmittingButtons):
    def added_to_experiment(self, experiment):
        super().added_to_experiment(experiment)
        t = self.exp.subpath("js/negotiation_submit.txt").read_text()
        self.js_template = jinja2.Template(t)


@exp.member(of_section="main")
class negotiation(al.AutoForwardPage):

    title = "Verhandlung"
    timeout = "20m"
    responsive_width = "95%, 95%, 95%, 85%"
    prefix_element_names = True

    original_labels = {}
    original_styles = {}

    _partner_has_moved = False
    _forward_by_timeout = False

    def on_first_show(self):
        label_kwargs = {"button_style": "", "leftlab": "Ihre Punkte"}

        self += al.JavaScript(path="js/update_styles.txt")

        r = self.exp.plugins.group.me.role
        tab = self.exp.read_csv_todict(f"files/table1{r}.csv", delimiter=";")
        data = {}
        for i, row in enumerate(tab):
            newpart = row["Verhandlungsgegenstände"]
            if newpart:
                part = newpart
            if not part in data:
                data[part] = {}
            data[part].update({row["Optionen"]: row["Punktwerte"]})

        btn_kwargs = {}
        elnames = ("interest", "stereo", "warranty", "delivery_time")
        for label, elname in zip(data, elnames):
            btn_kwargs[elname] = {
                "leftlab": f"**{label}**",
                "name": elname,
                "button_style": "btn-offer",
            }

        update = al.Button(
            text=f"{al.icon('sync')} Aktualisieren",
            func=self.get_button_styles,
            submit_first=True,
            button_style="btn-danger",
            followup="custom",
            align="center",
            custom_js="conduct_update(data);",
        )

        explanation = al.Text(
            "Die Anzeige wird alle 10 Sekunden automatisch aktualisiert. Wenn Sie mit dem \
            Verhandlungsergebnis einverstanden sind, wählen Sie 'Bereit' unter dem Chatfenster \
            aus. Erst dann kann die Verhandlung beschlossen werden."
        )

        legend = al.ButtonLabels(
            "Übereinstimmende Auswahl",
            "Ihre Auswahl",
            "Auswahl Ihres Gegenübers",
            "Keine Auswahl",
            button_style=["btn-success", "btn-dark", "btn-warning", "btn-outline-dark"],
            toplab="Bedeutung der Farben",
        )

        t = self.exp.plugins.group.shared_data["end"]
        countdown = al.CountDown.tilltime(t=t, align="center", font_size="huge")

        stack_elements = [
            countdown,
            al.VerticalSpace("10px"),
            explanation,
            legend,
            al.VerticalSpace("30px"),
            update,
            al.VerticalSpace("30px"),
        ]  # initialize list with update button

        for d, kwargs in zip(data.values(), btn_kwargs.values()):
            lab = al.ButtonLabels(*list(d.values()), **label_kwargs)
            entry = al.SingleChoiceBar(*list(d), **kwargs)
            line = al.Hline()

            stack_elements += [lab, entry, line]

        del stack_elements[-1]  # delete last line

        ready = al.SingleChoice(
            "Bereit",
            "Nicht bereit",
            default=2,
            name="ready",
            align="center",
            toplab="Geben Sie hier an, ob Sie bereit sind, fortzufahren.",
        )

        right_side = al.Stack(*stack_elements)

        nickname = "Verkäufer:in" if r == "seller" else "Käufer:in"
        chat = self.exp.plugins.group.chat(height="500px", nickname=nickname, you_label=" (Sie)")

        vspace = al.VerticalSpace("30px")

        oldal = self.exp.alfred_version == "2.1.0b2"
        submitbtn = SubmitNegotiation if oldal else SubmitNegotiation2
        submit = submitbtn(
            f"{al.icon('check-circle', size='3rem')}<br>Verhandlungsergebnis bestätigen<br>(zur nächsten Seite)",
            f"{al.icon('times', size='3rem')}<br>Verhandlung abbrechen<br>(zur nächsten Seite)",
            name="submit",
            button_style=["btn-dark", "btn-dark"],
            width="medium",
        )

        left_side = al.Stack(
            al.VerticalSpace("30px"),
            al.Text(f"Sie sind {nickname}", font_size="large", align="center"),
            al.Text("Hier können Sie mit Ihrem Gegenüber chatten.", align="center"),
            chat,
            vspace,
            submit,
            ready,
        )

        r = al.Row(right_side, left_side)
        r.layout.width_sm = [12, 12]
        r.layout.width_xl = [7, 5]
        self += r

        # load button styles repeatedly throughout the negotiation
        self += al.RepeatedCallback(
            func=self.get_button_styles,
            interval=10,
            followup="custom",
            custom_js="conduct_update(data); move_if_partner_has(data);",
            submit_first=True,
        )

        # load button styles one time upon every reload of the page
        self += al.Callback(
            func=self.get_button_styles, followup="custom", custom_js="conduct_update(data);"
        )

        url = self.exp.ui.add_callable(self.get_button_styles)
        self += al.JavaScript(
            code=f"""$('input[type=radio]').click(function(){{
                var data = $("#form").serializeArray();
                $.post("{self.exp.ui.set_page_data_url}", data);
                $.get('{url}', function(data){{
                    conduct_update(data); move_if_partner_has(data);
                }})
            }});"""
        )

        self += al.Style(code=".btn-offer {border-color: black;}")

        self += al.HideNavigation()

    def get_button_styles(self):
        vals = self.exp.plugins.group.you.values
        n = type(self).__name__

        styles = {}

        for negotiation_part in ["interest", "stereo", "warranty", "delivery_time"]:
            elname = n + "_" + negotiation_part
            el = getattr(self, elname)
            my_choice = el.input
            your_choice = vals.get(elname)

            el_styles = {}

            for choice in el.choices:

                if choice.value not in (my_choice, your_choice):
                    el_styles[choice.label_id] = "btn-outline-dark"

                elif choice.value == my_choice and my_choice == your_choice:
                    el_styles[choice.label_id] = "btn-success"

                elif choice.value == my_choice:
                    el_styles[choice.label_id] = "btn-dark"

                elif choice.value == your_choice:
                    el_styles[choice.label_id] = "btn-warning"

            styles[elname] = el_styles

        self._partner_has_moved = vals.get("negotiation_moved", False)

        return [styles, self._partner_has_moved]

    def on_first_hide(self):
        self += al.Value(True, name="moved")
        self += al.Value(self.calculate_points(), name="points")
        self += al.Value(self.calculate_tickets(), name="lottery_tickets")
        self += al.Value(self._forward_by_timeout, name="timeout")

    def calculate_points(self):
        if not self.agreement_reached():
            return 0

        r = self.exp.plugins.group.me.role
        tab = self.exp.read_csv_tolist(f"files/table1{r}.csv", delimiter=";")

        points = {}
        varnames = ["interest", "stereo", "warranty", "delivery_time"]
        for i, row in enumerate(tab):
            if i == 0:
                continue

            for n in varnames:
                if row[3].startswith(n):
                    if not n in points:
                        points[n] = [None]
                    points[n].append(row[2])

        achieved = []
        for n in varnames:
            el = getattr(self, "negotiation_" + n)
            won = points[n][int(el.input)]
            achieved.append(int(won))

        return sum(achieved)

    def calculate_tickets(self):
        points = self.calculate_points()
        return max([int(points / 1000), 1])

    def agreement_reached(self):
        if self._forward_by_timeout:
            return False

        vals = self.exp.plugins.group.you.values
        submit = "negotiation_submit"
        if vals.get(submit) == 2 or self.exp.values.get(submit) == 2:
            return False

        n = type(self).__name__
        equal = []
        for negotiation_part in ["interest", "stereo", "warranty", "delivery_time"]:
            elname = n + "_" + negotiation_part
            el = getattr(self, elname)
            my_choice = el.input
            your_choice = vals.get(elname)

            equal.append(my_choice == your_choice)
            equal.append(my_choice is not None)
            equal.append(your_choice is not None)

        if all(equal):
            return True

        return False

    def validate(self):
        if self.exp.values.get("negotiation_submit") == 2 or self._forward_by_timeout:
            return True
        elif self._partner_has_moved:
            return True

        if self.negotiation_ready.input != 1:
            self.exp.post_message(
                "Sie können die Verhandlung erst beenden, wenn Sie angeben, dass Sie bereit sind.",
                level="info",
            )

        if self.agreement_reached():
            vals = self.exp.plugins.group.you.values
            if vals.get("negotiation_ready") != 1:
                self.exp.post_message("Ihr Gegenüber ist noch nicht bereit.", level="info")
                return False
            return True

        self.exp.post_message(
            "Ihre Eingaben stimmen nicht mit den Eingaben ihres Gegenübers überein oder Sie haben nicht alle Verhandlunsggegenstände bearbeitet. Wenn Sie die Verhandlung abbrechen wollen, klicken Sie bitte auf 'Verhandlung abbrechen'.",
            level="danger",
        )
        return False

    def on_timeout(self):
        super().on_timeout()
        self._forward_by_timeout = True


@exp.member(of_section="main")
class WaitForSubmission(ali.WaitingPage):
    title = "Wartezimmer"
    wait_msg = "Bitte warten Sie, bis Ihr:e Verhandlungspartner:in bereit ist.\nDie maximale Wartezeit beträgt 10 Minuten."
    wait_timeout = 60 * 10

    wait_timeout_page = WaitingTimeoutPage()
    wait_exception_page = WaitingExceptionPage()

    def wait_for(self):
        you = self.exp.plugins.group.you
        your_submit = you.values.get("negotiation_submit", None)
        moved = you.values.get("negotiation_moved", False)
        return (your_submit is not None) or moved

    def on_exp_access(self):
        super().on_exp_access()
        self += al.Alert(alert_msg, "info")

@exp.member(of_section="main")
class negotiation_result(al.Page):
    title = "Verhandlungsergebnis"

    def on_first_show(self):

        agreement = self.exp.negotiation.agreement_reached()
        self += al.Value(agreement, name="negotiation_agreement_reached")

        tk = self.exp.values.get("negotiation_lottery_tickets")
        points = self.exp.values.get("negotiation_points")

        if self.exp.negotiation._forward_by_timeout:
            msg = "Sie wurden nach Ende der Verhandlungszeit automatisch weitergeleitet. \
                Daher gilt die Verhandlung als 'ohne Einigung beendet'."
            self.exp.post_message(msg, level="info")

        elif self.exp.negotiation._partner_has_moved:
            self.exp.post_message(
                "Sie wurden automatisch weitergeleitet, da Ihr Gegenüber die Verhandlung beendet hat.",
                level="info",
            )


        if agreement:
            self += al.Text("🤝", font_size=70, align="center")
            self += al.VerticalSpace("20px")
            self += al.Text(
                instr.negotiation_success.format(points=points, tickets=tk), align="center"
            )
        else:
            self += al.Text(":no_entry:", font_size=70, align="center")
            self += al.VerticalSpace("20px")
            self += al.Text(instr.negotiation_impasse)
        

        self += al.VerticalSpace("50px")
        forward_text = al.Text(f"Weiter zu den Abschlussfragen \
                {al.icon('chevron-circle-right', size='30pt')}", font_size="30pt")
        self += al.SubmittingButtons(
            forward_text, 
            name="forward_negotiation", 
            button_style="btn-success", 
            button_round_corners=False
        )
        self += al.HideNavigation()


exp.main += FixedPie(name="fixedpie2", title="Nach der Verhandlung", vargs={"pre_negotiation": False})


@exp.member(of_section="main")
class negotiation_questions(al.Page):
    title = "Fragebogen zur Verhandlung"

    def on_exp_access(self):

        self += al.Text(
            "Bitte geben Sie in den folgenden Fragen an, wie sehr Sie der jeweiligen Aussage zustimmen.",
            align="center",
        )

        choices = list(range(1, 7))

        for i in range(1, 5):
            self += al.VerticalSpace("40px")
            lab = getattr(instr, f"finalq{i}")
            self += al.SingleChoiceBar(
                *choices,
                toplab=lab,
                leftlab="gar nicht",
                rightlab="voll und ganz",
                name=f"finalq{i}",
                force_input=True,
            )

        if self.exp.condition == "process_accountability":
            for i in range(6, 7):
                self += al.VerticalSpace("40px")
                lab = getattr(instr, f"finalq{i}accountability")

                self += al.SingleChoiceBar(
                    *choices,
                    toplab=lab,
                    leftlab="gar nicht",
                    rightlab="voll und ganz",
                    name=f"finalq{i}",
                    force_input=True,
                )


@exp.member(of_section="main")
class svo(al.Page):
    title = "Ein paar weitere Fragen"

    def on_exp_access(self):
        self += al.Text(instr.svo)
        self += al.Hline()
        self += al.VerticalSpace("30px")

        labme_args = {"button_style": "", "leftlab": "Sie erhalten"}
        labyou_args = {"button_style": "", "leftlab": "Gegenüber erhält"}
        btn_labs = [al.icon("check")] * 9
        btn_args = {"force_input": True}

        me_ex = [30, 35, 40, 45, 50, 55, 60, 65, 70]
        you_ex = [80, 70, 60, 50, 40, 30, 20, 10, 0]

        self += al.Text("**Beispiel**", align="center")
        self += al.ButtonLabels(*me_ex, **labme_args)
        self += al.SingleChoiceBar(
            *btn_labs,
            **btn_args,
            name=f"svo_example",
            leftlab=" ",
            disabled=True,
            default=5,
            button_style="btn-outline-primary",
        )
        self += al.ButtonLabels(*you_ex, **labyou_args)
        self += al.Hline()

        me1 = [85] * 9
        you1 = [85, 76, 68, 59, 50, 41, 33, 24, 15]

        me2 = [85, 87, 89, 91, 93, 94, 96, 98, 100]
        you2 = [15, 19, 24, 28, 33, 37, 41, 46, 50]

        me3 = [50, 54, 59, 63, 68, 72, 76, 81, 85]
        you3 = [100, 98, 96, 94, 93, 91, 89, 87, 85]

        me4 = [50, 54, 59, 63, 68, 72, 76, 81, 85]
        you4 = [100, 89, 79, 68, 58, 47, 36, 26, 15]

        me5 = [100, 94, 88, 81, 75, 69, 63, 56, 50]
        you5 = [50, 56, 63, 69, 75, 81, 88, 94, 100]

        me6 = [100, 98, 96, 94, 93, 91, 89, 87, 85]
        you6 = [50, 54, 59, 63, 68, 72, 76, 81, 85]

        me = [me1, me2, me3, me4, me5, me6]
        you = [you1, you2, you3, you4, you5, you6]

        for i in range(6):
            self += al.ButtonLabels(*me[i], **labme_args)
            self += al.SingleChoiceBar(*btn_labs, **btn_args, name=f"svo{i}", leftlab=" ")
            self += al.ButtonLabels(*you[i], **labyou_args)
            if i != 5:
                self += al.Hline()


@exp.member(of_section="main")
class Registration(al.UnlinkedDataPage):
    title = "Abschließende Dateneingabe"

    def on_first_show(self):

        screening_mail = self.exp.exp_screening.screening_email.input

        self += al.Text(instr.registration)

        self += al.VerticalSpace("30px")

        self += al.TextEntry(
            placeholder="Vorname*", force_input=True, name="first_name", width="medium"
        )
        self += al.TextEntry(
            placeholder="Nachname*", force_input=True, name="last_name", width="medium"
        )
        self += al.RegEntry(
            placeholder="Email*",
            force_input=True,
            name="email",
            default=screening_mail,
            disabled=True,
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            width="medium",
        )
        self += al.NumberEntry(
            placeholder="Matrikelnummer (für Studierende)", width="medium", name="matriculation_number"
        )

        tickets = self.exp.values.get("negotiation_lottery_tickets")
        self += al.Value(tickets, name="lottery_tickets")


@exp.as_final_page
class Debriefing(al.Page):
    title = "Aufklärung über das Ziel der Studie"

    def on_exp_access(self):
        self += al.Text(instr.debriefing)

        self += al.Hline()
        self += al.Text("## Für Nutzer:innen von Survey Circle", align="center")
        self += al.Text("Der Code lautet", align="center")
        self += al.VerticalSpace("10px")
        self += al.Text("1MS7-B83W-22E6-XBEQ", align="center", font_size=20)
        self += al.VerticalSpace("10px")
        self += al.Text("[Hier klicken und Survey Code mit einem Klick einlösen](https://www.surveycircle.com/1MS7-B83W-22E6-XBEQ)", align="center", font_size=20)


if __name__ == "__main__":
    exp.run()
