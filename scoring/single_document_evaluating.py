from rouge_score import rouge_scorer
import pandas as pd
from final_year_project_django.ingestion import gpt_3_summary, get_t5_summary
import os
import numpy as np
import statistics
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
os.environ["TOKENIZERS_PARALLELISM"] = "false"
#
# s1 = ''''''
# s2 = gpt_3_summary(s1)
# s3 = get_t5_summary(s1)
# scores = scorer.score(s1,s2)
# scorest5 = scorer.score(s1,s3)
# # print(scorer)
# print("gpt", scores)
# print("t5", scorest5)

df = pd.read_csv('data/cnn_dailymail/test.csv')

gpt_recall = []
t5_recall = []

gpt_precision = []
t5_precision = []

for row in df.head(15).iterrows():
    # print(row[0])

    reduced_actual = row[1][2]
    x = row[1][1]
    reduced_summary_t5 = get_t5_summary(x)

    reduced_summary_gpt = gpt_3_summary(row[1][1])

    full_actual = row[1][2]

    # try:
    # Test 1
    #     print("T5",scorer.score(reduced_actual, reduced_summary_t5))
    scores = scorer.score(reduced_actual, reduced_summary_t5)
    t5_recall.append(scores['rougeL'].recall)
    t5_precision.append(scores['rougeL'].precision)
        # print(foo['rouge1'].precision)
        # print(foo['rouge1'].recall)
        # Test 2
        # print(scorer.score(full_actual, reduced_summary))
        # GPT test
    scores = scorer.score(reduced_actual, reduced_summary_gpt)
    gpt_recall.append(scores['rougeL'].recall)
    gpt_precision.append(scores['rougeL'].precision)

    # except:
    #     print("Error")
    #     pass
print("T5")
print(statistics.mean(t5_precision))
print(statistics.mean(t5_recall))

print("GPT")
print(statistics.mean(gpt_recall))
print(statistics.mean(gpt_precision))
# T5
# 0.3280458914537447
# 0.38348829488462133
# GPT
# 0.07645789054308325
# 0.0943009619335005