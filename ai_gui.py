import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
from getpass import getpass

# Set up HuggingFace API token
repo_id="tiiuae/falcon-7b-instruct"
huggingface_api_token="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"
llm = HuggingFaceHub(huggingfacehub_api_token=huggingface_api_token,
                     repo_id=repo_id,
                     model_kwargs={"temperature":0.7, "max_new_tokens":500})

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(llm=llm, prompt=prompt)

# Create the main application window
root = tk.Tk()
root.title("AI Assistant")

root.geometry("800x600")


# Function to process the input and display the output
def get_answer():
    question = question_entry.get()
    if question.strip() == "":
        messagebox.showwarning("Input Error", "Please enter a question.")
        return

    try:
        output = chain.run({"question": question})
        answer_text.configure(state='normal')
        answer_text.delete(1.0, tk.END)
        answer_text.insert(tk.END, output)
        answer_text.configure(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Create and place the input field
question_label = tk.Label(root, text="Enter your question:", font=("Arial", 14))
question_label.pack(pady=10)

question_entry = tk.Entry(root, width=100, font=("Arial", 14))
question_entry.pack(pady=10)

# Create and place the submit button
submit_button = tk.Button(root, text="Get Answer", command=get_answer, font=("Arial", 14))
submit_button.pack(pady=20)

# Create and place the output area
answer_label = tk.Label(root, text="Answer:", font=("Arial", 14))
answer_label.pack(pady=10)

answer_text = scrolledtext.ScrolledText(root, width=90, height=20, wrap=tk.WORD, font=("Arial", 14))
answer_text.pack(pady=10)
answer_text.configure(state='disabled')

# Start the Tkinter event loop
root.mainloop()