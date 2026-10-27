# Class 6 — survey-processing script (Class 5b workflow).
# Same idea as station-processing.py / post-processing.py:
# Class 5b as a .py file with # %% cells.
# Figures go to PNG with plt.savefig instead of plt.show().

# %%
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plot_likert
import spacy
import statsmodels.formula.api as smf
from scipy import stats
from spacy.matcher import Matcher

# %%
AnswersPath = '../../processed_data/diana_answers.csv'
CodebookPath = '../../processed_data/diana_codebook.csv'
FigDir = 'figures'

os.makedirs(FigDir, exist_ok=True)

# %%
# 1. Load answers and codebook
Answers = pd.read_csv(AnswersPath)
Codebook = pd.read_csv(CodebookPath)
print(Answers.shape)
print(Codebook.shape)

# %%
# 2. Single — age class (drop code 0 = no answer)
Age = Answers['F26'].replace({0: np.nan})
AgeShare = Age.value_counts(normalize=True) * 100
print(AgeShare)

plt.bar(x=AgeShare.index, height=AgeShare)
plt.xlabel('Age class (code; see codebook)')
plt.ylabel('Share of respondents (%)')
plt.title('Age of the participants')
plt.tight_layout()
plt.savefig(f'{FigDir}/age_share.png')
plt.close()
print(f'Saved {FigDir}/age_share.png')

# %%
# Education (F28) — same pattern
Education = Answers['F28'].replace({0: np.nan})
EduShare = Education.value_counts(normalize=True) * 100

plt.bar(x=EduShare.index, height=EduShare)
plt.xlabel('Answer code')
plt.ylabel('Share of respondents (%)')
plt.title('F28')
plt.tight_layout()
plt.savefig(f'{FigDir}/education_share.png')
plt.close()
print(f'Saved {FigDir}/education_share.png')

# %%
# 3. Multi-binary — how did you get your forest?
AcquiredCols = ['F1_1_a', 'F1_1_b', 'F1_1_c', 'F1_1_d', 'F1_1_e']
AcquiredShare = Answers[AcquiredCols].mean() * 100
AcquiredLabels = [
    'I inherited the forest.',
    'I bought the forest.',
    'I received the forest through marriage.',
    'I received the forest as a gift.',
    'I received the forest in another way.',
]
print(AcquiredShare)

plt.barh(y=AcquiredLabels, width=AcquiredShare)
plt.xlabel('Share of owners (%)')
plt.title('How did you get your forest?')
plt.tight_layout()
plt.savefig(f'{FigDir}/acquired_forest.png')
plt.close()
print(f'Saved {FigDir}/acquired_forest.png')

# %%
# Who takes care of the forest today (F12)
TodayCols = ['F12_a', 'F12_b', 'F12_c', 'F12_d', 'F12_e', 'F12_f']
CareLabels = [
    'Nobody', 'I myself', 'Someone from my family',
    'Acquaintances', 'Service providers (contractors)', 'Others',
]
TodayShare = Answers[TodayCols].mean() * 100

plt.barh(y=CareLabels, width=TodayShare)
plt.xlabel('Share of owners (%)')
plt.title('Who takes care of the forest today?')
plt.tight_layout()
plt.savefig(f'{FigDir}/care_today.png')
plt.close()
print(f'Saved {FigDir}/care_today.png')

# %%
# 4. Likert — relationship to the forest (F10 subset)
Items = ['F10_k', 'F10_y', 'F10_3', 'F10_v', 'F10_s', 'F10_4', 'F10_12', 'F10_z']
Agreement = Answers[Items].replace({0: np.nan})

Scale = [
    'strongly disagree', 'disagree', 'neutral', 'agree', 'strongly agree'
]
LabelMap = {
    1: 'strongly agree',
    2: 'agree',
    3: 'neutral',
    4: 'disagree',
    5: 'strongly disagree',
}
ItemLabels = Codebook.set_index('variable').loc[Items, 'question']
AgreementPlot = Agreement.rename(columns=ItemLabels)

plot_likert.plot_likert(
    df=AgreementPlot.replace(LabelMap),
    plot_scale=Scale,
    plot_percentage=True,
    label_max_width=50,
)
plt.tick_params(axis='y', labelsize=9)
plt.title('Relationship to the forest')
plt.tight_layout()
plt.savefig(f'{FigDir}/likert_relationship.png')
plt.close()
print(f'Saved {FigDir}/likert_relationship.png')

