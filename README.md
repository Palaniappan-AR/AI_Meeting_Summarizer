# AI_Meeting_Summarizer

**Overview**<br />
This project uses OpenAI's GPT API to process meeting transcripts. It can automatically summarize transcripts, extract action items, classify the meeting type, and analyze the sentiment. The system dynamically calls specific functions based on the transcript content and returns the results in a user-friendly format.

**Features**<br />
1. **Extract Action Items:** Identifies tasks and responsibilities discussed in the meeting. <br />
2. **Classify Meeting Type:** Categorizes meetings into predefined types like "Stand-up" or "Planning."<br />
3. **Analyze Sentiment:** Determines whether the meeting sentiment is Positive, Neutral, or Negative.<br />

**Function Definitions in API**<br />
Each function is described with required parameters, ensuring dynamic responses based on meeting content.

**OpenAI ChatCompletion**<br />
Sends the transcript to the GPT model, which decides on the necessary function call and retrieves corresponding results.
