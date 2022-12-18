from typing import Any, Text, Dict, List
from urllib import response
from . import db_functions, debug_host
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
# from pythonping import ping
from . import ssh_connect
import requests


# import asyncio, asyncssh, sys
# import platform    # For getting the operating system name
# import subprocess  # For executing a shell command


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_custom_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Thank you")
        # teasers = db_functions.show_brain_teaser()
        # dispatcher.utter_message(text=str(teasers))

        return []


class ActionChromeOSQNA(Action):

    def name(self) -> Text:
        return "action_chromeos_qna"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # =====================================
        # Exit the loop when below words are found.

        # =======================
        stop_bot=['stop','stop flow','back','exit','stop']
        if tracker.get_slot('chromeos_question') in stop_bot:
            dispatcher.utter_message(text="Thanks for using our service")
            dispatcher.utter_message(text="If need more assistance type 'help' ")

            return [SlotSet("chromeos_question", None)]

        question = tracker.get_slot('chromeos_question')
        data = {
            "client": "chromeos",
            "input_text": question
        }
        r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        result = r.json()
        lines = str(result).splitlines()
        last_line = lines[-1]
        result = result[:result.rfind('\n')]
        # teasers = db_functions.show_brain_teaser()
        # html_text = result.replace("\n", "<br>")
        # url_link = '<a href="' + last_line + '" target="_blank">' + last_line + '</a>'

        dispatcher.utter_message(text=result)
        dispatcher.utter_message(text=last_line)

        # dispatcher.utter_message(text=html_text)
        # dispatcher.utter_message(text=url_link)
        return [SlotSet("chromeos_question", None), FollowupAction('chromeos_qna_form')]


class ActionChromeOSQNAIntentTrigger(Action):

    def name(self) -> Text:
        return "action_chromeos_qna_intent_trigger"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # question = tracker.get_slot('chromeos_question')
        # data = {
        #     "client": "chromeos",
        #     "input_text": question
        # }
        # r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        # result = r.json()
        # lines = str(result).splitlines()
        # last_line = lines[-1]
        # # teasers = db_functions.show_brain_teaser()
        # dispatcher.utter_message(text=str(result))
        # dispatcher.utter_message(text=last_line)
        # return [UserUttered("/chromeos_knowledge_base", intent={'name': 'chromeos_knowledge_base', 'confidence': 1.0})]
        return []


class ActionStarTreeQNA(Action):

    def name(self) -> Text:
        return "action_startree_qna"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # =====================================
        # Exit the loop when below words are found.

        # =======================
        stop_bot=['stop','stop flow','back','exit','stop']
        if tracker.get_slot('startree_question') in stop_bot:
            dispatcher.utter_message(text="Thanks for using our service")
            dispatcher.utter_message(text="If need more assistance type 'help' ")

            return [SlotSet("startree_question", None)]



        question = tracker.get_slot('startree_question')
        data = {
            "client": "startree",
            "input_text": question
        }
        r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        result = r.json()
        lines = str(result).splitlines()
        last_line = lines[-1]
        result = result[:result.rfind('\n')]
        # teasers = db_functions.show_brain_teaser()

        # html_text = result.replace("\n", "<br>")
        # url_link = '<a href="' + last_line + '" target="_blank">' + last_line + '</a>'

        dispatcher.utter_message(text=result)
        dispatcher.utter_message(text=last_line)

        # dispatcher.utter_message(text=html_text)
        # dispatcher.utter_message(text=url_link)
        return [SlotSet("startree_question", None), FollowupAction('startree_qna_form')]


class ActionStarTreeQNAIntentTrigger(Action):

    def name(self) -> Text:
        return "action_startree_qna_intent_trigger"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # question = tracker.get_slot('startree_question')
        # data = {
        #     "client": "startree",
        #     "input_text": question
        # }
        # r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        # result = r.json()
        # lines = str(result).splitlines()
        # last_line = lines[-1]
        # # teasers = db_functions.show_brain_teaser()
        # dispatcher.utter_message(text=str(result))
        # dispatcher.utter_message(text=last_line)

        # return [UserUttered("/startree_knowledge_base", intent={'name': 'startree_knowledge_base', 'confidence': 1.0})]
        return []


