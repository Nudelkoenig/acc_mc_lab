"""Custom classes for participant registration and payout in Alfred 3

author: Christian Treffenstädt
updated: 2022-03-29

"""

import alfred3 as al

registration_page_content = dict(
    title="Participant Registration",
    statustext="Klick on 'Continue' to complete your registration.",

    instr_no_registration="We do not need any of your personal information.",
    instr_registration="Please enter the following personal information",

    first_name_instr="First name",
    last_name_instr="Last name",

    birth_date_instr="Birthday",
    birth_date_pattern=r"^(0[1-9]|[12][0-9]|3[01])[-/.](0[1-9]|1[012])[-/.](19|20)\d\d$",
    birth_date_suffix="DD.MM.YYYY",
    birth_date_match_hint="This will be the match hint for the birth date field.",

    email_instr="Email",
    email_pattern=r"[^@]+@[^@]+\.[^@]+",
    email_match_hint="Please enter a valid email address.",

    iban_instr="IBAN",
    iban_pattern=r"^[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?:[ ]?[0-9]{1,2})?$",
    iban_match_hint="Error: Please check your input.",

    bic_instr="BIC",
    bic_pattern=r"^[a-zA-Z]{6}[0-9a-zA-Z]{2}([0-9a-zA-Z]{3})?$",
    bic_match_hint="Error: Please check your input.",

    tax_office_instr="Tax office",

    phone_instr="Phone number",
    phone_pattern=r"^\+?(?:[0-9]\x20?){6,14}[0-9]$",
    phone_match_hint="Error: Please check your input.",

    street_instr="Street name",
    house_number_instr="House number",

    postal_code_instr="Post code",
    postal_code_pattern=r"(?i)^[a-z0-9][a-z0-9\- ]{0,10}[a-z0-9]$",
    postal_code_match_hint="Error: Please check your input.",

    city_instr="City name",
    country_instr="Country name",

    various_instr="Various information",
    various_pattern=r"^..*$",  # Anything but empty
    various_match_hint="Error: Please check your input.",

    privacy_info="This is a dummy text for privacy information",
    repeated_title="It seems you have already participated in this experiment",
    repeated_text="This is a dummy text for the repeated participation page",

    repeated_participation_title="Repeated participation detected",
    repeated_participation_icon="times-circle",

    repeated_participation_message="Sorry, but repeated participation is not allowed in this experiment. "
                           "Your personal data will not be saved",
)