# %%
# 5. Associations — Spearman (attachment vs visits)
Attachment = Answers['F10_3'].replace({0: np.nan})
Visits = Answers['F34'].replace({0: np.nan})
Result = stats.spearmanr(a=Attachment, b=Visits, nan_policy='omit')
print('Spearman rho (attachment vs visits) =', round(Result.statistic, 2))

# %%
# Mann–Whitney (ask experts vs sustainability)
AskExperts = Answers['F17_b']
Sustainability = Answers['F10_x'].replace({0: np.nan})
NoExperts = Sustainability.loc[AskExperts == 0]
YesExperts = Sustainability.loc[AskExperts == 1]
NYes = YesExperts.count()
NNo = NoExperts.count()
Result = stats.mannwhitneyu(x=NoExperts, y=YesExperts, nan_policy='omit')
EffectSize = 1 - 2 * Result.statistic / (NYes * NNo)
print('rank-biserial r (experts vs sustainability) =', round(EffectSize, 2))

# %%
# Chi-square (residence vs care self)
Residence = Answers['F29'].replace({0: np.nan})
CareSelf = Answers['F12_b']
Counts = pd.crosstab(index=Residence, columns=CareSelf)
print(Counts)
Result = stats.chi2_contingency(observed=Counts)
N = Counts.sum().sum()
K = 2
EffectSize = np.sqrt(Result.statistic / (N * (K - 1)))
print("Cramér's V =", round(EffectSize, 2))

# %%
# Exercise A — climate adapt vs age (Spearman)
ClimateAdapt = Answers['F10_w'].replace({0: np.nan})
AgeClass = Answers['F26'].replace({0: np.nan})
Result = stats.spearmanr(a=ClimateAdapt, b=AgeClass, nan_policy='omit')
print('Spearman rho (climate adapt vs age) =', round(Result.statistic, 2))

# %%
# 6. Linear regression — sustainability ~ experts + forestry + respect
Answers['sustainability_agree'] = 6 - Answers['F10_x'].replace({0: np.nan})
Answers['ask_experts'] = Answers['F17_b'] == 1
Answers['works_in_forestry'] = Answers['F30'].replace({0: np.nan, 2: 0, 3: np.nan})
Answers['plant_animal_respect'] = 6 - Answers['F10_0'].replace({0: np.nan})

Model = smf.ols(
    formula='sustainability_agree ~ ask_experts + works_in_forestry + plant_animal_respect',
    data=Answers,
).fit()
print(Model.summary())

# %%
# Exercise B — likes work ~ valued + talk + care self
Answers['likes_work'] = 6 - Answers['F10_8'].replace({0: np.nan})
Answers['feel_valued'] = 6 - Answers['F10_17'].replace({0: np.nan})
Answers['talk_forest'] = 6 - Answers['F10_15'].replace({0: np.nan})
Answers['care_self'] = Answers['F12_b']

Model = smf.ols(
    formula='likes_work ~ feel_valued + talk_forest + care_self',
    data=Answers,
).fit()
print(Model.summary())

# %%
# 7. Text — spaCy word frequencies (F4 keywords)
nlp = spacy.load('en_core_web_sm', disable=['ner'])

KeywordCols = ['F4_a', 'F4_b', 'F4_c', 'F4_d', 'F4_e']
Keywords = Answers[KeywordCols].replace({'-99': np.nan, '-66': np.nan})
AllKeywords = Keywords.stack().dropna()
AllKeywordText = AllKeywords.str.cat(sep=' ')

KeywordNLP = nlp(AllKeywordText)
NTokens = len(KeywordNLP)
Roots = pd.Series(index=range(NTokens), dtype=object)
for i, token in enumerate(KeywordNLP):
    if not token.is_stop and not token.is_punct:
        Roots.loc[i] = token.lemma_.lower()

TopWords = Roots.value_counts().head(20)
plt.barh(y=TopWords.index, width=TopWords)
plt.xlabel('Number of mentions')
plt.title('Spontaneous associations (F4)')
plt.tight_layout()
plt.savefig(f'{FigDir}/f4_keywords.png')
plt.close()
print(f'Saved {FigDir}/f4_keywords.png')

# %%
# Exercise C — F19 disaster responses (top roots)
DisasterText = Answers['F19'].replace({'-99': np.nan, '-66': np.nan}).dropna()
AllDisasterText = DisasterText.str.cat(sep=' ')
DisasterNLP = nlp(AllDisasterText)
NTokens = len(DisasterNLP)
Roots = pd.Series(index=range(NTokens), dtype=object)
for i, token in enumerate(DisasterNLP):
    if not token.is_stop and not token.is_punct:
        Roots.loc[i] = token.lemma_.lower()

