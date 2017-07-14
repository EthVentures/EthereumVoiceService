"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema and Sample Utterances for this skill, as well
as testing instructions are located at https://github.com/EthVentures/AlexaSatori
"""
from __future__ import print_function
from satori.rtm.client import make_client, SubscriptionMode
import sys
import time
import threading
import math

endpoint = "wss://open-data.api.satori.com"
appkey = "YOUR-KEY-HERE" #https://developer.satori.com/#/signup
channel = "complete-ethereum-market-data"


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Streaming Ether, an Alexa Skill powered by Satori Lyve Data. "

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "To get the market prices of ether, you may ask for the latest prices. "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Goodbye"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_ether_tick():
    with make_client(endpoint=endpoint, appkey=appkey) as client:

        tick = []
        event = threading.Event()

        def read_callback(reply):
            tick.append(reply)
            event.set()

        client.read(channel, callback=read_callback)

        if not event.wait(2):
            print('Read request timed out')
        else:
            price = tick[0]['body']['message']['price']
            exchange = tick[0]['body']['message']['exchange']
            print(price)
            print(exchange)
        print("Prices updated")
        return

def ask_support_exchanges(intent, session):
    """ responds support exchanges.
    """
    session_attributes = {}
    reprompt_text = None

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_output = "Powered by open source tools built by eeth ventures,  latest prices are updated from all major crypto currency exchanges."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def ask_price_ether(intent, session):
    with make_client(endpoint=endpoint, appkey=appkey) as client:

        dollars, cents = 0, 0
        tick = []
        event = threading.Event()

        def read_callback(reply):
            tick.append(reply)
            event.set()

        client.read(channel, callback=read_callback)
        if not event.wait(2):
            print('Read request timed out')
        else:
            price = tick[0]['body']['message']['price']
            exchange = tick[0]['body']['message']['exchange']
            dollars = int(price)
            cents = int((price - dollars)*100)   #room for improvement, truncates for now instead of rounding fractional pennies

        session_attributes = {}
        reprompt_text = None

        speech_output = "Last Reported Price was " + str(dollars) + \
                            " dollars and " + str(cents) + " cents, reported by the " + exchange + " exchange."
        should_end_session = False

        return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    session_attributes = {}
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])



def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AskPriceEther":
        return ask_price_ether(intent, session)
    elif intent_name == "AskSupportedExchanges":
        return ask_support_exchanges(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
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


# --------------- Main handler ------------------

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
