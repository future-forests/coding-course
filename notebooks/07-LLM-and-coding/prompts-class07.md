# Prompts used to make the Class 7 slides

These are the prompts I sent to an LLM (Claude) to help build the Class 7 presentation "Using LLMs in coding", in the order I sent them.

---

## Prompt 1 (main prompt)

*Attached: the cover of the Stanford HAI "Artificial Intelligence Index Report 2026", and a slide titled "Tool-augmented LLMs for data analysis" (spreadsheet upload → converted to prompt in background → LLM → code output → code executor).*

Can you make a powerpoint for the class 7 of this course: https://github.com/future-forests/coding-course/tree/main

The idea is to introduce how to use LLM in coding and make a data analysis exercise with a take-out message: stay skeptical about the use of LLM, don't trust them blindly.

How I see the presentation (feel free to adapt it to make it coherent), each point is a slide:

* Slide 1: Explain what this class is about (but don't make a slide with all the different sections of the presentation), says it is hard to make a class about that topic because things are moving fast, I know that what I show here will be outdated in two months but I spent tens of hours to make the best presentation you can find online

* Slide 2: First figure in  https://communities.sas.com/t5/SAS-Communities-Library/Where-does-GenAI-fit-within-the-AI-landscape/ta-p/915000 with the different circles but extend it:
   * Artificial intelligence: umbrella term that means the broad science of mimicking human abilities, say it started by Alan Turing in ...
   * Machine learning: that trains a machine how to learn, started by ... in ...
   * Deep learning: machine learning that uses neural networks (vague resemblance to the brain), started by ... in ...
   * GenAI: Deep learning models that generate new content (here we focus on LLM that deals with text because we are dealing with codes), started by the google engineer paper in 2017
* Slide 3: LLMs are neural netwroks trained to predict the next word (or token), gives a figure that show a prompt , also called input tokens, ("It is a beautiful day today, the sky is ...") -> LLM -> prediction (10% blue, 7% clear, 4% beautiful, ...), show it is actually not words but a sequence of integer tokens like [3206, 382, 261, 6107, 2163, 4044, 11, 290, 17307, 382]

* Slide 4: How LLM is made?
   * LLMs are a type of neural network. The really basic version of how a neural network works is this: you have a program with billions of dials that you can tweak, and those dials (called the “weights”) determine what the output of the program is.
   * We don’t write an LLM like we do other software. Instead, we write a program that trains the LLM. So there are two programs: the training program, and the LLM itself. But we don’t know why it works as well as it does.
* Slide 5: Training part:
   * Pre-training: The model is exposed to massive amounts of code (and often natural language) to learn (1) syntax rules, (2) common coding patterns, (3) relationships between code and comments
   * More training:
      * Fine-tuning on specific domain (like scientific Python),
      * RLHF (Reinforcement Learning from Human Feedback): Aligning outputs with human preferences,
      * Instruction tuning**: Teaching the model to follow human instructions
      * Reinforcement Learning from Verifiable Rewards—it is the reason we have models that are so good at coding, and mathematics, and finding security holes. While the model is being trained, you run exercises to see how good it is—and the strongest performers get their weights reinforced for the next round. It’s like an evolutionary process that you run.
      * ...
* Slide 6: LLM and coding
   * The model doesn’t “understand” code in the way humans do, but it has learned enough patterns to generate syntactically correct and often semantically meaningful code.
   * Really good at it, cite the artificial intelligence index report (Al capability is not plateauing. It is accelerating and reaching more people than ever. Industry produced over 90% of notable frontier models in 2025, and several of those models now meet or exceed human baselines on PhD-level science questions, multimodal reasoning, and competition mathematics. On a key coding benchmark—SWE-bench Verified—performance rose from 60% to near 100% of meeting the human baseline in a single year. Organizational adoption reached 88%, and 4 in 5 university students now use generative Al.) - add the report cover I shared in the image
* Slide 7, 8 and 9: LLM tools are application build on tops of LLMs: Chatbots and Agents (Agent = LLM (could be Chatbot) + tool). Explain with one graph what they are:
   * User prompt -> LLM, System prompt (see https://github.com/openai/codex/blob/rust-v0.114.0/codex-rs/core/templates/model_instructions/gpt-5.2-codex_instructions_template.md) -> LLM -> result
   * For agents (next slide) keep same diagram but add a loop (LLM -> system prompt (reasoning/thinking) -> write python tool -> extract or produce data -> LLM)
   * Third slide adapt the second screenshot to show an example
* Slide 10: List of chatbots for the exercise (make a table with links for Duck.ai, Mistral, ChatGPT, Claude, Gemini and say their provider)
* Exercise (work in progress)

* Conclusion:
   * Now what you are using
   * Stay skeptical
* Next class: 
   * Responsible Use of Generative AI in Assisted Coding
   * Prompting tips
   * VS code + CoPilot example
   * LLM benchmark 
* make a list of references used:
   * https://en.wikipedia.org/wiki/Artificial_intelligence and so many others
   * https://coderefinery.github.io/coding-with-ai
   * https://www.lesswrong.com/posts/dww6cpbo2XoKbsxyw/where-do-chatbots-come-from-what-i-wish-everyone-knew-about
   * https://communities.sas.com/t5/SAS-Communities-Library/Where-does-GenAI-fit-within-the-AI-landscape/ta-p/915000
   * https://simonwillison.net/
   * Beyond Vibe Coding: Responsible AI-Assisted Data Analysis for Reproducible Research by Ilona Lipp


For layout use a simple template but with dark background, verify that the presentation is coherent, that text are not overlaying with other objects and text is readable

---

## Prompt 2

*Attached: a sketch showing a column of input tokens → Model → the same column of tokens plus one new output token.*

Please in the slide 3, make it less fancy:

* Title: LLMs are neural networks trained to predict the next word (or token)
* Start by the first figure and explain it in one sentence, and then give an example "It is a beautiful day today, the sky is..." [in integers token 3206, 382, 261, 6107, 2163, 4044, 11, 290, 17307, 382]-> LLM -> prediction (10% blue, 7% clear, 4% beautiful, ...), don't show integer tokens for predictions, neither a bar chat, I really need (sentence -> LLM -> prediction) also I didn't like to call it prompt or input the sentence, how should I call it?

---

## Prompt 3

* Slide 4 just start by saying on the right before the rest (We don’t write an LLM like we do other software. Instead, we write a program that trains the LLM.)
* Slide 7, give the link to the system prompt, take a simpler example that doesn't use agents like "plot"
* Do you think the loop representation at slide 8 makes sense?

---

## Prompt 4

Yes please do

---

## Prompt 5

can you make a thinking box inside LLM then before calling the agent? What do you think? Also can you make the slide 9 match the loop in slide 8, what is inside the agent what is outside?

---

## Prompt 6

*Attached: three annotated figures ("Trap 1", "Trap 2", "Trap 3") from a tree and squirrel dataset.*

I prefer how was slide 9 before please bring it back.

* for slide 6, also says that data analysis is not only about coding, it's also about problem thinking, creativity. How good are they for that? let's try an exercise


Please add a disclaimer at the first slide that says that I have been using a LLM to make this presentation, It is always dubious to speak about LLM when using a LLM, but around 95% of what you will see are my ideas and my research using literrature from experts, and for full transparency you can see the prompt I use to make this slides in [URL file], I will modify the URL, just give me the full prompt I sent you.

For the exercise, please copy the slides 23, 24, 25 than put the 3 traps using the images I share here instead

Make a slide after the exercise about the problems of using AI, just mention some with a rectangle, a small sentence and a reference if they want to know more:

* Ethics and safety? The tool itself isn't dangerous, because it doesn't have will or desire, but people can use this tool to do bad (reference: [AI safety](https://en.wikipedia.org/wiki/AI_safety))
* Environment? not enough top-down research. electricity and water is peanut compared to meat consumption (calculate how much one querry emit CO2 and use water compare to a steak and reference https://ourworldindata.org/how-much-energy-do-data-centers-and-artificial-intelligence-use), says that can replace energy-intensive weather forecast model
* Political? speaks that because of the data that they need to be trained, only a few company can allow doing that -> few are in powers (no reference needed for this one)

---

## Promt 7

Can you combine slide 11 and 12 together and make it coherent, like a real class exercise. I decided to go back to the original superheroes question instead of the tree dataset. Start with the data (shows the columns using the same image as one attached), then research question, then what they should do (upload your .csv (duck.ai doesn't accept .csv so copy paste the table), make relevant plots, try to understand what are the different decisions that were taken), say after 15 min we discuss our results and one by one we share them on zoom. 

research question: "Are there differences between
(1) popular and (2) nonpopular superheroes regarding their ability to
recover from injury?"

Replace slide 13 with something like slide 26 in the pdf I shared. put the questions, I will count on the black board. Part 2 and 3 are just yes or no answer. Then a rectangle that says, let's share one by one our result on zoom

I have shared new figures for slides 13, 14, 15

Can you divide slide 17 into 5 rectangle: safety risks, ethical issues, environmental impacts, Dominance by tech giants (instead of power), others (leave this one empty for now, I will work on it after). keep the text for ethics and safety in safety risks, add this quote from Hinton (""10 to 20 per cent chance" that AI would cause human extinction within the next three decades"). for ethical speak about learning methods, privacy and copyright issues, I will find a source for this, just let me a space to put it. Add some data centers implementation are really problematic in the environment one.