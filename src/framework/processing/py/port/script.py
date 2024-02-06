# TODO: pytests for payload creation, check is base64 encoding is OS, t
# test that only adjusted/permitted data is submitted. Selenium testing of page
import logging
import io
import pandas as pd
import zipfile
import json
import base64

import port.api.props as props
from port.api.commands import CommandSystemDonate, CommandUIRender

from port.api.questionare import questions
from port.api.utils import find_question_by_value, find_id_by_value
from port.api.utils import extract_zip_file_info, zip_file_to_b64, data_quiz_to_rows

# meta_tables: a list of optional tables, for example for logging data

# Until this code part we have  the first page or welcome page
# process is where the page sequence is defined
def process(sessionId):
    # sessionId is a unix epoch time stamp (maybe it should be a uuid v7)

    yield donate(f"{sessionId}-tracking", '[{ "message": "user entered script" }]')
    platform = "Instagram"

    # Set progress bar for the necessary
    steps = 3
    step_percentage = 100 / steps
    progress = 0

    # Lists to whom data will be appended
    data = None
    data_quiz = []

    # Extra info dumped in meta_data object and later donated
    meta_data = []

    def log_meta_data(message, meta_data=meta_data):
        """Nested function Logs a debug message to the meta_data list, indicating an action or state
        relevant to the application's operation.

        Parameters
        ----------
        message : str
            The debug message to be added to the meta_data list.
        meta_data : list, optional
            The list to which the debug message will be appended.
            If not provided, defaults to the global `meta_data` list.

        """
        meta_data.append(("debug", message))

    log_meta_data("Start")

    # START OF PROCESS

    # Autogenerate question_ids list from questions dictionary keys
    question_ids = list(questions.keys())

    # Now loop for each question and increase progress bar question_ids
    # QUIZ  PAGES
    for question_id in question_ids:
        response = yield render_question_page(platform, progress, question_id)
        data_quiz.append(response)
        progress += step_percentage
    # END OF QUIZ

    donate(f"{sessionId}-{platform}", "Questionary done")
    while True:
        # While loop to ensure if there is problem with file submission to
        # redo the file submission
        log_meta_data(f"{platform}: prompt file")

        promptFile = prompt_file(platform, "application/zip, text/plain")
        fileResult = yield render_donation_page(platform, promptFile, progress)

        if fileResult.__type__ == "PayloadString":
            log_meta_data("Extracting file")

            # fileResult.value is the zip file_name submitted by user
            # leaving doSomethingWithTheFile naming convention as it is :)
            extractionResult = doSomethingWithTheFile(platform, fileResult.value)

            if extractionResult != None:
                log_meta_data("Extraction successful, go to consent form")
                data = extractionResult
                break
            else:
                log_meta_data("Prompt confirmation to retry file selection")
                retry_result = yield render_donation_page(
                    platform, retry_confirmation(platform), progress
                )
                if retry_result.__type__ == "PayloadTrue":
                    log_meta_data("Skip due to invalid file")
                    continue
                else:
                    log_meta_data("Retry prompt file")
                    break
        else:
            log_meta_data("Skip to next step")
            break

        # STEP 2: ask for consent and add quiz results to be in one single JSON payload
    progress += step_percentage

    if data != None:
        log_meta_data("Prompt consent")

        prompt = prompt_consent(platform, data, data_quiz, meta_data)
        consent_result = yield render_donation_page(platform, prompt, progress)
        progress += step_percentage
        if consent_result.__type__ == "PayloadJSON":
            log_meta_data("Donate consent data")

            payload_list = json.loads(
                # from code above and it contains the zip file name
                consent_result.value
            )
            # payload_list is like this:
            # [{'zip_content': [{'filename': 'photos/202010/0a8..c2.jpg',
            # 'compressed size': '86988', 'size': '92491'},....
            # {'type': 'debug', 'message': 'Instagram: extraction successful, go to consent form'}, .....
            # {'user_omissions': '[]'}]
            # getting dic with files paths and informations
            payload_file_dic = payload_list[0]

            # Getting files and convert them into base64
            for _, zip_content in payload_file_dic.items():
                zip_payload = []
                for item_dic in zip_content:
                    file_to_extract = item_dic["filename"]
                    file_encoded = zip_file_to_b64(fileResult.value, file_to_extract)
                    # THIS IS JUST A DEMO THE BASE64 STRING IS TO BIG, LETS CUT IT OUT
                    # TO MAKE THINGS READABLE ON JSON PAYLOAD
                    item_dic["payload"] = file_encoded[0:100]
                    payload_list.append(item_dic)

            payload_file_dic["zip_content"] = payload_list
            payload_list[0] = payload_file_dic
            consent_result.value = str(payload_list)  # convertion back to string

        yield donate(f"{sessionId}-{platform}", consent_result.value)

    # Thank you, page
    yield render_end_page()


