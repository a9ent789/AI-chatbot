#Tecumseh McMullin CSC444

#libraries
import os
import tkinter as tk
import random
import datetime
import pyttsx3

engine = pyttsx3.init()

#importing text area with scrollbar
from tkinter import scrolledtext
#importing the ability to read the gguf files.
from llama_cpp import Llama

#LLM
model_path = "Maid.gguf"

#version
version = 1.5

#Date
todays_date = datetime.datetime.now().strftime("%m-%d-%Y")

def speak(text):
    engine.say(text)
    engine.runAndWait()

#function to load model
def load_model():
    if not os.path.isfile(model_path):
        print("Error: using the model path " + model_path + " No Model with that name at location.")
        exit()

    #loads model
    global model
    #parameters for loading the model.
    model = Llama(
        model_path=model_path,
        seed=random.randint(1, 2**31),
    )

#function for model responses.
def generate_response(model, input_tokens, prompt_input_text, text_widget):
    # Display input from user
    text_widget.insert(tk.END, '\n\nMaster: ' + prompt_input_text + '\n')

    # Output the text into the GUI
    output_response_text = b""
    count = 0
    output_response_text = b"\n\nMaid: "
    text_widget.insert(tk.END, output_response_text)

    # Accumulate response text to be spoken
    response_to_speak = ""

    # Loop through model generation
    for token in model.generate(input_tokens, top_k=40, top_p=.95, temp=72, repeat_penalty=1.1):
        response_text = model.detokenize([token])
        output_response_text = response_text.decode()
        response_to_speak += output_response_text + " "  # Accumulate text to be spoken
        text_widget.insert(tk.END, output_response_text)
        text_widget.see(tk.END)
        root.update_idletasks()
        count += 1

        if count > 5000 or (token == model.token_eos()):
            break

        text_area_main_user_input.delete('1.0', tk.END)

    # Speak the accumulated response text
    speak(response_to_speak)

#Send message function, this takes the input of the user then uses it.
def send_message():
    user_prompt_input_text = text_area_main_user_input.get('1.0', 'end-1c')
    user_prompt_input_text = user_prompt_input_text.strip()
    byte_message = user_prompt_input_text.encode('utf-8')
    input_tokens = model.tokenize((b"### Human: " + byte_message + b"\n### Maid: I am here to serve you master and make your life easier "))
    print("Input Tokens: ", input_tokens)

    #this is how the users input is used, by running the generate response function.
    generate_response(model, input_tokens, user_prompt_input_text, text_area_display)

#main function that shows all the stuff and does things
def main():

    #loads model.
    load_model()

    #the entire surrounding area of the GUI
    global root
    root = tk.Tk()
    root.title("ButterFingers -v" + str(version) + " - " + todays_date)

    #the frame
    frame_display = tk.Frame(root)

    scrollbar_frame_display = tk.Scrollbar(frame_display)

    #where the user input is
    global text_area_main_user_input
    text_area_main_user_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=125, height=10)

    #display for the text area
    global text_area_display
    text_area_display = scrolledtext.ScrolledText(frame_display, width=100, height=25, yscrollcommand=scrollbar_frame_display.set)

    #colors to use
    teal = "#C5EBEF"
    dark_grey = "#202020"
    light_grey = "#767878"

    #Text area
    text_area_display.config(background=dark_grey, foreground=teal, font=("Courier", 12))
    scrollbar_frame_display.config(command=text_area_display.yview)

    #send button to give the box instructions
    button_send_message = tk.Button(root, text="Send Message", command=send_message)

    avatar_frame = tk.Frame(root)
    avatar_frame.pack(side=tk.LEFT)

    # Load the avatar image
    avatar_image = tk.PhotoImage(file="Maid2.png")

    # Display the avatar
    avatar_label = tk.Label(avatar_frame, image=avatar_image, background=light_grey)
    
    
    #packing all of the different visuals
    text_area_display.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar_frame_display.pack(side=tk.RIGHT, fill=tk.Y)
    frame_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    button_send_message.pack()
    text_area_main_user_input.pack(pady=10, padx=10, fill=tk.X, expand=True)
    avatar_label.pack(pady = 10, padx = 10)

    root.mainloop()

#runs the main function
main()