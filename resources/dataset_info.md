# Dataset Information

## Overview

This project uses the **Stanford Question Answering Dataset (SQuAD) v2.0** for demonstrating semantic search capabilities. SQuAD is a reading comprehension dataset consisting of questions posed by crowdworkers on a set of Wikipedia articles.

## Dataset Details

- **Name**: SQuAD v2.0
- **Source**: [Hugging Face Datasets](https://huggingface.co/datasets/squad_v2)
- **Size**: ~130k examples (Train split used)
- **Format**: JSON / Arrow (via Hugging Face)
- **Description**: SQuAD2.0 combines the 100,000 questions in SQuAD1.1 with over 50,000 unanswerable questions written adversarially by crowdworkers to look similar to answerable ones.

## Data Structure

For the purpose of this vector search demo, we focus on the **context** field.

```json
{
  "id": "56be85543aeaaa14008c9063",
  "title": "Beyoncé",
  "context": "Beyoncé Giselle Knowles-Carter (/biːˈjɒnseɪ/ bee-YON-say; born September 4, 1981) is an American singer, songwriter, record producer and actress...",
  "question": "When did Beyonce start becoming popular?",
  "answers": {
    "text": ["in the late 1990s"],
    "answer_start": [269]
  }
}
```

## Usage in Project

1. **Loading**: The dataset is loaded using the `datasets` library:

   ```python
   dataset = load_dataset("squad_v2", split="train")
   ```

2. **Preprocessing**: We extract unique `context` entries to avoid duplicates.

   ```python
   contexts = list(set(dataset['context']))
   ```

3. **Embedding**: Each unique context is converted into a vector embedding using OpenAI's `text-embedding-3-large` model.

4. **Indexing**: These vectors are upserted into a Pinecone index for fast similarity search.

## References

- **Dataset Page**: [https://rajpurkar.github.io/SQuAD-explorer/](https://rajpurkar.github.io/SQuAD-explorer/)
- **Hugging Face**: [https://huggingface.co/datasets/squad_v2](https://huggingface.co/datasets/squad_v2)
- **Paper**: "Know What You Don't Know: Unanswerable Questions for SQuAD" (Rajpurkar et al., 2018)
