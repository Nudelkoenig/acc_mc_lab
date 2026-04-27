"""Custom classes for participant screening and filtering in Alfred 3

author: Christian Treffenstädt
updated: 2021-05-11

Dev notes:

Currently, there are three possible use cases I can think of:

1. The most common use case: Screening participants and participant
   logging within the same experiment. Participants are screened at the
   beginning of an experiment and their participation is either logged
   instantaneously (on hiding of the screening page) or on one of the
   following pages > Implementation finished

2. Participant logging without screening. This will occur often, as we
   might conduct an experiment for which screening is not necessary but
   we want to log participation for future screening purposes.

3. Screening without logging. There are two scenarios in which the
   screening page might be used without participation logging. The more
   common scenario involves using on-page screening elements but
   deactivating mail-based screening altogether. The less common
   scenario would involve mail-based screening without participant
   logging. This might be useful for small pilot studies, but should not
   occur often.

As a result, mail-based filtering on the screening page, on-page
screening elements, and participation checks should be implemented
independently of each other. Nonetheless, all methods should work together
if they are activated.

"""

import alfred3 as al
from alfred3.exceptions import AlfredError
import requests

screening_page_content = dict(
    title="Participant Screening",
    screening_info=(
        "A general information about participant exclusion and the relevant criteria. "
    ),
    email_instruction="Please enter your email address",
    email_pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    email_match_hint="Please enter a valid email address.",
    data_protection_info=(
        "An information on storage and use of the collected email address."
    ),
    exclusion_title="You have been excluded!",
    exclusion_icon="times-circle",
    exclusion_message="Sorry, but you can not participate in this experiment.",
)


