Demo: The program will use only the specified text file to answer questions 
by making calls to gpt API and passing the question and document as parameters

 % python3 ask_file.py
Ask a question: What is my name?

Answer:
Your name is Arul.

% cat notes.txt
notes.txt

The company was founded in 2018.
Its headquarters are in Austin.
The CEO is Jane Smith. Your name is Arul and you are learning python.

% python3 ask_file.py
Ask a question: Who is the CEO of the company?

Answer:
Jane Smith.
