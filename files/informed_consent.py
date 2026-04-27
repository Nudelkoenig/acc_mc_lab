"""Informed consent page
author: Christian Treffenstädt
updated: 2021-04-27
"""

import alfred3 as al

##########################
# - Section 2: Content - #
##########################

informed_consent_content = dict(
    experimenter_in_charge="",
    experimenter_in_charge_email="",
    privacy_officer="",
    privacy_officer_email="",
    study_email="",
    consent_accept_label="Accept",
    consent_reject_label="Reject",

    # language=HTML
    title=(
        "<div align='center' style='font-size: 1.6em; margin-bottom: 25px;'>Informed "
        "Consent<div>"
    ),

    statustext="",

    # language=HTML
    introduction=(
        "This are introductory sentences to the informed consent"
    ),

    # language=HTML
    experiment_info=
    """This text should provide specific information about the experiment.    
    """,

    # language=HTML
    anonymity_info=
    """This text should provide specific information about the anonymity of experimental 
    data.     
    """,

    # language=HTML
    personal_data_info=
    """This text should provide specific information about the collection and use of any
    personal information.
    
    """,

    # language=HTML
    data_disclaimer=
    """This text should provide general information about our handling of the collected
    experimental data.
    
    """,

    # language=HTML
    consent=
    """<span style="font-size: large; "><b>Consent Regarding Data Collection and 
    Processing</b></span><br><br>This text should provide the actual consent text, 
    which must contain specific information required by law.<br><br>The person 
    responsible for this data collection is: <br><br> <b>{experimenter_in_charge} 
    ({experimenter_in_charge_email})</b>.<br><br>The responsible privacy officer is: 
    {privacy_officer}.<br><br><b>{privacy_officer_email}</b><br><br>I have no further 
    questions<br><br><b>Note:</b> If you click on 'Accept', the experiment will start 
    immediately. Click 'Reject' to finish the experiment without your personal data 
    being recorded.""",

    consent_reject_title="Consent: Rejected",
    consent_reject_icon="times-circle",
    # language=HTML
    consent_reject_message=
    """You have aborted the experiment.
    <br><br>
    You can close this page now.
    <br><br>
    If you have any questions, please mail us at <span style="color: blue; ">{study_email}</span>
    """
)


#################################
# - Section 3: Custom classes - #
#################################


class InformedConsent(al.Page):
    """Custom question to document participants' consent"""

    content = None

    def __init__(
            self,
            content=None,
            **kwargs
    ):
        super(InformedConsent, self).__init__(**kwargs)

        if content is not None:
            self.content = content

        if self.content is None:
            self.content = informed_consent_content

        if "title" not in kwargs:
            self.title = self.content["title"]

    def on_exp_access(self):

        # Disable all forward type buttons
        self += al.Style("#forward_button {display: none;}")
        self += al.Style("#finish_button {display: none;}")

        self += al.Text(self.content["introduction"])
        self += al.Text(self.content["experiment_info"])
        self += al.Text(self.content["anonymity_info"])
        self += al.Text(self.content["personal_data_info"])
        self += al.Text(self.content["data_disclaimer"])

        self += al.Hline()

        consent_text = self.content["consent"].format(
            experimenter_in_charge=self.content["experimenter_in_charge"],
            experimenter_in_charge_email=self.content["experimenter_in_charge_email"],
            privacy_officer=self.content["privacy_officer"],
            privacy_officer_email=self.content["privacy_officer_email"]
        )

        self += al.Text(consent_text)

        self += al.SubmittingButtons(
            self.content["consent_reject_label"],
            self.content["consent_accept_label"],
            name="consent",
            align="center",
            width="wide",
            button_style="btn-dark",
        )

    def on_each_hide(self):
        if self.consent.input is None:
            return

        elif self.consent.input == 2:
            self.exp.session_status = 'Informed Consent: Accepted'

        elif self.consent.input == 1:
            self._experiment.session_status = 'Informed Consent: Rejected'

            self.exp.abort(
                reason=(
                    "Informed Consent: The participant has rejected the informed "
                    "consent statement. Aborting the Session."
                ),
                title=self.content["consent_reject_title"],
                icon=self.content["consent_reject_icon"],
                msg=self.content["consent_reject_message"].format(
                    study_email=self.content["study_email"])
            )