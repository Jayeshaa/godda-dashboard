import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="MGNREGA GODDA DISTRICT ANALYSIS",
    layout="wide"
)

st.title("MGNREGA GODDA DISTRICT ANALYSIS")

# ---------------------------------
# Population Data
# ---------------------------------
total_households = 243676
total_population = 1302084
male_population = 674500
female_population = 627470
transgender_population = 109

# Social Category Households
sc_households = 22079
st_households = 55081
other_households = 164882

# ---------------------------------
# Calculate Average Household Size
# ---------------------------------
avg_household_size = total_population / total_households

# Estimated Population
sc_population = round(sc_households * avg_household_size)
st_population = round(st_households * avg_household_size)
other_population = round(other_households * avg_household_size)

# ---------------------------------
# KPI Metrics
# ---------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Households", f"{total_households:,}")
col2.metric("Total Population", f"{total_population:,}")
col3.metric("Male Population", f"{male_population:,}")
col4.metric("Female Population", f"{female_population:,}")
col5.metric("Transgender Population", f"{transgender_population:,}")

# ---------------------------------
# Population by Social Category
# ---------------------------------
df_population = pd.DataFrame({
    "Category": ["SC", "ST", "Others"],
    "Population": [
        sc_population,
        st_population,
        other_population
    ]
})

fig = px.bar(
    df_population,
    x="Category",
    y="Population",
    text="Population",
    title="Estimated Population by Social Category",
    color="Category"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    height=500,
    xaxis_title="Social Category",
    yaxis_title="Population"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# Methodology Section
# ---------------------------------
st.markdown("---")
st.subheader("Population Estimation Methodology")

st.latex(
    rf"\text{{Average Household Size}} = \frac{{{total_population:,}}}{{{total_households:,}}} = {avg_household_size:.2f}"
)

st.latex(
    r"\text{Estimated Population} = \text{Number of Households} \times \text{Average Household Size}"
)

st.info(
    f"""
Average Household Size = {avg_household_size:.2f}

SC Population = {sc_households:,} × {avg_household_size:.2f} ≈ {sc_population:,}

ST Population = {st_households:,} × {avg_household_size:.2f} ≈ {st_population:,}

Others Population = {other_households:,} × {avg_household_size:.2f} ≈ {other_population:,}
"""
)
# ---------------------------------
# Employment Analysis
# ---------------------------------

st.header("Employment Analysis")

employment_df = pd.DataFrame({
    "Block": [
        "BASANTRAY",
        "BOARIJORE",
        "GODDA",
        "MAHAGAMA",
        "MEHARMA",
        "PATHERGAMA",
        "PORAIYAHAT",
        "SUNDERPAHARI",
        "THAKURGANGTI"
    ],
    "Applied": [22719,43248,38777,42302,40561,22920,39698,19738,32574],
    "Issued": [16541,37282,33588,35614,36262,19919,35481,16674,28953],
    "Active": [8867,23336,16062,17403,21017,11352,21613,10606,19871]
})

# Percentages
employment_df["Issued_%"] = (
    employment_df["Issued"] /
    employment_df["Applied"] * 100
).round(2)

employment_df["Active_%"] = (
    employment_df["Active"] /
    employment_df["Applied"] * 100
).round(2)

employment_df["Active_Among_Issued_%"] = (
    employment_df["Active"] /
    employment_df["Issued"] * 100
).round(2)

# Plotly Chart
fig = px.bar(
    employment_df,
    x="Block",
    y=["Issued_%", "Active_%", "Active_Among_Issued_%"],
    barmode="group",
    text_auto=".2f",
    title="Job Card Conversion Analysis (%)"
)

fig.update_layout(
    height=650,
    yaxis_title="Percentage (%)",
    xaxis_title="Blocks",
    legend_title="Metrics"
)

st.plotly_chart(fig, use_container_width=True)

# Summary Metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Issued %",
    f"{employment_df['Issued_%'].mean():.2f}%"
)

col2.metric(
    "Average Active %",
    f"{employment_df['Active_%'].mean():.2f}%"
)

col3.metric(
    "Average Active among Issued %",
    f"{employment_df['Active_Among_Issued_%'].mean():.2f}%"
)

# Formula Section
st.markdown("---")
st.subheader("Methodology")

st.latex(
    r"\text{Issued \%}=\frac{\text{Issued Jobcards}}{\text{Applied Jobcards}}\times100"
)

st.latex(
    r"\text{Active \%}=\frac{\text{Active Jobcards}}{\text{Applied Jobcards}}\times100"
)

st.latex(
    r"\text{Active Among Issued \%}=\frac{\text{Active Jobcards}}{\text{Issued Jobcards}}\times100"
)

st.info("""
Interpretation:

• Applied Job Cards are considered as 100%.

• Issued % shows how many applicants received job cards.

• Active % shows how many applicants currently have active job cards.

• Active Among Issued % shows retention of issued job cards.
""")
st.header("Monthly Employment Demand Pattern")

