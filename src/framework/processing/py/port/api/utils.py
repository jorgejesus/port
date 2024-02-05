# Module with generic functions and file processing code

import zipfile
import base64


def zip_file_to_b64(zip_file_path, file_to_extract):
    """
       Opens the zip file submitted by user, gets the file to be encoded, reads binary into base64 and returns base64 string
    non-negative, numeric input values.

       Parameters
       ----------
       zip_file_path : str
           zip file to open, that is on pydiode filesystem e.g horsesarecool52_20201020.zip.
       file_to_extract : str
           file name and path to be converted e.g photos/202010/000a4f5dbe0f67f2760d3766233cddd0.jpg  .

       Returns
       -------
       str
           file encoded as base64
    """

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        # Extract the specific file to memory
        with zip_ref.open(file_to_extract) as file:
            # Read the content of the file
            file_content = file.read()
            # Encode the file content in base64
            encoded_content = base64.b64encode(file_content)
            # Print or use the encoded content
            _ = encoded_content.decode()  # Decoding for readability if printing
    return _


def extract_zip_file_info(zip_file):
    """
    Extract information about each file in a zip archive.

    This function opens a zip file and extracts information for each file contained within it. For each file, it gathers the file name, its compressed size, and its original size before compression. This information is returned as a list of tuples.

    Parameters
    ----------
    zip_file : str
        The path to the zip file from which to extract file information.

    Returns
    -------
    list of tuples
        A list where each tuple contains the following information about a file in the zip archive:
        - file_name (str): The name of the file.
        - compress_size (int): The size of the file after compression, in bytes.
        - file_size (int): The original size of the file before compression, in bytes.
    """

    data = []
    try:
        with zipfile.ZipFile(zip_file, "r") as z:
                for file_name in z.namelist():
                    with z.open(file_name) as file:
                        file_content = file.read()
                        info = z.getinfo(file_name)
                        data.append((file_name, info.compress_size, info.file_size))
    except zipfile.BadZipFile:
        return None
    return data


## Questionary or questions function and tools


def find_question_by_value(questions, target_value, language="en"):
    """
    Search for a question by a given answer value in a specified language.

    Iterates through a dictionary of questions, each containing multiple items (possible answers),
    to find the first question for which any of its items' values match the `target_value`. Returns
    the question's title in the specified language if found, otherwise returns `None`.

    Parameters
    ----------
    questions : dict
        A dictionary with questions, possible answers and questions/answer ids. See: questionare.questions dic.
    target_value : str
        The value of the answer to search for among the questions.
    language : str, optional
        The language in which to return the question's title. Default is "en" only options are "en" and "nl".

    Returns
    -------
    str or None
        The title of the first question that contains an item with a value matching `target_value`
        in the specified `language`, or `None` if no match is found.

    Examples
    --------
    >>> from questionare import questions
    >>> find_question_by_value(questions, "Every day")
    """
    return next(
        (
            question["title"][language]
            for question in questions.values()
            if any(item["value"] == target_value for item in question["items"])
        ),
        None,  # Default value if no item matches
    )


def find_id_by_value(questions, target_value):
    """
    Find the ID of a question item based on a specific answer value.

    Searches through a structured dictionary of questions and their possible answers
    to find the first item whose 'value' matches the specified `target_value`. Returns
    the 'id' of the matching item if found, otherwise returns `None`.

    Parameters
    ----------
    questions : dict
        A dictionary with questions, possible answers and questions/answer ids. See: questionare.questions dic.
    target_value : str
        The answer value to search for among all question items.

    Returns
    -------
    str or None
        The 'id' of the first question item that matches the `target_value`, or `None` if
        no match is found.

    Examples
    --------
    >>> from questionare import questions
    >>> find_id_by_value(questions, "Every day")
    'Q1_1'
    """
    return next(
        (
            item["id"]
            for question in questions.values()
            for item in question["items"]
            if item["value"] == target_value
        ),
        None,  # Default value if no item matches
    )


def data_quiz_to_rows(questions, data_quiz):
    """
    Reorganizes quiz data into a structured list containing question IDs, question titles, and answers.

    Iterates through a list of quiz responses, identifying the type of each response. For responses
    identified as 'PayloadString', it finds the corresponding question ID and title based on the
    response value. Each identified item is then stored in a new list as a tuple containing the
    question ID, question title, and the original response value.

    Parameters
    ----------
    data_quiz : list
        A list of response objects, where each response object is expected to have a '__type__'
        attribute indicating its type ('PayloadString' for the relevant ones) and a 'value'
        attribute containing the answer text.

    Returns
    -------
    list of tuples
        A list where each tuple contains:
        - The ID of the question corresponding to a response (str or None if not found).
        - The title of the question corresponding to a response (str or None if not found).
        - The original value of the response (str).

    Examples
    --------
    >>> data_quiz = [
    ...     {"__type__": "PayloadString", "value": "Every day"},
    ...     {"__type__": "PayloadString", "value": "A few times a week"}
    ... ]
    >>> data_quiz_to_rows(data_quiz)
    [('Q1_1', 'How often do you seek social interactions?', 'Every day'),
     ('Q1_2', 'How often do you seek social interactions?', 'A few times a week')]
    """

    _ = []
    for response in data_quiz:
        if response.__type__ == "PayloadString":
            id = find_id_by_value(questions, response.value)
            question = find_question_by_value(questions, response.value)
            _.append((id, question, response.value))
    return _