registration_selection_content = dict(
    title="Select a Registration Option",
    instr_selection="This is a general selection instruction",
    instr_choice="This is the instruction for the selection element",

    # The following option needs to be set to the number of options
    # in this dictionary. There can be more options in the dictionary
    # than are shown on the page. You can add configuration blocks for
    # more options and update the available_options setting, whenever
    # necessary

    available_options=5,

    show_option_1=True,
    option_1_instruction="This is the instruction for option 1.",
    option_1_label="Itemlabel Option 1",
    option_1_register_name=True,
    option_1_register_birth_date=True,
    option_1_register_email=True,
    option_1_register_phone=False,
    option_1_register_iban=True,
    option_1_register_address=True,
    option_1_register_various=True,
    option_1_register_payout=False,

    show_option_2=True,
    option_2_instruction="This is the instruction for option 2.",
    option_2_label="Itemlabel Option 2",
    option_2_register_name=True,
    option_2_register_birth_date=False,
    option_2_register_email=True,
    option_2_register_phone=False,
    option_2_register_iban=True,
    option_2_register_address=False,
    option_2_register_various=False,
    option_2_register_payout=False,

    show_option_3=True,
    option_3_instruction="This is the instruction for option 3.",
    option_3_label="Itemlabel Option 3",
    option_3_register_name=True,
    option_3_register_birth_date=False,
    option_3_register_email=True,
    option_3_register_phone=False,
    option_3_register_iban=False,
    option_3_register_address=False,
    option_3_register_various=False,
    option_3_register_payout=False,

    show_option_4=True,
    option_4_instruction="This is the instruction for option 4.",
    option_4_label="Itemlabel Option 4",
    option_4_register_name=True,
    option_4_register_birth_date=False,
    option_4_register_email=True,
    option_4_register_phone=False,
    option_4_register_iban=False,
    option_4_register_address=False,
    option_4_register_various=False,
    option_4_register_payout=False,

    show_option_5=True,
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


class RegistrationPage(al.UnlinkedDataPage):
    """DocString is missing!"""

    name = "exp_registration"
    prefix_element_names = False
    register_name = False
    register_birth_date = False
    register_email = True
    register_phone = False
    register_iban = False
    register_address = False
    register_various = False
    register_payout = False
    content = None
    in_registration_section = False
    check_repeated = True
    version_specific = True

    def __init__(
            self,
            register_name: bool = None,
            register_birth_date: bool = None,
            register_email: bool = None,
            register_phone: bool = None,
            register_iban: bool = None,
            register_address: bool = None,
            register_various: bool = None,
            register_payout: bool = None,
            content: dict = None,
            in_registration_section: bool = None,
            check_repeated: bool = None,
            version_specific: bool = None,
            **kwargs,
    ):

        if self.name != "exp_registration":
            raise ValueError(
                "Property 'name' cannot be set for a RegistrationPage. For referencing "
                "purposes, the RegistrationPage is always named 'exp_registration'."
            )

        if "name" in kwargs:
            raise ValueError(
                "Argument 'name' cannot be set for a RegistrationPage. For referencing "
                "purposes, the RegistrationPage is always named 'exp_registration'."
            )

        if self.prefix_element_names:
            raise ValueError(
                "Property 'prefix_element_names' cannot be set for a RegistrationPage, as"
                "prefixes are added automatically."
            )

        if "prefix_element_names" in kwargs:
            raise ValueError(
                "Argument 'prefix_element_names' cannot be set for a RegistrationPage, as"
                "prefixes are added automatically."
            )

        super(RegistrationPage, self).__init__(
            **kwargs, prefix_element_names=False, name="exp_registration"
        )

        if register_name is not None:
            self.register_name = register_name

        if register_birth_date is not None:
            self.register_birth_date = register_birth_date

        if register_email is not None:
            self.register_email = register_email

        if register_phone is not None:
            self.register_phone = register_phone

        if register_iban is not None:
            self.register_iban = register_iban

        if register_address is not None:
            self.register_address = register_address

        if register_various is not None:
            self.register_various = register_various

        if register_payout is not None:
            self.register_payout = register_payout

        if content is not None:
            self.content = content

        if self.content is None:
            self.content = registration_page_content

        if in_registration_section is not None:
            self.in_registration_section = in_registration_section

        if check_repeated is not None:
            self.check_repeated = check_repeated

        if version_specific is not None:
            self.version_specific = version_specific

        if "title" not in kwargs:
            self.title = self.content["title"]

    def on_exp_access(self):
        # Todo: Create own custom RowLayout and pass to the following
        #       input elements.
        # Todo: Add description argument for all input elements. Add
        #       description placeholders to content

        self += al.Alert(
            self.content["instr_registration"],
            align="center",
            category="dark",
        )

        first_name = al.TextEntry(
            name="exp_reg_first_name",
            toplab=self.content["first_name_instr"],
            force_input=True,
            layout=(4, 8),
            align="center",
            description=f"Participant Registration: First Name "
                        f"({self.content['first_name_instr']})"
        )

        last_name = al.TextEntry(
            name="exp_reg_last_name",
            toplab=self.content["last_name_instr"],
            force_input=True,
            layout=(3, 9),
            align="center",
            description=f"Participant Registration: Last Name "
                        f"({self.content['last_name_instr']})"
        )

        row = al.Row(
            first_name, last_name,

        )
        row.layout.width_sm = [5, 7]

        self += row

        date_of_birth = al.RegEntry(
            name="exp_reg_date_of_birth",
            toplab=self.content["birth_date_instr"],
            force_input=True,
            layout=(4, 8),
            pattern=self.content["birth_date_pattern"],
            suffix=self.content["birth_date_suffix"],
            match_hint=self.content["birth_date_match_hint"],
            align="center",
            description=f"Participant Registration: Date of Birth "
                        f"({self.content['birth_date_instr']})"
        )

        mail = al.RegEntry(
            name="exp_reg_email",
            toplab=self.content["email_instr"],
            force_input=True,
            layout=(3, 9),
            pattern=self.content["email_pattern"],
            match_hint=self.content["email_match_hint"],
            align="center",
            description=f"Participant Registration: E-mail "
                        f"({self.content['email_instr']})"
        )

        row_birth_mail = al.Row(
            date_of_birth, mail,
        )

        row_birth_mail.layout.width_sm = [5, 7]

        self += row_birth_mail

        self += al.RegEntry(
            name="exp_reg_phone",
            toplab=self.content["phone_instr"],
            force_input=True,
            layout=5,
            pattern=self.content["phone_pattern"],
            match_hint=self.content["phone_match_hint"],
            align="center",
            description=f"Participant Registration: Phone Number "
                        f"({self.content['phone_instr']})"
        )

        self += al.TextEntry(
            name="exp_reg_tax_office",
            toplab=self.content["tax_office_instr"],
            force_input=True,
            layout=(2, 4),
            align="center",
            description=f"Participant Registration: Tax Office "
                        f"({self.content['tax_office_instr']})"
        )

        iban = al.RegEntry(
            name="exp_reg_iban",
            toplab=self.content["iban_instr"],
            force_input=True,
            layout=(2, 10),
            pattern=self.content["iban_pattern"],
            match_hint=self.content["iban_match_hint"],
            align="center",
            description=f"Participant Registration: IBAN "
                        f"({self.content['iban_instr']})"
        )

        bic = al.RegEntry(
            name="exp_reg_bic",
            toplab=self.content["bic_instr"],
            force_input=True,
            layout=(4, 8),
            pattern=self.content["bic_pattern"],
            match_hint=self.content["bic_match_hint"],
            align="center",
            description=f"Participant Registration: BIC "
                        f"({self.content['bic_instr']})"
        )

        row_iban_bic = al.Row(
            iban, bic,

            align="left"
        )

        row_iban_bic.layout.width_sm = [7, 5]

        self += row_iban_bic

        street = al.TextEntry(
            name="exp_reg_street",
            toplab=self.content["street_instr"],
            force_input=True,
            layout=(3, 9),
            align="center",
            description=f"Participant Registration: Street "
                        f"({self.content['street_instr']})"
        )

        house_number = al.TextEntry(
            name="exp_reg_house_number",
            toplab=self.content["house_number_instr"],
            force_input=True,
            layout=(5, 7),
            align="center",
            description=f"Participant Registration: House Number "
                        f"({self.content['house_number_instr']})"
        )

        row_street_number = al.Row(
            street, house_number,

        )
        row_street_number.layout.width_sm = [7, 5]

        self += row_street_number

        postal_code = al.RegEntry(
            name="exp_reg_postal_code",
            toplab=self.content["postal_code_instr"],
            force_input=True,
            layout=(4, 8),
            pattern=self.content["postal_code_pattern"],
            match_hint=self.content["postal_code_match_hint"],
            align="center",
            description=f"Participant Registration: Postal Code "
                        f"({self.content['postal_code_instr']})"
        )

        city = al.TextEntry(
            name="exp_reg_city",
            toplab=self.content["city_instr"],
            force_input=True,
            layout=(3, 9),
            align="center",
            description=f"Participant Registration: City "
                        f"({self.content['city_instr']})"
        )

        country = al.TextEntry(
            name="exp_reg_country",
            toplab=self.content["country_instr"],
            force_input=True,
            layout=(2, 4),
            width="medium",
            position="center",
            align="center",
            description=f"Participant Registration: Country "
                        f"({self.content['country_instr']})"
        )

        row_postcode_city_country = al.Row(
            postal_code, city, country

        )

        row_postcode_city_country.layout.width_sm = [2, 5, 5]

        self += row_postcode_city_country

        self += al.RegEntry(
            name="exp_reg_various",
            toplab=self.content["various_instr"],
            force_input=True,
            layout=(2, 4),
            pattern=self.content["various_pattern"],
            match_hint=self.content["various_match_hint"],
            align="center",
            description=f"Participant Registration: Various "
                        f"({self.content['various_instr']})"
        )

    def on_each_show(self):
        self.exp.session_status = "participant registration"

        if self.register_name:
            self.exp_reg_first_name.should_be_shown = True
            self.exp_reg_last_name.should_be_shown = True
        else:
            self.exp_reg_first_name.should_be_shown = False
            self.exp_reg_last_name.should_be_shown = False

        if self.register_birth_date:
            self.exp_reg_date_of_birth.should_be_shown = True
        else:
            self.exp_reg_date_of_birth.should_be_shown = False

        if self.register_email:
            self.exp_reg_email.should_be_shown = True
        else:
            self.exp_reg_email.should_be_shown = False

        if self.register_phone:
            self.exp_reg_phone.should_be_shown = True
        else:
            self.exp_reg_phone.should_be_shown = False

        if self.register_iban:
            self.exp_reg_iban.should_be_shown = True
            self.exp_reg_bic.should_be_shown = True
            self.exp_reg_tax_office.should_be_shown = True
        else:
            self.exp_reg_iban.should_be_shown = False
            self.exp_reg_bic.should_be_shown = False
            self.exp_reg_tax_office.should_be_shown = False

        if self.register_address:
            self.exp_reg_street.should_be_shown = True
            self.exp_reg_house_number.should_be_shown = True
            self.exp_reg_postal_code.should_be_shown = True
            self.exp_reg_city.should_be_shown = True
            self.exp_reg_country.should_be_shown = True
        else:
            self.exp_reg_street.should_be_shown = False
            self.exp_reg_house_number.should_be_shown = False
            self.exp_reg_postal_code.should_be_shown = False
            self.exp_reg_city.should_be_shown = False
            self.exp_reg_country.should_be_shown = False

        if self.register_various:
            self.exp_reg_various.should_be_shown = True
        else:
            self.exp_reg_various.should_be_shown = False

        if sum([
            self.register_name,
            self.register_birth_date,
            self.register_email,
            self.register_phone,
            self.register_iban,
            self.register_address,
            self.register_various
        ]) == 0:
            self += al.Text(self.content["instr_no_registration"])

    def on_close(self):

        if self.register_payout:
            self += al.Value(
                name="exp_reg_payout", value=self.exp.adata["payout"]
            )
        self.exp.adata["payout"] = "deleted"

        # Todo: Implement repeated participation check for name and birth date
        if self.check_repeated:

            if self.register_iban:
                check_iban = self.exp.data_manager.unlinked_data['exp_data']['exp_reg_iban']['value']
                self.exp_reg_iban.input = None
                self.save_data(sync=True)

                for dataset in self.exp.all_unlinked_data:

                    try:
                        decrypt_iban = self.exp.decrypt(str(dataset["exp_reg_iban"]))

                    except:
                        self.exp.log.warning(
                            'Participant Registration: Could not decrypt IBAN in repeated participation check '
                        )
                        decrypt_iban = ''

                    if check_iban == decrypt_iban:
                        for element in self.input_elements.values():
                            element.input = None  # This deletes all user input for the registration page

                        self.exp.abort(
                            reason=(
                                "Participant Registration:  The participant has been excluded based on"
                                " a repeated participation."
                            ),
                            title=self.content["repeated_participation_title"],
                            icon=self.content["repeated_participation_icon"],
                            msg=self.content["repeated_participation_message"],
                        )
            
                self.exp_reg_iban.input = check_iban
            self.exp._save_data() # TODO Remove after update to alfred3 v2.3.2 (Issue #169)


class SelectionPage(al.NoDataPage):
    """DocString is missing!"""

    content = None

    def __init__(self, content: dict = None, **kwargs):
        if "name" in kwargs:
            raise ValueError(
                "Argument 'name' cannot be set for a RegistrationSelection page. For "
                "referencing purposes, RegistrationSelection is always named "
                "'exp_reg_selection'."
            )

        super(SelectionPage, self).__init__(**kwargs, name="exp_reg_selection")

        if content is not None:
            self.content = content

        if self.content is None:
            self.content = registration_selection_content

        if "title" not in kwargs:
            self.title = self.content["title"]

    def on_exp_access(self):
        self += al.Text(self.content["instr_selection"])

        item_labels = []

        for i in range(self.content["available_options"]):
            if self.content[f"show_option_{i + 1}"]:
                self += al.Text(self.content[f"option_{i + 1}_instruction"])
                item_labels.append(self.content[f"option_{i + 1}_label"])

        self += al.SingleChoiceList(
            *item_labels,
            toplab=self.content["instr_choice"],
            name="registration_choice",
            force_input=True,
            width="medium",
        )

    def on_each_hide(self):
        selection = self.registration_choice.choice_labels.index(
            self.registration_choice.input) + 1

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_name = self.content[f"option_{selection}_register_name"]

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_birth_date = self.content[f"option_{selection}_register_birth_date"]

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_email = self.content[f"option_{selection}_register_email"]

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_phone = self.content[f"option_{selection}_register_phone"]

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_iban = self.content[f"option_{selection}_register_iban"]

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_address = self.content[f"option_{selection}_register_address"]

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_various = self.content[f"option_{selection}_register_various"]

        self.exp.root_section.all_pages[
            "exp_registration"
        ].register_payout = self.content[f"option_{selection}_register_payout"]