monthly_df = pd.DataFrame({
    "Month": [
        "Apr","May","Jun","Jul","Aug","Sep",
        "Oct","Nov","Dec","Jan","Feb","Mar"
    ],
    "Households":[
        27337,32598,39717,37644,32755,23394,
        22502,20448,19118,21355,20945,21201
    ],
    "Persondays":[
        383461,476800,621999,534697,454779,277384,
        274937,239054,248212,269763,259733,260494
    ]
})

# Demand Index (Peak Month = 100)
max_households = monthly_df["Households"].max()

monthly_df["Demand_Index_%"] = (
    monthly_df["Households"] / max_households * 100
).round(2)

fig1 = px.line(
    monthly_df,
    x="Month",
    y="Demand_Index_%",
    markers=True,
    title="Monthly Employment Demand Pattern (%)"
)

fig1.update_layout(
    yaxis_title="Demand Index (%)",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

st.latex(
    r"\text{Monthly Household Demand \%}=\frac{\text{Households in Month}}{\text{Maximum Monthly Households}}\times100"
)

# -----------------------------------------
# Household vs Persondays Contribution
# -----------------------------------------

total_households = monthly_df["Households"].sum()
total_persondays = monthly_df["Persondays"].sum()

monthly_df["Household_Share_%"] = (
    monthly_df["Households"] / total_households * 100
).round(2)

monthly_df["Persondays_Share_%"] = (
    monthly_df["Persondays"] / total_persondays * 100
).round(2)

fig2 = px.bar(
    monthly_df,
    x="Month",
    y=["Household_Share_%", "Persondays_Share_%"],
    barmode="group",
    text_auto=".2f",
    title="Household vs Persondays Contribution (%)"
)

fig2.update_layout(
    yaxis_title="Contribution (%)",
    height=600
)

st.plotly_chart(fig2, use_container_width=True)

st.latex(
    r"\text{Household Share \%}=\frac{\text{Monthly Households}}{\text{Total Annual Households}}\times100"
)

st.latex(
    r"\text{Persondays Share \%}=\frac{\text{Monthly Persondays}}{\text{Total Annual Persondays}}\times100"
)


# Total SC Population
sc_population = 117969

# Data
df_sc = pd.DataFrame({
    "Block": [
        "BASANTRAY", "BOARIJORE", "GODDA",
        "MAHAGAMA", "MEHARMA", "PATHERGAMA",
        "PORAIYAHAT", "SUNDERPAHARI", "THAKURGANGTI"
    ],
    "Registered_SC": [3698, 3078, 3981, 3788, 1488, 2754, 4269, 1414, 1757],
    "Active_SC": [793, 827, 795, 641, 540, 717, 988, 454, 631]
})

# Percentages
df_sc["Registered_SC_%"] = (
    df_sc["Registered_SC"] / sc_population * 100
).round(2)

df_sc["Active_SC_%"] = (
    df_sc["Active_SC"] / sc_population * 100
).round(2)

# Convert to long format
chart_df = df_sc.melt(
    id_vars="Block",
    value_vars=["Registered_SC_%", "Active_SC_%"],
    var_name="Category",
    value_name="Percentage"
)

# Plotly Chart
fig = px.bar(
    chart_df,
    x="Block",
    y="Percentage",
    color="Category",
    barmode="group",
    text="Percentage",
    title="SC Worker Participation by Block (%)"
)

fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

fig.update_layout(
    xaxis_title="Block",
    yaxis_title="Percentage of Total SC Population",
    legend_title="Worker Type",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
\text{Registered SC Workers \%}
=
\frac{\text{Registered SC Workers}}
{\text{Total SC Population}}
\times 100
''')

st.latex(r'''
\text{Active SC Workers \%}
=
\frac{\text{Active SC Workers}}
{\text{Total SC Population}}
\times 100
''')

# Total ST Population
st_population = 294271

# Data
df_st = pd.DataFrame({
    "Block": [
        "BASANTRAY", "BOARIJORE", "GODDA",
        "MAHAGAMA", "MEHARMA", "PATHERGAMA",
        "PORAIYAHAT", "SUNDERPAHARI", "THAKURGANGTI"
    ],
    "Registered_ST": [3698, 3078, 3981, 3788, 1488, 2754, 4269, 1414, 1757],
    "Active_ST": [793, 827, 795, 641, 540, 717, 988, 454, 631]
})

# Percentages
df_st["Registered_ST_%"] = (
    df_st["Registered_ST"] / st_population * 100
).round(2)

df_st["Active_ST_%"] = (
    df_st["Active_ST"] / st_population * 100
).round(2)

# Convert to long format
chart_df = df_st.melt(
    id_vars="Block",
    value_vars=["Registered_ST_%", "Active_ST_%"],
    var_name="Category",
    value_name="Percentage"
)

# Plotly Chart
fig = px.bar(
    chart_df,
    x="Block",
    y="Percentage",
    color="Category",
    barmode="group",
    text="Percentage",
    title="ST Worker Participation by Block (%)"
)

fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

fig.update_layout(
    xaxis_title="Block",
    yaxis_title="Percentage of Total SC Population",
    legend_title="Worker Type",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
\text{Registered ST Workers \%}
=
\frac{\text{Registered ST Workers}}
{\text{Total ST Population}}
\times 100
''')

st.latex(r'''
\text{Active ST Workers \%}
=
\frac{\text{Active ST Workers}}
{\text{Total ST Population}}
\times 100
''')

# Total Women Population
women_population = 627470

# Data
df_women = pd.DataFrame({
    "Block": [
        "BASANTRAY", "BOARIJORE", "GODDA",
        "MAHAGAMA", "MEHARMA", "PATHERGAMA",
        "PORAIYAHAT", "SUNDERPAHARI", "THAKURGANGTI"
    ],
    "Registered_Women": [1474,37277,6502,3201,1206,5172,19665,19381,4071],
    "Active_Women": [264,11632,1444,471,444,1269,5377,5156,877]
})

# Percentages
df_women["Registered_Women_%"] = (
    df_women["Registered_Women"] / women_population * 100
).round(2)

df_women["Active_Women_%"] = (
    df_women["Active_Women"] / women_population * 100
).round(2)

# Convert to long format
chart_df = df_women.melt(
    id_vars="Block",
    value_vars=["Registered_Women_%", "Active_Women_%"],
    var_name="Category",
    value_name="Percentage"
)

# Plotly Chart
fig = px.bar(
    chart_df,
    x="Block",
    y="Percentage",
    color="Category",
    barmode="group",
    text="Percentage",
    title="Women Worker Participation by Block (%)"
)

fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

fig.update_layout(
    xaxis_title="Block",
    yaxis_title="Percentage of Total SC Population",
    legend_title="Worker Type",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
\text{Registered Women Workers \%}
=
\frac{\text{Registered Women Workers}}
{\text{Total Women Population}}
\times 100
''')

st.latex(r'''
\text{Active Women Workers \%}
=
\frac{\text{Active Women Workers}}
{\text{Total Women Population}}
\times 100
''')


blocks = [
    "BASANTRAY","BOARIJORE","GODDA",
    "MAHAGAMA","MEHARMA","PATHERGAMA",
    "PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

active_eshram = [8079,22603,14168,11421,15177,11015,21907,10625,21477]
beneficiary = [11433,27672,21188,20258,22616,13944,24500,10734,19789]

df = pd.DataFrame({
    "Block": blocks,
    "Active_eShram": active_eshram,
    "Beneficiary": beneficiary
})

# Use highest active workers as 100%
base = df["Active_eShram"].max()

df["Active_eShram_%"] = (
    df["Active_eShram"] / base * 100
).round(2)

df["Beneficiary_%"] = (
    df["Beneficiary"] / base * 100
).round(2)

chart_df = df.melt(
    id_vars="Block",
    value_vars=["Active_eShram_%","Beneficiary_%"],
    var_name="Category",
    value_name="Percentage"
)

fig = px.bar(
    chart_df,
    x="Block",
    y="Percentage",
    color="Category",
    barmode="group",
    text="Percentage",
    title="e-Shram Coverage Analysis (%)"
)

fig.update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside'
)

fig.update_layout(
    height=600,
    xaxis_title="Block",
    yaxis_title="Percentage (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
\text{Active Workers e-Shram \%}
=
\frac{\text{Active Workers e-Shram}}
{\max(\text{Active Workers e-Shram})}
\times100
''')

st.latex(r'''
\text{Beneficiary Coverage \%}
=
\frac{\text{Beneficiary of e-Shram Portal}}
{\max(\text{Active Workers e-Shram})}
\times100
''')


blocks = [
    "BASANTRAY","BOARIJORE","GODDA",
    "MAHAGAMA","MEHARMA","PATHERGAMA",
    "PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

df = pd.DataFrame({
    "Block": blocks,

    "18_30": [935/6610*100,4082/12258*100,1389/9102*100,1546/8236*100,
              2431/7800*100,1417/6951*100,3139/10685*100,1558/5775*100,
              5468/12914*100],

    "31_40": [1268/11734*100,4070/23076*100,2592/32022*100,1891/20227*100,
              2986/18838*100,1701/14007*100,4030/31006*100,1968/13600*100,
              4658/17778*100],

    "41_50": [1334/15088*100,3980/34076*100,2691/49499*100,2170/32680*100,
              3138/28409*100,1905/18496*100,4289/45747*100,1984/19768*100,
              3774/23519*100],

    "51_60": [874/11424*100,2635/24283*100,1652/28707*100,1419/21610*100,
              1527/16817*100,1285/13110*100,2869/32292*100,1129/12584*100,
              2198/15811*100],

    "61_80": [265/5173*100,933/13258*100,522/14020*100,487/11689*100,
              477/9676*100,517/7779*100,1060/18123*100,238/5031*100,
              617/8543*100],

    "80_plus": [3/276*100,8/966*100,1/261*100,5/520*100,
                9/1165*100,13/462*100,12/959*100,3/23*100,
                5/783*100]
})

# Convert to long format
chart_df = df.melt(
    id_vars="Block",
    var_name="Age_Group",
    value_name="Employment_Rate"
)

fig = px.bar(
    chart_df,
    x="Block",
    y="Employment_Rate",
    color="Age_Group",
    barmode="group",
    text=chart_df["Employment_Rate"].round(1),
    title="Age-wise Employment Rate (%) by Block"
)

fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='outside'
)

fig.update_layout(
    height=700,
    xaxis_title="Block",
    yaxis_title="Employment Rate (%)",
    legend_title="Age Group"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
\text{Employment Rate (\%)}
=
\frac{\text{Employed Persons}}
{\text{Registered Persons}}
\times100
''')


blocks = [
    "BASANTRAY","BOARIJORE","GODDA",
    "MAHAGAMA","MEHARMA","PATHERGAMA",
    "PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

df = pd.DataFrame({
    "Block": blocks,
    "Male_Skilled":[726,468,455,1093,827,699,795,648,1940],
    "Female_Skilled":[65,104,83,282,347,257,16,278,163],
    "Male_SemiSkilled":[8,129,313,69,25,108,316,75,571],
    "Female_SemiSkilled":[621,1195,875,537,995,672,1038,715,1405]
})

# Total workforce in each block
df["Total"] = (
    df["Male_Skilled"] +
    df["Female_Skilled"] +
    df["Male_SemiSkilled"] +
    df["Female_SemiSkilled"]
)

# Percentage calculations
df["Male_Skilled_%"] = round(df["Male_Skilled"] / df["Total"] * 100, 2)
df["Female_Skilled_%"] = round(df["Female_Skilled"] / df["Total"] * 100, 2)
df["Male_SemiSkilled_%"] = round(df["Male_SemiSkilled"] / df["Total"] * 100, 2)
df["Female_SemiSkilled_%"] = round(df["Female_SemiSkilled"] / df["Total"] * 100, 2)

chart_df = df.melt(
    id_vars="Block",
    value_vars=[
        "Male_Skilled_%",
        "Female_Skilled_%",
        "Male_SemiSkilled_%",
        "Female_SemiSkilled_%"
    ],
    var_name="Category",
    value_name="Percentage"
)

fig = px.bar(
    chart_df,
    x="Block",
    y="Percentage",
    color="Category",
    barmode="group",
    text="Percentage",
    title="Skill Composition by Block (%)"
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_layout(
    height=700,
    xaxis_title="Block",
    yaxis_title="Percentage of Total Skilled & Semi-Skilled Workforce",
    legend_title="Worker Category"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
\text{Category Percentage}
=
\frac{\text{Workers in Category}}
{\text{Male Skilled + Female Skilled + Male Semi-Skilled + Female Semi-Skilled}}
\times100
''')

st.latex(r'''
\begin{aligned}
\text{Male Skilled \%} &= \frac{\text{Male Skilled}}
{\text{Male Skilled}+\text{Female Skilled}+\text{Male Semi-Skilled}+\text{Female Semi-Skilled}}
\times 100 \\[8pt]

\text{Female Skilled \%} &= \frac{\text{Female Skilled}}
{\text{Male Skilled}+\text{Female Skilled}+\text{Male Semi-Skilled}+\text{Female Semi-Skilled}}
\times 100 \\[8pt]

\text{Male Semi-Skilled \%} &= \frac{\text{Male Semi-Skilled}}
{\text{Male Skilled}+\text{Female Skilled}+\text{Male Semi-Skilled}+\text{Female Semi-Skilled}}
\times 100 \\[8pt]

\text{Female Semi-Skilled \%} &= \frac{\text{Female Semi-Skilled}}
{\text{Male Skilled}+\text{Female Skilled}+\text{Male Semi-Skilled}+\text{Female Semi-Skilled}}
\times 100
\end{aligned}
''')

st.title("MGNREGA Persondays Distribution (%)")

# Data Loading
data = {
    "Blocks": [
        "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
        "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
    ],
    "SCs": [17494,26901,18598,9579,13170,13020,28479,13864,20323],
    "STs": [3965,388954,42669,7792,9827,32355,195804,151343,26018],
    "Others": [159514,419651,270403,255501,429059,208505,547247,167566,823712],
    "Women": [77896,380895,142814,138406,211253,113261,321081,143780,447698]
}

df = pd.DataFrame(data)

# Total persondays per block
df["Total"] = df[["SCs","STs","Others","Women"]].sum(axis=1)

# Convert to percentage
for col in ["SCs","STs","Others","Women"]:
    df[col + "_%"] = (df[col] / df["Total"]) * 100

# Melt for Plotly
df_melt = df.melt(
    id_vars="Blocks",
    value_vars=["SCs_%","STs_%","Others_%","Women_%"],
    var_name="Category",
    value_name="Percentage"
)

# Clean labels
df_melt["Category"] = df_melt["Category"].str.replace("_%","")

# Plot
fig = px.bar(
    df_melt,
    x="Blocks",
    y="Percentage",
    color="Category",
    barmode="stack",
    text_auto=".1f"
)

fig.update_layout(
    title="Persondays Generated (%) by Category per Block",
    yaxis_title="Percentage (%)",
    xaxis_title="Blocks"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T = SCs + STs + Others + Women
''')

st.latex(r'''
\%C =
\frac{C}{T} \times 100
''')

#st.title("MGNREGA Vulnerable Household Analysis")

# Data Loading
data = {
    "Blocks": [
        "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
        "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
    ],
    "Households": [0, 24, 2, 9, 0, 0, 18, 0, 1]
}

df = pd.DataFrame(data)

# Plot
fig = px.bar(
    df,
    x="Blocks",
    y="Households",
    text="Households",
    title="Households from Vulnerable Communities Receiving Individual Assets (Stopped from MGNREGA)"
)

fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Number of Households"
)

st.plotly_chart(fig, use_container_width=True)

st.title("Disabled and Transgender Inclusion")

# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Disabled data
disabled_registered = [232,36,120,293,13,65,99,49,177]
disabled_employed   = [15,8,24,46,2,10,17,11,69]
disabled_persondays  = [705,323,987,1503,104,305,921,522,4154]

# Transgender data
trans_registered = [4,5,2,2,2,0,5,1,1]
trans_employed   = [0,0,1,0,0,0,0,0,0]
trans_persondays = [0,0,18,0,0,0,0,0,0]

df = pd.DataFrame({
    "Blocks": blocks,

    "Disabled Registered": disabled_registered,
    "Disabled Employed": disabled_employed,
    "Disabled Persondays": disabled_persondays,

    "Trans Registered": trans_registered,
    "Trans Employed": trans_employed,
    "Trans Persondays": trans_persondays
})

# Totals
df["Disabled Total"] = df["Disabled Registered"] + df["Disabled Employed"] + df["Disabled Persondays"]
df["Trans Total"] = df["Trans Registered"] + df["Trans Employed"] + df["Trans Persondays"]

# Percentages (Disabled)
df["Disabled Registered %"] = df["Disabled Registered"] / df["Disabled Total"] * 100
df["Disabled Employed %"] = df["Disabled Employed"] / df["Disabled Total"] * 100
df["Disabled Persondays %"] = df["Disabled Persondays"] / df["Disabled Total"] * 100

# Percentages (Transgender)
df["Trans Registered %"] = df["Trans Registered"] / df["Trans Total"] * 100
df["Trans Employed %"] = df["Trans Employed"] / df["Trans Total"] * 100
df["Trans Persondays %"] = df["Trans Persondays"] / df["Trans Total"] * 100

# Melt for Plotly
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=[
        "Disabled Registered %","Disabled Employed %","Disabled Persondays %",
        "Trans Registered %","Trans Employed %","Trans Persondays %"
    ],
    var_name="Category",
    value_name="Percentage"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Percentage",
    color="Category",
    barmode="group",
    text_auto=".1f",
    title="Percentage Distribution: Disabled vs Transgender (Across Blocks)"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Percentage (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T_i^{(D)} = DR_i + DE_i + DP_i
''')

st.latex(r'''
T_i^{(T)} = TR_i + TE_i + TP_i
''')

st.latex(r'''
\%C_i = \frac{C_i}{T_i} \times 100
''')

#st.title("MNREGA Bank Account Analysis")

# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Data
commercial_rrb = [21870, 42773, 38386, 36706, 35909, 27195, 50036, 20892, 33602]
cooperative =    [1, 1, 0, 0, 0, 7, 0, 0, 1]
post_office =    [297, 1230, 3905, 3081, 1745, 542, 340, 1622, 2318]

df = pd.DataFrame({
    "Blocks": blocks,
    "Commercial_RRB": commercial_rrb,
    "Cooperative": cooperative,
    "Post_Office": post_office
})

# Total per block
df["Total"] = df["Commercial_RRB"] + df["Cooperative"] + df["Post_Office"]

# Percentages
df["Commercial_RRB_%"] = df["Commercial_RRB"] / df["Total"] * 100
df["Cooperative_%"] = df["Cooperative"] / df["Total"] * 100
df["Post_Office_%"] = df["Post_Office"] / df["Total"] * 100

# Melt for plotting
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=[
        "Commercial_RRB_%",
        "Cooperative_%",
        "Post_Office_%"
    ],
    var_name="Account Type",
    value_name="Percentage"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Percentage",
    color="Account Type",
    barmode="group",
    text_auto=".1f",
    title="MNREGA Bank Account Distribution (%) by Block"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Percentage (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T_i = \text{Commercial\&RRB}_i + \text{Cooperative}_i + \text{Post Office}_i
''')

st.latex(r'''
\%C_i = \frac{\text{Commercial\&RRB}_i}{T_i} \times 100
''')

st.latex(r'''
\%Coop_i = \frac{\text{Cooperative}_i}{T_i} \times 100
''')

st.latex(r'''
\%PO_i = \frac{\text{Post Office}_i}{T_i} \times 100
''')


# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Frozen account data
commercial_rrb = [18648,35937,26020,33438,34572,25738,37237,19605,31796]
cooperative =    [0,0,0,0,0,5,0,0,1]
post_office =    [0,1,1,0,0,0,0,0,20]

df = pd.DataFrame({
    "Blocks": blocks,
    "Commercial_RRB": commercial_rrb,
    "Cooperative": cooperative,
    "Post_Office": post_office
})

# Total frozen accounts per block
df["Total"] = df["Commercial_RRB"] + df["Cooperative"] + df["Post_Office"]

# Percentages
df["Commercial_RRB_%"] = df["Commercial_RRB"] / df["Total"] * 100
df["Cooperative_%"] = df["Cooperative"] / df["Total"] * 100
df["Post_Office_%"] = df["Post_Office"] / df["Total"] * 100

# Melt for Plotly
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=[
        "Commercial_RRB_%",
        "Cooperative_%",
        "Post_Office_%"
    ],
    var_name="Account Type",
    value_name="Percentage"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Percentage",
    color="Account Type",
    barmode="group",
    text_auto=".1f",
    title="Frozen MNREGA Bank Accounts Distribution (%) by Block"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Percentage (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T_i = \text{Commercial\&RRB Frozen}_i + \text{Cooperative Frozen}_i + \text{Post Office Frozen}_i
''')

st.latex(r'''
\%Commercial_i = \frac{\text{Commercial\&RRB Frozen}_i}{T_i} \times 100
''')

st.latex(r'''
\%Cooperative_i = \frac{\text{Cooperative Frozen}_i}{T_i} \times 100
''')

st.latex(r'''
\%PostOffice_i = \frac{\text{Post Office Frozen}_i}{T_i} \times 100
''')

# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# PFMS pending accounts
pending = [1221, 3097, 2882, 1377, 1838, 1348, 3022, 1528, 2190]

df = pd.DataFrame({
    "Blocks": blocks,
    "Pending_Accounts": pending
})

# Total pending across all blocks
df["Total"] = df["Pending_Accounts"].sum()

# Percentage contribution
df["Pending_%"] = (df["Pending_Accounts"] / df["Total"]) * 100

# Plot
fig = px.bar(
    df,
    x="Blocks",
    y="Pending_%",
    text_auto=".1f",
    title="PFMS Pending Account Validation (%) by Block"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Percentage Share (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T = \sum_{i=1}^{n} P_i
''')

st.latex(r'''
\%P_i = \frac{P_i}{T} \times 100
''')


# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Data (Rs. in Lakhs)
wage = [460.4,2121.11,840.37,693.25,1143.88,636.87,1944.8,845.89,2210.12]
material = [127.38,359.12,163.77,142.26,270.64,150.85,588.2,258.18,439.49]
admin = [26.06,37.07,46.71,35.13,40.39,36.51,54.83,29.72,36.98]

df = pd.DataFrame({
    "Blocks": blocks,
    "Wage": wage,
    "Material": material,
    "Admin": admin
})

# Total expenditure
df["Total"] = df["Wage"] + df["Material"] + df["Admin"]

# Percentages
df["Wage_%"] = df["Wage"] / df["Total"] * 100
df["Material_%"] = df["Material"] / df["Total"] * 100
df["Admin_%"] = df["Admin"] / df["Total"] * 100

# Melt for plotting
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=["Wage_%","Material_%","Admin_%"],
    var_name="Expenditure Type",
    value_name="Percentage"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Percentage",
    color="Expenditure Type",
    barmode="group",
    text_auto=".1f",
    title="MGNREGA Expenditure Composition (%) by Block"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Percentage (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.latex(r'''
\%W_i = \frac{W_i}{T_i} \times 100
''')

st.latex(r'''
\%M_i = \frac{M_i}{T_i} \times 100
''')

st.latex(r'''
\%A_i = \frac{A_i}{T_i} \times 100
''')

# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Data
cost_per_personday = [378.59,316.64,336.44,377.25,385.28,363.39,361.95,363.35,393.2]
labour = [461.22,2129.57,845.28,695.59,1152.66,647.19,1967.09,848.49,2218.45]
material = [227.7,432.12,274.46,279.31,545.8,347.94,701.68,343.07,1094.08]

df = pd.DataFrame({
    "Blocks": blocks,
    "Cost_Per_Personday": cost_per_personday,
    "Labour_Expenditure": labour,
    "Material_Expenditure": material
})

# Melt for plotting
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=[
        "Cost_Per_Personday",
        "Labour_Expenditure",
        "Material_Expenditure"
    ],
    var_name="Metric",
    value_name="Value"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Value",
    color="Metric",
    barmode="group",
    text_auto=".1f",
    title="Cost Efficiency & Expenditure Analysis by Block"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Value (Rs.)"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
C_i = \text{Cost per Personday}_i
''')

st.latex(r'''
L_i = \text{Labour Expenditure}_i
''')

st.latex(r'''
M_i = \text{Material Expenditure}_i
''')

st.latex(r'''
\text{Efficiency Relation} = \frac{L_i + M_i}{C_i}
''')

# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Data
transactions = [32192,126737,64966,52457,78111,44449,71427,147008,56399]
amount = [460.84,2128.59,843.86,695.58,1151.69,640.33,1965.47,2218.04,846.97]

df = pd.DataFrame({
    "Blocks": blocks,
    "Total_Transactions": transactions,
    "Amount_Involved": amount
})

# Melt for grouped visualization
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=["Total_Transactions", "Amount_Involved"],
    var_name="Metric",
    value_name="Value"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Value",
    color="Metric",
    barmode="group",
    text_auto=".1f",
    title="PFMS Payment Analysis: Transactions vs Amount Involved"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Value"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T_i = \text{Total Transactions}_i
''')

st.latex(r'''
A_i = \text{Amount Involved}_i
''')

st.latex(r'''
\text{Efficiency Ratio}_i = \frac{A_i}{T_i}
''')


# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Data
transactions = [32192,126737,64966,52457,78111,44449,71427,147008,56399]
amount = [460.84,2128.59,843.86,695.58,1151.69,640.33,1965.47,2218.04,846.97]

df = pd.DataFrame({
    "Blocks": blocks,
    "Total_Transactions": transactions,
    "Amount_Involved": amount
})

# Melt for grouped visualization
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=["Total_Transactions", "Amount_Involved"],
    var_name="Metric",
    value_name="Value"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Value",
    color="Metric",
    barmode="group",
    text_auto=".1f",
    title="PFMS Payment Analysis: Transactions vs Amount Involved"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Value"
)

st.plotly_chart(fig, use_container_width=True)


# Categories
categories = [
    "Anganwadi/Other Rural Infrastructure",
    "Coastal Areas",
    "Drought Proofing",
    "Rural Drinking Water",
    "Food Grain",
    "Flood Control and Protection",
    "Fisheries",
    "Micro Irrigation Works",
    "Works on Individuals Land (Category IV)",
    "Land Development",
    "Other Works",
    "Play Ground",
    "Rural Connectivity",
    "Rural Sanitation",
    "Bharat Nirman Sewa Kendra",
    "Water Conservation and Water Harvesting",
    "Renovation of traditional water bodies"
]

approved = [303,0,171,0,0,0,0,210,14310,66,0,0,107,32,0,423,3]
ongoing   = [48,0,132,0,0,0,0,85,8281,2,0,0,77,10,0,286,3]
completed = [255,0,39,0,0,0,0,125,6007,64,0,0,30,22,0,137,0]

df = pd.DataFrame({
    "Category": categories,
    "Approved": approved,
    "Ongoing": ongoing,
    "Completed": completed
})

# Melt for grouped bar chart
plot_df = pd.melt(
    df,
    id_vars="Category",
    value_vars=["Approved", "Ongoing", "Completed"],
    var_name="Work Status",
    value_name="Count"
)

# Plot
fig = px.bar(
    plot_df,
    x="Category",
    y="Count",
    color="Work Status",
    barmode="group",
    text_auto=True,
    title="Category-wise MGNREGA Work Status Distribution"
)

fig.update_layout(
    xaxis_title="Work Category",
    yaxis_title="Number of Works",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T_i = A_i + O_i + C_i
''')

st.latex(r'''
A_i = \text{Total Approved Works}
''')

st.latex(r'''
O_i = \text{Ongoing Works}
''')

st.latex(r'''
C_i = \text{Completed Works}
''')


# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Data (categories)
df = pd.DataFrame({
    "Blocks": blocks,

    "Identified": [14,3,13,0,0,7,0,0,2],
    "Approved_Not_Started": [0,0,0,0,0,0,0,0,0],
    "Ongoing": [1,1,3,0,0,2,0,0,0],
    "Completed": [2,0,7,0,0,5,0,0,0],

    "Land_Productivity": [0,8,0,0,0,1,7,0,0],
    "Plantation": [0,0,0,0,0,0,0,0,0],
    "Rural_Housing": [0,1,16,1,0,45,31,6,10],
    "Livestock_Infrastructure": [2,13,0,1,0,2,2,0,0]
})

# Melt for grouped bar chart
plot_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=[
        "Identified",
        "Approved_Not_Started",
        "Ongoing",
        "Completed",
        "Land_Productivity",
        "Plantation",
        "Rural_Housing",
        "Livestock_Infrastructure"
    ],
    var_name="Category",
    value_name="Work Count"
)

