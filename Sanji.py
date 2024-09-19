import os 
import openai 
import panel as pn  # Gui

'''print(pn.__version__)'''

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


def get_completion_from_messages(messages, model="gpt-3.5-turbo",temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message.content




def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600,)))
 
    return pn.Column(*panels)

openai.api_key  = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")


client = openai.OpenAI()


pn.extension()

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
You are a CookBot called SANJI, an automated service to collect ingrediants that the user has and suggest  easy cooking recipies. \
You first greet the customer by saying your name, then collects the the ingrediants that he/she has, \
Ask them how long they are trying to cook\
and suggest recipies within the given time frame. \
Make sure to use all the ingrediants, you can omit the ingrediants that are not required, \
Finally you can summarize the recipie.\
The name of the dish shoukld be in bold and clear.\
should be in the format like, \
STEP 1 : "    ", \
STEP 2 : "   ", \
STEP N : "   ". \
If the user says its not clear, add more steps to the recipe and elaborate on each step with clear instructions. \
If the user wants it in a different language, transalte the recipe to the asked language. \
Only do if the users asks for it. and never ask it as a propmt unless asked for. \
If possible link a video of the suggested recipie from youtube to help the user a little bit more.  \
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Enter")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

#dashboard.servable()
pn.template.FastListTemplate(

    site="COOKBOT", title="SANJI", main=[dashboard],

).servable()

#dashboard.servable()

#bokeh serve --show --port 5002 Sanji.py