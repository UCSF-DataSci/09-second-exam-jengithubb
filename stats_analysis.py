import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.formula.api import mixedlm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import f_oneway, zscore
from numpy import sqrt

def main():
    # Load data
    data = pd.read_csv("ms_data.csv")
    insurance_types = pd.read_csv("insurance.lst", header=0, names=["insurance_type"])
    data['visit_date'] = pd.to_datetime(data['visit_date'])

    # Calculate z-scores for walking_speed
    data['ws_zscore'] = zscore(data['walking_speed'])
    # Identify outliers for walking_speed
    outliers = data[(data['ws_zscore'] > 3) | (data['ws_zscore'] < -3)]
    print("Outliers detected in walking_speed:\n", outliers)
    # Remove outliers for walking_speed
    data= data[(data['ws_zscore'] <= 3) & (data['ws_zscore'] >= -3)]


    # Calculate z-scores for visit_cost
    data['vc_zscore'] = zscore(data['visit_cost'])
    # Identify outliers for visit_cost
    outliers = data[(data['vc_zscore'] > 3) | (data['vc_zscore'] < -3)]
    print("Outliers detected in visit_cost:\n", outliers)
    # Remove outliers for visit_cost
    data= data[(data['vc_zscore'] <= 3) & (data['vc_zscore'] >= -3)]

    # Analyze walking speed: Multiple regression
    print("### Walking Speed Analysis ###")
    data['education_level'] = data['education_level'].astype('category')
    # Fit the OLS regression model
    regression_model = smf.ols("walking_speed ~ age + C(education_level)", data=data).fit()
    print(regression_model.summary())

    # Account for repeated measures
    print("\n### Account for repeated measures ###")
    # Fit the mixed-effects model
    mixed_model = mixedlm("walking_speed ~ age + C(education_level)", data, groups=data["patient_id"]).fit()
    print(mixed_model.summary()) 


    # Test for significant trends in walking speed
    print("\n### Test for significant trends ###")
    # Fit the OLS model with interaction terms
    interaction_model = smf.ols("walking_speed ~ age * C(education_level)", data=data).fit(cov_type='cluster', cov_kwds={'groups': data['patient_id']})
    print(interaction_model.summary())


    # Simple analysis of insurance type effect
    grouped = data.groupby('insurance_type')['visit_cost']
    anova_result = f_oneway(*[group for _, group in grouped])
    print("ANOVA result for visit costs by insurance type:", anova_result)
    summary_iv = data.groupby("insurance_type")["visit_cost"].agg(["mean", "std"]).reset_index()
    print(summary_iv)

    # Boxplot for costs
    data.boxplot(column='visit_cost', by='insurance_type')
    plt.title("visit costs by insurance type")
    plt.suptitle("")  
    plt.xlabel("Insurance Type")
    plt.ylabel("Visit Cost")
    plt.savefig("Boxplot_c.png")
    plt.show()

    # Function to calculate Cohen's d
    def cohen_d(group1, group2):
        mean_diff = group1.mean() - group2.mean()
        pooled_std = sqrt(
            ((len(group1) - 1) * group1.std()**2 + (len(group2) - 1) * group2.std()**2) /
            (len(group1) + len(group2) - 2)
        )
        return mean_diff / pooled_std

    # Calculate effect sizes
    basic = data[data['insurance_type'] == 'Basic']['visit_cost']
    premium = data[data['insurance_type'] == 'Premium']['visit_cost']
    platinum = data[data['insurance_type'] == 'Platinum']['visit_cost']
    deluxe_premium = data[data['insurance_type'] == 'Deluxe_Premium']['visit_cost']
    ultimate = data[data['insurance_type'] == 'Ultimate']['visit_cost']

    # Print pairwise Cohen's d
    print(f"Basic vs Premium: {cohen_d(basic, premium):.4f}")
    print(f"Basic vs Platinum: {cohen_d(basic, platinum):.4f}")
    print(f"Basic vs Deluxe_Premium: {cohen_d(basic, deluxe_premium):.4f}")
    print(f"Basic vs Ultimate: {cohen_d(basic, ultimate):.4f}")

    print(f"Premium vs Platinum: {cohen_d(premium, platinum):.4f}")
    print(f"Premium vs Deluxe_Premium: {cohen_d(premium, deluxe_premium):.4f}")
    print(f"Premium vs Ultimate: {cohen_d(premium, ultimate):.4f}")
    
    print(f"Platinum vs Deluxe_Premium: {cohen_d(platinum, deluxe_premium):.4f}")
    print(f"Platinum vs Ultimate: {cohen_d(platinum, ultimate):.4f}")

    print(f"Deluxe_Premium vs Ultimate: {cohen_d(deluxe_premium, ultimate):.4f}")


    # Advanced analysis: Interaction effects of education and age on walking speed
    print("\n### Interaction Effects on Walking Speed ###")
    interaction_model = smf.ols("walking_speed ~ age * C(education_level)", data=data).fit()
    print(interaction_model.summary())

    # Control for confounders
    confounder_formula = "walking_speed ~ C(education_level) + age + C(insurance_type)"
    confounder_model = smf.ols(confounder_formula, data=data).fit()
    print(confounder_model.summary())



if __name__ == "__main__":
    main()