# Plot
fig = px.bar(
    plot_df,
    x="Blocks",
    y="Work Count",
    color="Category",
    barmode="group",
    text_auto=True,
    title="Amrit Sarovar & Rural Development Works by Block (Category-wise)"
)

fig.update_layout(
    xaxis_title="Blocks",
    yaxis_title="Number of Works",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T_{i} = \sum_{k=1}^{n} W_{ik}
''')

st.latex(r'''
W_{ik} = \text{Number of Works in Category k for Block i}
''')

st.latex(r'''
\%W_{ik} = \frac{W_{ik}}{T_i} \times 100
''')



# Blocks
blocks = [
    "BASANTRAY","BOARIJORE","GODDA","MAHAGAMA","MEHARMA",
    "PATHERGAMA","PORAIYAHAT","SUNDERPAHARI","THAKURGANGTI"
]

# Issues (counts)
mis_mis = [79,15,97,0,7,0,17,0,22]
dev_mis = [82,86,203,0,40,0,78,0,21]
proc = [77,50,177,0,20,0,107,0,19]
griev = [20,4,25,0,3,0,6,0,3]

# Amounts
amt_mis = [176965,512142,586414,0,482239,0,5256,0,421619]
amt_dev = [8336637,24803018,1535812,0,10252574,0,82866,0,6847589]
amt_proc = [27075,1255337,71915,0,229485,0,5840,0,334867]
amt_griev = [1400,29250,700,0,21090,0,2944,0,187461]

df = pd.DataFrame({
    "Blocks": blocks,

    "Misconduct_Issues": mis_mis,
    "Deviation_Issues": dev_mis,
    "Process_Violation_Issues": proc,
    "Grievances_Issues": griev,

    "Misconduct_Amount": amt_mis,
    "Deviation_Amount": amt_dev,
    "Process_Violation_Amount": amt_proc,
    "Grievances_Amount": amt_griev
})

# Totals per block
df["Total_Issues"] = df[[
    "Misconduct_Issues",
    "Deviation_Issues",
    "Process_Violation_Issues",
    "Grievances_Issues"
]].sum(axis=1)

df["Total_Amount"] = df[[
    "Misconduct_Amount",
    "Deviation_Amount",
    "Process_Violation_Amount",
    "Grievances_Amount"
]].sum(axis=1)

# Avoid divide by zero
df["Total_Issues"] = df["Total_Issues"].replace(0, 1)
df["Total_Amount"] = df["Total_Amount"].replace(0, 1)

# Issue percentages
for col in ["Misconduct_Issues","Deviation_Issues","Process_Violation_Issues","Grievances_Issues"]:
    df[col + "_%"] = df[col] / df["Total_Issues"] * 100

# Amount percentages
for col in ["Misconduct_Amount","Deviation_Amount","Process_Violation_Amount","Grievances_Amount"]:
    df[col + "_%"] = df[col] / df["Total_Amount"] * 100

# Melt issues
issue_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=[
        "Misconduct_Issues_%",
        "Deviation_Issues_%",
        "Process_Violation_Issues_%",
        "Grievances_Issues_%"
    ],
    var_name="Issue Category",
    value_name="Percentage"
)

# Plot Issues
fig1 = px.bar(
    issue_df,
    x="Blocks",
    y="Percentage",
    color="Issue Category",
    barmode="group",
    text_auto=".1f",
    title="Issue Distribution (%) by Block"
)

fig1.update_layout(xaxis_tickangle=-45)

st.title("MGNREGA Issue & Financial Misconduct Dashboard")
st.plotly_chart(fig1, use_container_width=True)

# Melt amount
amt_df = pd.melt(
    df,
    id_vars="Blocks",
    value_vars=[
        "Misconduct_Amount_%",
        "Deviation_Amount_%",
        "Process_Violation_Amount_%",
        "Grievances_Amount_%"
    ],
    var_name="Financial Category",
    value_name="Percentage"
)

# Plot Amount
fig2 = px.bar(
    amt_df,
    x="Blocks",
    y="Percentage",
    color="Financial Category",
    barmode="group",
    text_auto=".1f",
    title="Financial Impact Distribution (%) by Block"
)

fig2.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Methodology")

st.latex(r'''
T_i = \sum (\text{Issues in all categories})_i
''')

st.latex(r'''
\%Issue_{ik} = \frac{Issue_{ik}}{T_i} \times 100
''')


st.latex(r'''
A_i = \sum (\text{Amount across all categories})_i
''')

st.latex(r'''
\%Amount_{ik} = \frac{Amount_{ik}}{A_i} \times 100
''')















