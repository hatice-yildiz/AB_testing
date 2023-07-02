# AB_testing

<p>Work Problem</p>
<p>Facebook recently introduced a new type of bidding, "average bidding", as an alternative to the existing type of bidding called "maximum bidding". To test this new feature, an A/B test was conducted to see if average bidding brings more conversions than maximum bidding.</p>

<h3>Task 1: Preparing and Analyzing Data</h3>
<h3>Task 2: Defining the Hypothesis of the A/B Test</h3>
<h3>Task 3: Hypothesis Testing</h3>
<h3>Task 4: Analysis of Results</h3>

<h3>Bonus: Functionalization of the Process</h3>

<h3>Required Library and Functions</h3>

<pre><code>import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest
</code></pre>
