from rouge_score import rouge_scorer
import pandas as pd
from final_year_project_django.ingestion import gpt_3_summary, get_t5_summary
import os
import numpy as np
import statistics
scorer = rouge_scorer.RougeScorer(['rougeL','rouge1'], use_stemmer=True)
os.environ["TOKENIZERS_PARALLELISM"] = "false"


df = pd.read_csv('data/cnn_dailymail/test.csv')

gpt_recall_rougeL = []
t5_recall_rougeL = []
gpt_precision_rougeL = []
t5_precision_rougeL = []


gpt_recall_rouge1 = []
t5_recall_rouge1 = []
gpt_precision_rouge1 = []
t5_precision_rouge1 = []

for row in df.head(10).iterrows():
    # print(row[0])

    reduced_actual = row[1][2]
    x = row[1][1]
    reduced_summary_t5 = get_t5_summary(x)

    try:
        reduced_summary_gpt = gpt_3_summary(row[1][1])


        full_actual = row[1][2]

    # try:
    # Test 1
    #     print("T5",scorer.score(reduced_actual, reduced_summary_t5))
        scores = scorer.score(reduced_actual, reduced_summary_t5)
    except:
        print('error')
    t5_recall_rougeL.append(scores['rougeL'].recall)
    t5_precision_rougeL.append(scores['rougeL'].precision)

    t5_recall_rouge1.append(scores['rouge1'].recall)
    t5_precision_rouge1.append(scores['rouge1'].precision)

    scores = scorer.score(reduced_actual, reduced_summary_gpt)
    gpt_recall_rougeL.append(scores['rougeL'].recall)
    gpt_precision_rougeL.append(scores['rougeL'].precision)

    gpt_recall_rouge1.append(scores['rouge1'].recall)
    gpt_precision_rouge1.append(scores['rouge1'].precision)
    # except:
    #     print("Error")
    #     pass
print("T5")
print("Precision Rouge L",statistics.mean(t5_precision_rougeL))
print("Recall Rouge L", statistics.mean(t5_recall_rougeL))
print('-----')
print("Precision Rouge 1",statistics.mean(t5_precision_rouge1))
print("Recall Rouge 1", statistics.mean(t5_recall_rouge1))
print('-----'*3)
print("GPT")
print("Precision RougeL", statistics.mean(gpt_precision_rougeL))
print("Recall RougeL", statistics.mean(gpt_recall_rougeL))
print('-----')
print("Precision Rouge1", statistics.mean(gpt_precision_rouge1))
print("Recall Rouge1", statistics.mean(gpt_recall_rouge1))
