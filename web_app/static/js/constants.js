const action_name = "action_greet_user";
const rasa_server_url = "https://rasa.jiva.live/webhooks/rest/webhook";
const sender_id = uuidv4();
const rasa_action_trigger_URL=`https://rasa.jiva.live/conversations/${sender_id}/execute`;
const rasa_customActionTrigger_URL="https://action.jiva.live/webhook/";