class ScreeningPage(al.Page):
    """
    Provides different options to filter participants.

    The *ScreeningPage* can be added to an experiment to filter
    participants in three ways:

        * Users can add input elements, preferably through the page's
          :meth:`alfred3.page.Page.on_first_show` method, and filter
          participants based on their answers to these screening elements
          by overriding :meth:`.validate_screening_elements`. The
          experiment session will then be aborted based on the methods
          return value.
        * If users have access to an instance of mortimer (version 0.8.2
          or higher), they can use mortimer's participation check feature
          (:ref:`https://github.com/ctreffe/mortimer/wiki/Check-participation`)
          to filter participants based on their recorded participation to
          the current and other experiments.
        * Users can pass lists with email addresses against which the
          participant's email is compared. If the email is found on any of
          the lists, the experiment session will be aborted.

    All three methods work both independently and in combination with any
    of the other methods. See the example section for further information.

    Args:
        email_screening (bool): If *True* a
            :class:`alfred3.element.input.RegEntry` element and a data
            protection disclaimer are added on the top of the page,
            prompting the participant to enter an email address for
            which both mortimer's participation check or the comparison
            against email address lists can be performed. Defaults to
            *True*.
        part_check_filter (dict): Contains nested dictionaries with the
            necessary information to perform a participation check with
            mortimer. The dictionary keys can be freely chosen and
            function as labels which are used in log entries regarding the
            screening results. A nested dictionary must contain an
            'exp_id' key with a valid exp_id value. To perform a version
            specific participation check the dictionary may also contain
            an 'exp_version' key with a valid version value.
        mail_list_filter (dict): Contains lists of email addresses (as
            strings). The dictionary keys can be freely chosen and
            function as labels which are used in log entries regarding the
            screening results.
        mortimer_url (str): The URL to a mortimer instance v0.8.2 or
            newer. The email screening feature of this page will access
            mortimer's */participation* route if a participant check
            and/or registration is performed.
        content (dict): Contains customized texts and configurations for
            the page. Defaults to a dictionary with minimal examples.
        repeated_participation (bool): Only relevant if *email_screening*
            is *True*. If this is set to *False* users are prevented from
            repeatedly participating in the current experiment by adding
            the current experiment and version to the *part_check_filter*.
            Other versions of the experiment need to be added manually.
        register_on_hiding (bool): If set to *True* the participation for
            the specified email address will be registered with mortimer
            on leaving the page in any direction. Defaults to *True*. See
            the examples below on how to postpone the participation
            registration to a later page in the experiment.

    Examples:

        1. Participation check with immediate participation registration

        2. Email list filtering with immediate participation registration

        3. Screening elements example without participation registration

        4. Screening elements and participation check with postponed
           participation registration

        5. Immediate participation registration without screening

        6. Postponed participation registration without screening

    Todo: Add examples.

    Todo: Currently, the screening page should be added to a forward only
          section to correctly enforce input element validation. In the
          next version of this module, the screening process should be
          activated with an alfred3 action button. This offers three
          improvements: First, this will free up the on_hiding hook since
          the current code can be moved to a callback function for the
          button. Second, the forward button could be specifically
          deactivated on the screening page but the backward button could
          still be shown, allowing users to go back to the previous page
          but not to continue to the experiment without validation even
          if the screening page is added to a section without validation.
          This will also prevent the duplicate match hints.

    """

    name = "exp_screening"
    prefix_element_names = False
    email_screening = True
    part_check_filter = None
    mail_list_filter = None
    mortimer_url = None
    content = None
    repeated_participation = False
    register_on_hiding = True

    def __init__(
        self,
        email_screening: bool = None,
        mail_list_filter: dict = None,
        part_check_filter: dict = None,
        mortimer_url: str = None,
        content: dict = None,
        repeated_participation: bool = None,
        register_on_hiding: bool = None,
        **kwargs,
    ):
        if self.name != "exp_screening":
            raise ValueError(
                "Property 'name' cannot be set for a ScreeningPage. For referencing "
                "purposes, the ScreeningPage is always named 'exp_screening'."
            )

        if "name" in kwargs:
            raise ValueError(
                "Argument 'name' cannot be set for a ScreeningPage. For referencing "
                "purposes, the ScreeningPage is always named 'exp_screening'."
            )

        if self.prefix_element_names:
            raise ValueError(
                "Property 'prefix_element_names' cannot be set for a ScreeningPage, as"
                "prefixes are added automatically."
            )

        if "prefix_element_names" in kwargs:
            raise ValueError(
                "Argument 'prefix_element_names' cannot be set for a ScreeningPage, as"
                "prefixes are added automatically."
            )

        super(ScreeningPage, self).__init__(**kwargs, name="exp_screening")

        if email_screening is not None:
            self.email_screening = email_screening

        if self.mail_list_filter is None:
            self.mail_list_filter = {}

        if mail_list_filter is not None:
            self.mail_list_filter = mail_list_filter

        if self.part_check_filter is None:
            self.part_check_filter = {}

        if part_check_filter is not None:
            self.part_check_filter = part_check_filter

        if mortimer_url is not None:
            self.mortimer_url = mortimer_url

        if self.mortimer_url is None:
            raise ValueError("Required argument 'mortimer_url' is missing.")

        if self.content is None:
            self.content = screening_page_content

        if content is not None:
            self.content = content

        if repeated_participation is not None:
            self.repeated_participation = repeated_participation

        if register_on_hiding is not None:
            self.register_on_hiding = register_on_hiding

        if "title" not in kwargs:
            self.title = self.content["title"]

    def on_exp_access(self):
        if not self.repeated_participation:
            self.part_check_filter['self'] = {
                'exp_id': self.exp.exp_id,
                'exp_version': self.exp.version
                }

        self.append(al.Text(self.content["screening_info"]))

        if self.email_screening:
            self.append(
                al.RegEntry(
                    pattern=self.content["email_pattern"],
                    match_hint=self.content["email_match_hint"],
                    name="screening_email",
                    force_input=True,
                    leftlab=al.Label(self.content["email_instruction"], align="left"),
                    width="wide",
                )
            )

            self.append(al.Text(self.content["data_protection_info"]))

    def on_first_hide(self):

        if not self.screening_email.validate_data():
            return

        if not self.validate_screening_elements():
            self.exp.abort(
                reason=(
                    "Participant Screening:  The participant has been excluded based on"
                    " answers to additional screening elements on page."
                ),
                title=self.content["exclusion_title"],
                icon=self.content["exclusion_icon"],
                msg=self.content["exclusion_message"],
            )

            return

        if self.email_screening and (self.filter_by_part_check() or self.filter_by_mail_list()):
            return

        # Participation registration needs to be executed as last step
        if self.register_on_hiding:
            register_participation(
                self.exp, self.mortimer_url, with_screening_email=True
            )

        self.exp.session_status = "End of Participant Screening"

    def filter_by_part_check(self):
        for key, entry in self.part_check_filter.items():
            if "exp_version" in entry:
                result = check_participation(
                    mortimer_url=self.mortimer_url,
                    exp_id=entry["exp_id"],
                    exp_version=entry["exp_version"],
                    alias=self.screening_email.data["screening_email"]["value"],
                )

            else:
                result = check_participation(
                    mortimer_url=self.mortimer_url,
                    exp_id=entry["exp_id"],
                    alias=self.screening_email.data["screening_email"]["value"],
                )

            if result is True:
                if entry["exp_id"] == self.exp.exp_id:
                    reason = (
                        "Participant Screening: Participant has already participated "
                        "in this experiment and has been excluded."
                    )
                else:
                    reason = (
                        "Participant Screening: Participant has already participated "
                        f"in experiment '{key}' and has been excluded."
                    )

                self.exp.abort(
                    reason=reason,
                    title=self.content["exclusion_title"],
                    icon=self.content["exclusion_icon"],
                    msg=self.content["exclusion_message"],
                )

                return True

        return False

    def filter_by_mail_list(self):
        for key, mail_list in self.mail_list_filter.items():
            if self.screening_email.data["screening_email"]["value"].lower() in [e.lower() for e in mail_list]:
                self.exp.abort(
                    reason=(
                        f"The given email address was found in email list '{key}'. "
                        f"The participant has been excluded."
                    ),
                    title=self.content["exclusion_title"],
                    icon=self.content["exclusion_icon"],
                    msg=self.content["exclusion_message"],
                )

                return True

        return False

    def validate_screening_elements(self):
        return True

    @property
    def data(self):
        if not self.has_been_shown:
            return {}
        else:
            data = {}
            for element in self.input_elements.values():
                if "screening_email" not in element.data:
                    data.update(element.data)
            return data