## HTML PAGES to be rendered by def process(sessionId):


def render_question_page(platform, progress, question_key):
    question_data = questions.get(question_key)

    if not question_data:
        raise ValueError(f"No question found for key: {question_key}")

    header = props.PropsUIHeader(
        props.Translatable({"en": "Questionare", "nl": "Vragenlijst"})
    )
    title = props.Translatable(question_data["title"])
    description = props.Translatable(question_data["description"])
    items = [props.RadioItem(item) for item in question_data["items"]]

    body = props.PropsUIPromptRadioInput(title, description, items)
    footer = props.PropsUIFooter(progress)
    page = props.PropsUIPageDonation(platform, header, body, footer)

    return CommandUIRender(page)


def render_end_page():
    page = props.PropsUIPageEnd()
    return CommandUIRender(page)


def render_donation_page(platform, body, progress):
    header = props.PropsUIHeader(props.Translatable({"en": platform, "nl": platform}))

    footer = props.PropsUIFooter(progress)
    page = props.PropsUIPageDonation(platform, header, body, footer)
    return CommandUIRender(page)


def retry_confirmation(platform):
    text = props.Translatable(
        {
            "en": f"Unfortunately, we cannot process your {platform} file. Continue, if you are sure that you selected the right file. Try again to select a different file.",
            "nl": f"Helaas, kunnen we uw {platform} bestand niet verwerken. Weet u zeker dat u het juiste bestand heeft gekozen? Ga dan verder. Probeer opnieuw als u een ander bestand wilt kiezen.",
        }
    )
    ok = props.Translatable({"en": "Try again", "nl": "Probeer opnieuw"})
    cancel = props.Translatable({"en": "Continue", "nl": "Verder"})
    return props.PropsUIPromptConfirm(text, ok, cancel)


def prompt_file(platform, extensions):
    description = props.Translatable(
        {
            "en": f"Please follow the download instructions and choose the file that you stored on your device. Click “Skip” at the right bottom, if you do not have a {platform} file. ",
            "nl": f"Volg de download instructies en kies het bestand dat u opgeslagen heeft op uw apparaat. Als u geen {platform} bestand heeft klik dan op “Overslaan” rechts onder.",
        }
    )

    return props.PropsUIPromptFileInput(description, extensions)


def doSomethingWithTheFile(platform, filename):
    return extract_zip_file_info(filename)


def prompt_consent(
    id,
    data,
    data_quiz,
    meta_data,
):

    table_title = props.Translatable(
        {"en": "Zip file contents", "nl": "Inhoud zip bestand"}
    )

    log_title = props.Translatable({"en": "Log messages", "nl": "Log berichten"})
    quiz_title = props.Translatable(
        {"en": "Questionare Results", "nl": "Vragenlijstresultaten"}
    )

    quiz_frame = pd.DataFrame(
        data_quiz_to_rows(questions, data_quiz), columns=["id", "Question", "Answer"]
    )
    table_quiz = props.PropsUIPromptConsentFormTable(
        "quiz_content", quiz_title, quiz_frame
    )

    data_frame = pd.DataFrame(data, columns=["filename", "compressed size", "size"])
    table_zip = props.PropsUIPromptConsentFormTable(
        "zip_content", table_title, data_frame
    )
    meta_frame = pd.DataFrame(meta_data, columns=["type", "message"])
    meta_table = props.PropsUIPromptConsentFormTable(
        "log_messages", log_title, meta_frame
    )

    return props.PropsUIPromptConsentForm([table_zip, table_quiz], [meta_table])


def donate(key, json_string):
    return CommandSystemDonate(key, json_string)
