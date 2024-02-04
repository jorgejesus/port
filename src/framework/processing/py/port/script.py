import logging
import io

import port.api.props as props
from port.api.commands import (CommandSystemDonate, CommandUIRender)

from port.api.questionare import questions 
from port.api.utils import find_question_by_value, find_id_by_value
import pandas as pd
import zipfile
import json

import base64

# This is a generic logger that will dump log information on the user's browsers
# This can also be changed for file logs on server/container 
LOG_STREAM = io.StringIO()
logging.basicConfig(
    stream=LOG_STREAM,
    level=logging.INFO,
    format="%(asctime)s --- %(name)s --- %(levelname)s --- %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)

LOGGER = logging.getLogger("yolo")

def data_quiz_to_rows(data_quiz): 
    _ = []
    for response in data_quiz:
        if response.__type__ == 'PayloadString':
            id = find_id_by_value (questions, response.value)
            question = find_question_by_value(questions,response.value)
            _.append((id,question,response.value))       
    return _

# Until here it show the first page or welcome page
def process(sessionId):
    yield donate(f"{sessionId}-tracking", '[{ "message": "user entered script" }]')
    platforms = ["Instagram"]

    # Adjust code for 
    subflows = len(platforms)
    steps = 3
    step_percentage = (100/subflows)/steps
    #Any print will dump it on the console.log of browser
    LOGGER.info(f"session id:{sessionId}")
    # progress in %
    progress = 0

    for index, platform in enumerate(platforms):
        meta_data = []
        meta_data.append(("debug", f"{platform}: start"))

        data = None
        data_quiz = []
        
        while True:
            # Render question 1
            _ = yield render_question_page(platform, progress, "q1")
            progress += step_percentage
            data_quiz.append(_)
            # Render question 2
            _ = yield render_question_page(platform, progress, "q2")
            data_quiz.append(_)
            progress += step_percentage
            # Render question 3
            _ = yield render_question_page(platform, progress, "q3")
            data_quiz.append(_)
            progress += step_percentage
            
            #print(q3_response) #{"__type__":"PayloadString","value":"Totally confortable, I am the center of group's attention, there is no group without me!!!"}
            
            donate(f"{sessionId}-{platform}", "Questionary done")
            
            meta_data.append(("debug", f"{platform}: prompt file"))
            promptFile = prompt_file(platform, "application/zip, text/plain")
            fileResult = yield render_donation_page(platform, promptFile, progress)
            if fileResult.__type__ == 'PayloadString':
                meta_data.append(("debug", f"{platform}: extracting file"))
                # fileResult.value is the filename 
                extractionResult = doSomethingWithTheFile(platform, fileResult.value)
                if extractionResult != 'invalid':
                    meta_data.append(("debug", f"{platform}: extraction successful, go to consent form"))
                    data = extractionResult
                    break
                else:
                    meta_data.append(("debug", f"{platform}: prompt confirmation to retry file selection"))
                    retry_result = yield render_donation_page(platform, retry_confirmation(platform), progress)
                    if retry_result.__type__ == 'PayloadTrue':
                        meta_data.append(("debug", f"{platform}: skip due to invalid file"))
                        continue
                    else:
                        meta_data.append(("debug", f"{platform}: retry prompt file"))
                        break
            else:
                meta_data.append(("debug", f"{platform}: skip to next step"))
                break
            
        # STEP 2: ask for consent and add quiz results to be in one single JSON payload
        progress += step_percentage
        if data is not None:
            meta_data.append(("debug", f"{platform}: prompt consent"))
            prompt = prompt_consent(platform, data, data_quiz, meta_data)
            consent_result = yield render_donation_page(platform, prompt, progress)
            progress += step_percentage
            if consent_result.__type__ == "PayloadJSON":
                # It would be more efficient to base64 binary content here as we have already filtered
                # the files to be submited. But then consent_result.value is a string like this (yes type str)
                # [{"zip_content":[{"filename":"photos/202010/0a8abe05d3522dad75da53df6f51e6c2.jpg","compressed size":"86988","size":"92491"},{"filename":"photos/202010/2b815e891c6c3d325f91772175dc57b3.jpg","compressed size":"159094","size":"159220"},{"filename":"photos/202010/2c855e509a802f5f85b483e5b55807c1.jpg","compressed size":"124918","size":"125071"}]},{"log_messages":[{"type":"debug","message":"Instagram: start"},{"type":"debug","message":"Instagram: prompt file"},{"type":"debug","message":"Instagram: extracting file"},{"type":"debug","message":"Instagram: extraction successful, go to consent form"},{"type":"debug","message":"Instagram: prompt consent"}]},{"user_omissions":"[]"}]
                # Better to do the base64 on the  doSomethingWithTheFile --> extract_zip_contents
                # Here we can reopen the zip file and inject the binary content into PayLoadJSON
                #file_encoded = base64.b64encode(file_content)
                meta_data.append(("debug", f"{platform}: donate consent data"))
                print("LOOKING AT CONSENT")
                tmp=json.loads(consent_result.value)
                # this is tmp [{'zip_content': [{'filename': 'photos/202010/0a8abe05d3522dad75da53df6f51e6c2.jpg', 'compressed size': '86988', 'size': '92491'}, {'filename': 'photos/202010/2b815e891c6c3d325f91772175dc57b3.jpg', 'compressed size': '159094', 'size': '159220'}, {'filename': 'photos/202010/2c855e509a802f5f85b483e5b55807c1.jpg', 'compressed size': '124918', 'size': '125071'}]}, {'quiz_content': [{'id': 'Q1_2', 'Question': '1. How often do you seek social interactions in your daily life?', 'Answer': 'A few times a week, I attend a meetup where I live'}, {'id': 'Q2_3', 'Question': '2. Do you feel energized and rejuvenated by spending time with people?', 'Answer': 'More or less, I think it depends who are the persons'}, {'id': 'Q3_5', 'Question': '3. How comfortable do you feel being the center of attention in a group setting?', 'Answer': 'If someone looks at me,  I will run to the emergency exit'}]}, {'log_messages': [{'type': 'debug', 'message': 'Instagram: start'}, {'type': 'debug', 'message': 'Instagram: prompt file'}, {'type': 'debug', 'message': 'Instagram: extracting file'}, {'type': 'debug', 'message': 'Instagram: extraction successful, go to consent form'}, {'type': 'debug', 'message': 'Instagram: prompt consent'}]}, {'user_omissions': '[]'}]
                print(tmp)
                yield donate(f"{sessionId}-{platform}", consent_result.value)

    yield render_end_page()

def render_question_page(platform, progress, question_key):
    question_data = questions.get(question_key)

    if not question_data:
        raise ValueError(f"No question found for key: {question_key}")

    header = props.PropsUIHeader(props.Translatable({"en": "Questionare", "nl": "Vragenlijst"}))
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
    header = props.PropsUIHeader(props.Translatable({
        "en": platform,
        "nl": platform
    }))

    footer = props.PropsUIFooter(progress)
    page = props.PropsUIPageDonation(platform, header, body, footer)
    return CommandUIRender(page)


def retry_confirmation(platform):
    text = props.Translatable({
        "en": f"Unfortunately, we cannot process your {platform} file. Continue, if you are sure that you selected the right file. Try again to select a different file.",
        "nl": f"Helaas, kunnen we uw {platform} bestand niet verwerken. Weet u zeker dat u het juiste bestand heeft gekozen? Ga dan verder. Probeer opnieuw als u een ander bestand wilt kiezen."
    })
    ok = props.Translatable({
        "en": "Try again",
        "nl": "Probeer opnieuw"
    })
    cancel = props.Translatable({
        "en": "Continue",
        "nl": "Verder"
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)


def prompt_file(platform, extensions):
    description = props.Translatable({
        "en": f"Please follow the download instructions and choose the file that you stored on your device. Click “Skip” at the right bottom, if you do not have a {platform} file. ",
        "nl": f"Volg de download instructies en kies het bestand dat u opgeslagen heeft op uw apparaat. Als u geen {platform} bestand heeft klik dan op “Overslaan” rechts onder."
    })

    return props.PropsUIPromptFileInput(description, extensions)


def doSomethingWithTheFile(platform, filename):
    return extract_zip_contents(filename)

def extract_zip_contents(zip_file):
    # Open the zip file
    #try:
        data = []
        with zipfile.ZipFile(zip_file, 'r') as z:
            for file_name in z.namelist():
                # Read the content of the file
                with z.open(file_name) as file:
                    file_content = file.read()
                    # Convert the content to base64
                    info = z.getinfo(file_name)
                    data.append((file_name, info.compress_size, info.file_size))
        return data

def prompt_consent(id, data, data_quiz, meta_data,):

    table_title = props.Translatable({
        "en": "Zip file contents",
        "nl": "Inhoud zip bestand"
    })

    log_title = props.Translatable({
        "en": "Log messages",
        "nl": "Log berichten"
    })
    quiz_title = props.Translatable({
        "en": "Questionare Results",
        "nl": "Vragenlijstresultaten"
    })

    quiz_frame=pd.DataFrame(data_quiz_to_rows(data_quiz), columns=["id", "Question","Answer"])
    table_quiz = props.PropsUIPromptConsentFormTable("quiz_content", quiz_title, quiz_frame)
    
    data_frame = pd.DataFrame(data, columns=["filename", "compressed size", "size" ])
    table_zip = props.PropsUIPromptConsentFormTable("zip_content", table_title, data_frame)
    meta_frame = pd.DataFrame(meta_data, columns=["type", "message"])
    meta_table = props.PropsUIPromptConsentFormTable("log_messages", log_title, meta_frame)
    
    return props.PropsUIPromptConsentForm([table_zip,table_quiz], [meta_table])


def donate(key, json_string):
    return CommandSystemDonate(key, json_string)