def check_participation(
    mortimer_url: str, alias: str, exp_id: str, exp_version: str = None
):
    """
    Checks if alias was already registered.

    This method sends a request to a mortimer instance to
    check if the specified *alias* has already been registered as a
    participant for the given *exp_id* and, optionally, *exp_version*.

    Args:
        mortimer_url (str): The URL to a mortimer instance v0.8.2 or
            newer.
        alias (str): Usually an e-mail address. mortimer stores
            participation data based on hashed aliases. See
            :meth:`.register_participation` for more information.
        exp_id (str): Experiment ID for which to perform the check.
        exp_version (str): Experiment version for which to perform the
            check. Defaults to *None* which means that the participation
            check is performed for any version of the experiment.

    Returns:
        bool: *True* if alias has already been registered as a participant
        for the specified experiment, *False* if not.

    Raises:
        AlfredError: On request timeout or an error response, which means
        that the server could not be reached or insufficient data was sent
        (exp_id or alias missing).


    """
    if exp_version is not None:
        params = {"alias": alias.lower(), "exp_id": exp_id, "exp_version": exp_version}
    else:
        params = {"alias": alias.lower(), "exp_id": exp_id}

    r = requests.get(mortimer_url + "/participation", timeout=10, params=params)

    if r.status_code == 200 and r.text == "true":
        return True

    elif r.status_code == 200 and r.text == "false":
        return False

    else:
        raise AlfredError("Participant Screening Error: Participation check failed.")


def register_participation(
    exp: al.experiment.ExperimentSession,  # Cleared by Johannes
    mortimer_url: str,
    with_screening_email: bool = False,
    alias: str = None,
    ignore_already_registered: bool = False,
):
    """
    Registers a participant for the current experiment.

    This method sends a request to a mortimer instance to register the
    specified alias as participant for the experiment from which the
    method is called. Both
    :attr:`alfred3.experiment.ExperimentSession.exp_id` and
    :attr:`alfred3.experiment.ExperimentSession.version` are used to
    store the registration data in mortimer. There are two ways in which
    an alias can be passed to the method:

        * Manually specifying an alias with the *alias* argument
        * Deriving the alias as an e-mail address entered on a
            :class:`.ScreeningPage` which has to be included
            in the experiment.

    Args:
        exp (alfred3.experiment.ExperimentSession): The  object to access
            *exp_id* and *version*.
        mortimer_url (str): The URL to a mortimer instance v0.8.2 or newer.
        with_screening_email (bool): If *True* the alias will be set by
            accessing the data of a :class:`.ScreeningPage`.
        alias (str): Argument for manually passing an alias. Defaults to
            *None*.
        ignore_already_registered (bool): Set to *True* if the experiment
            should be continued even if the current participant alias was
            already registered. Defaults to *False*.

    Raises:
        AlfredError: On request timeout or an error response, which means
        that the server could not be reached or insufficient data was sent
        (exp_id or alias missing). Additionally, the method will raise an
        error if the specified participant alias was already registered
        and *ignore_already_registered* is set to *False* (which it is by
        default).


    """

    if with_screening_email and alias is not None:
        raise ValueError(
            "Participant Screening: Argument 'alias' has to be None if "
            "'with_screening_email' is set to True."
        )
    elif with_screening_email is False and alias is None:
        raise ValueError(
            "Participant Screening: Argument 'alias' cannot be None if "
            "'with_screening_email' is set to False."
        )

    if with_screening_email:
        alias = exp.all_pages["exp_screening"].screening_email.data["screening_email"][
            "value"
        ]

    r = requests.post(
        mortimer_url + "/participation",
        timeout=10,
        data={"alias": alias.lower(), "exp_id": exp.exp_id, "exp_version": exp.version},
    )

    if r.status_code == 201 and r.text == "success":
        exp.log.info("Experiment Screening: Participant registration successful.")

    elif r.status_code == 200 and r.text == "already registered":
        if ignore_already_registered:
            exp.log.warning(
                "Participant Screening: Participant was already registered for this "
                "experiment in the current version. Continuing the current session "
                "because argument 'ignore_already_registered' is set to True."
            )
        else:
            raise AlfredError(
                "Participant Screening Error: Participant was already registered for "
                "this experiment in the current version. Stopping the current session."
            )

    else:
        raise AlfredError(
            "Participant Screening Error: Participant registration failed. Stopping "
            "the current session."
        )