class ShowBrainTeaser(Action):

    def name(self) -> Text:
        return "action_show_brain_teaser"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        result = db_functions.show_brain_teaser()
        question = result["question"]
        question_id = result["q_id"]
        # dispatcher.utter_message(text=question)
        # input_channel = tracker.get_latest_input_channel
        # print(input_channel)

        buttons = []
        for d in result["options"]:
            fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
            buttons.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})
        dispatcher.utter_message(text=question, buttons=buttons)

        return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]


class ValidateBrainTeaserAnswer(Action):

    def name(self) -> Text:
        return "action_validate_brain_teaser_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        brain_teaser_answer = tracker.get_slot('brain_teaser_answer')
        question_id = tracker.get_slot('question_id')

        if db_functions.brain_teaser_answer_check(q_id=question_id, answer=brain_teaser_answer):
            dispatcher.utter_message(text="Great Job! Let's move forward.")
        else:
            dispatcher.utter_message(text="Sorry, that was incorrect. Let's move forward.")

        return [SlotSet("brain_teaser_answer", None), SlotSet("question_id", None)]


class ActionDebugHostValidate(Action):

    def name(self) -> Text:
        return "action_debug_host_validate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_value = tracker.get_slot("debug_host_proceed")
        if slot_value == 'No':
            dispatcher.utter_message(text=f"Operation canceled.")
        elif slot_value == 'Yes':
            # result = ''
            # dispatcher.utter_message(text= f"fetching results.. please wait..")
            # Option for the number of packets as a function of

            host_value = tracker.get_slot("debug_host_name")
            username_value = tracker.get_slot("debug_host_username")
            password_value = tracker.get_slot("debug_host_password")
            ssh_command_value = tracker.get_slot("ssh_command_option")

            # buttons =[]
            # for d in result["options"]:
            #     fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
            #     buttons.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})
            result = ssh_connect.ssh_exec_command(host=host_value, username=username_value, password=password_value,
                                                  command=ssh_command_value)
            # print(("*"*100) + "\n" + str(result))
            dispatcher.utter_message(text=result)
        else:
            dispatcher.utter_message(text="Didn't expect that input, please try again.")
            # if ssh_connect.ssh_conn_check(host=host_value, username=username_value, password=password_value, command='hostname'):
            #     # try:
            #     #     command = 'ss -ltn'
            #     #     # result = asyncio.get_event_loop().run_until_complete(ssh_connect.run_client(host=host_value, username=username_value, password=password_value, command=command))
            #     #     result = ssh_connect.ssh_exec_command(host=host_value, username=username_value, password=password_value, command=command)
            #     #     # result = ' '.join([str(elem)+'\n' for elem in result_list])
            #     # # except (OSError, asyncssh.Error) as exc:
            #     # except Exception as exc:
            #     #     result = 'SSH connection failed: ' + str(exc)
            #         # sys.exit()
            #     dispatcher.utter_message(text= 'Connection Successful. Executing command..')
            #     # command_list = ['hostname', 'ss -ltn', 'cat /proc/meminfo', 'df']
            #     # buttons =[]
            #     # for d in command_list:
            #     #     fill_slot = "{'ssh_command_option' : '" + d + "'}"
            #     #     buttons.append({"title": d, "payload": f"/intent_ssh_command_option {fill_slot}"})
            #     # dispatcher.utter_message(text="", buttons=buttons)
            #     result = ssh_connect.ssh_conn_check(host=host_value, username=username_value, password=password_value, command=ssh_command_value)
            #     dispatcher.utter_message(text= result)
            # else:
            #     dispatcher.utter_message(text= "SSH Connection failed")
        return [SlotSet("debug_host_name", None), SlotSet("debug_host_username", None),
                SlotSet("debug_host_password", None), SlotSet("debug_host_proceed", None),
                SlotSet("ssh_command_option", None)]

# class ActionDebugHostExecuteCommand(Action):

#     def name(self) -> Text:
#         return "action_debug_host_execute_command"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         host_value = tracker.get_slot("debug_host_name")
#         username_value = tracker.get_slot("debug_host_username")
#         password_value = tracker.get_slot("debug_host_password")
#         ssh_command_value = tracker.get_slot("ssh_command_option")

#         result = ssh_connect.ssh_conn_check(host=host_value, username=username_value, password=password_value, command=ssh_command_value)
#         dispatcher.utter_message(text= result)
#         return [SlotSet("debug_host_name", None), SlotSet("debug_host_username", None), SlotSet("debug_host_password", None), SlotSet("debug_host_proceed", None), SlotSet("ssh_command_option", None)]