TopWords = Roots.value_counts().head(20)
plt.barh(y=TopWords.index, width=TopWords)
plt.xlabel('Number of times the word appears')
plt.title('Keywords in disaster responses (F19)')
plt.tight_layout()
plt.savefig(f'{FigDir}/f19_keywords.png')
plt.close()
print(f'Saved {FigDir}/f19_keywords.png')

# %%
# Verbs in F19
Roots = pd.Series(index=range(NTokens), dtype=object)
for i, token in enumerate(DisasterNLP):
    if token.pos_ == 'VERB' and not token.is_stop and not token.is_punct:
        Roots.loc[i] = token.lemma_.lower()

TopVerbs = Roots.value_counts().head(20)
plt.barh(y=TopVerbs.index, width=TopVerbs)
plt.xlabel('Number of times the verb appears')
plt.title('Verbs in disaster responses (F19)')
plt.tight_layout()
plt.savefig(f'{FigDir}/f19_verbs.png')
plt.close()
print(f'Saved {FigDir}/f19_verbs.png')

# %%
# Adjective–noun phrases in F19
MatcherAdjNoun = Matcher(nlp.vocab)
MatcherAdjNoun.add('ADJ_PHRASE', [[{'POS': 'ADJ'}, {'POS': 'NOUN'}]])
KeywordAdjNoun = MatcherAdjNoun(DisasterNLP, as_spans=True)
NAdj = len(KeywordAdjNoun)
AdjNoun = pd.Series(index=range(NAdj), dtype=object)
for i, adjnoun in enumerate(KeywordAdjNoun):
    AdjNoun.loc[i] = adjnoun.text.lower()

TopAdjNoun = AdjNoun.value_counts().head(15)
plt.barh(y=TopAdjNoun.index, width=TopAdjNoun)
plt.xlabel('Number of times the phrase appears')
plt.title('Adjective–noun in disaster responses (F19)')
plt.tight_layout()
plt.savefig(f'{FigDir}/f19_adj_noun.png')
plt.close()
print(f'Saved {FigDir}/f19_adj_noun.png')

# %%
# Mentions "sell" in F19 → Mann–Whitney vs economic benefit
MatcherSell = Matcher(nlp.vocab)
MatcherSell.add('SELL', [[{'LEMMA': 'sell'}]])
Answers['mentions_sell'] = 0
for Index in DisasterText.index:
    NLP = nlp(DisasterText.loc[Index])
    if MatcherSell(NLP):
        Answers.loc[Index, 'mentions_sell'] = 1
print(Answers['mentions_sell'].value_counts())

EconomicBenefit = Answers['F10_s'].replace({0: np.nan})
Mentions = Answers['mentions_sell']
NoSell = EconomicBenefit.loc[Mentions == 0]
YesSell = EconomicBenefit.loc[Mentions == 1]
NYes = YesSell.count()
NNo = NoSell.count()
Result = stats.mannwhitneyu(x=NoSell, y=YesSell, nan_policy='omit')
EffectSize = 1 - 2 * Result.statistic / (NYes * NNo)
print('rank-biserial r (sell vs economic benefit) =', round(EffectSize, 2))

# %%
# Exercise D — mentions plant/replant vs drought worry
MatcherPlant = Matcher(nlp.vocab)
MatcherPlant.add('PLANT', [[{'LEMMA': 'plant'}], [{'LEMMA': 'replant'}]])
Answers['mentions_plant'] = 0
for Index in DisasterText.index:
    NLP = nlp(DisasterText.loc[Index])
    if MatcherPlant(NLP):
        Answers.loc[Index, 'mentions_plant'] = 1
print(Answers['mentions_plant'].value_counts())

DroughtWorry = Answers['F15_a'].replace({0: np.nan, 6: np.nan})
Mentions = Answers['mentions_plant']
NoPlant = DroughtWorry.loc[Mentions == 0]
YesPlant = DroughtWorry.loc[Mentions == 1]
NYes = YesPlant.count()
NNo = NoPlant.count()
Result = stats.mannwhitneyu(x=NoPlant, y=YesPlant, nan_policy='omit')
EffectSize = 1 - 2 * Result.statistic / (NYes * NNo)
print('rank-biserial r (plant vs drought worry) =', round(EffectSize, 2))
