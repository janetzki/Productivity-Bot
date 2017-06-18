"""
This code sample is a part of a simple demo to show beginners how to create a skill (app) for the Amazon Echo using AWS Lambda and the Alexa Skills Kit.

For the full code sample visit https://github.com/pmckinney8/Alexa_Dojo_Skill.git
"""

from __future__ import print_function
import requests
import json

alcohol_url = "https://hpi.de/naumann/sites/ingestion/hackhpi/alcohol/add"
caffeine_url = "https://hpi.de/naumann/sites/ingestion/hackhpi/caffeine/add"
profile_url = "https://hpi.de/naumann/sites/ingestion/hackhpi/alcohol/setprofile"
caffeine_recommendation_url = "https://hpi.de/naumann/sites/ingestion/hackhpi/caffeine/recommendation"
alcohol_recommendation_url = "https://hpi.de/naumann/sites/ingestion/hackhpi/alcohol/recommendation"


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "DrinkIntend":
        return get_drink_response(intent_request)
    elif intent_name == "DrinkFinishedIntend":
        return get_finished_drink(intent_request)
    elif intent_name == "CaffeineIntend":
        return get_caffeine(intent_request)
    elif intent_name == "AlcoholIntend":
        return get_alcohol(intent_request)
    elif intent_name == "CaffeineRecommendationIntend":
        return get_caffeine_recommendation()
    elif intent_name == "AlcoholRecommendationIntend":
        return get_alcohol_recommendation()
    elif intent_name == "CaffeineLevelIntend":
        return get_caffeine_level()
    elif intent_name == "AlcoholLevelIntend":
        return get_alcohol_level()
    elif intent_name == "SexIntend":
        return set_sex(intent_request)
    elif intent_name == "BodyweightIntend":
        return set_bodyweight(intent_request)
    elif intent_name == "AgeIntend":
        return set_age(intent_request)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Productivity Bot. I will help you stay in your Ballmer Peak."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = "Welcome to the help section for the Productivity Bot. A couple of examples of phrases that I can except are... What shall I drink... or, how much alcohol does a drink contain. Lets get started now by trying one of these."

    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_drink_response(intent_request):
    session_attributes = {}
    card_title = "Drink response"
    drink = intent_request["intent"]["slots"]["Drink"]["value"]
    requests.post(caffeine_url, json={"drink": drink})  # todo: specify serving (ml)
    requests.post(alcohol_url, json={"drink": drink})  # todo: specify serving (ml)
    speech_output = f"Enjoy your {drink}."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_finished_drink(intent_request):
    session_attributes = {}
    card_title = "Finished drink response"
    drink = intent_request["intent"]["slots"]["Drink"]["value"]
    # requests.post("https://hpi.de/naumann/sites/ingestion/hackhpi/", json={"drink finished": drink})
    speech_output = f"I hope your {drink} was tasty."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_caffeine_recommendation():
    session_attributes = {}
    card_title = "Caffeine recommendation response"
    json_answer = requests.get(caffeine_recommendation_url).text
    speech_output = json.loads(json_answer)["results"]
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_alcohol_recommendation():
    session_attributes = {}
    card_title = "Alcohol recommendation response"
    json_answer = requests.get(alcohol_recommendation_url).text
    speech_output = json.loads(json_answer)["results"]
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_caffeine(intent_request):
    session_attributes = {}
    card_title = "Caffeine response"
    drink = intent_request["intent"]["slots"]["Drink"]["value"]
    speech_output = f"{drink} contains a lot of caffeine."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_alcohol(intent_request):
    session_attributes = {}
    card_title = "Alcohol response"
    drink = intent_request["intent"]["slots"]["Drink"]["value"]
    speech_output = f"{drink} contains a lot of alcohol."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_caffeine_level():
    session_attributes = {}
    card_title = "Caffeine level response"
    speech_output = "Your caffeine level is over 9000."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_alcohol_level():
    session_attributes = {}
    card_title = "Alcohol level response"
    speech_output = "Your alcohol level is over 9000."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def set_sex(intent_request):
    session_attributes = {}
    card_title = "Sex response"
    sex = intent_request["intent"]["slots"]["Sex"]["value"]
    requests.post(profile_url, json={"sex": sex})
    speech_output = f"Yes, you are so {sex}."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def set_bodyweight(intent_request):
    session_attributes = {}
    card_title = "Bodyweight response"
    weight = intent_request["intent"]["slots"]["Number"]["value"]
    requests.post(profile_url, json={"bodyweight": weight})
    speech_output = f"A bodyweight of {weight} is just perfect!"
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def set_age(intent_request):
    session_attributes = {}
    card_title = "Age response"
    age = intent_request["intent"]["slots"]["Number"]["value"]
    requests.post(profile_url, json={"age": age})
    speech_output = f"I am less than {age} years old."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the Productivity bot! I hope you were productive."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
