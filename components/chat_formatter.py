from transformers import AutoTokenizer
from loguru import logger

class ChatFormatter:
    def __init__(self, model_name:str):    
        logger.debug(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if not self.tokenizer.chat_template:
            # default mistral chat template
            logger.warning('No chat template detected, using default template.')
            self.tokenizer.chat_template = "{{ bos_token }}{% for message in messages %}{% if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}{% endif %}{% if message['role'] == 'user' %}{{ '[INST] ' + message['content'] + ' [/INST]' }}{% elif message['role'] == 'assistant' %}{{ message['content'] + eos_token + ' ' }}{% else %}{{ raise_exception('Only user and assistant roles are supported!') }}{% endif %}{% endfor %}"
            self.needs_formatting = True
        else:
            logger.info(f'Chat template detected. Message formatting should be handled by server.')
            self.needs_formatting = False
        self.model_name = model_name

    def subset_user_assistant_pairs(self, messages):
        pairs = []
        pair = []

        for message in messages:
            pair.append(message)
            if message['role'] == 'assistant':
                pairs.append(pair)
                pair = []
        
        return pairs
    
    def apply_chat_template(self, messages, tokenize=False):
        if self.needs_formatting:
            last_two = messages[-2:]
            system_plus_user = [{'role':'user','content':f"### System Setting: \n {last_two[0]['content']}" + f"### User Request: \n {last_two[1]['content']}"}]
            messages = messages[:-2] + system_plus_user 
            formatted_messages = []            
            formatted_messages=[{
                "role": 'user', 
                "content": self.tokenizer.apply_chat_template(messages, tokenize=tokenize)
            }]
            return formatted_messages
        else:
            return messages

    def replace_inst_tags_with_emoji(self, text:str):
        if text:
            # Define the robot emoji
            robot_emoji = '🤖'

            # Replace the [INST] and [/INST] tags with the robot emoji
            # We use the 'split' method to break the text at each tag and then 'join' with the emoji
            return text.replace("[INST]", robot_emoji).replace("[/INST]", "")
        else: return ''