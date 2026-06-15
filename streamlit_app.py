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

df_st["Active_SC_%"] = (
    df_st["Active_SC"] / st_population * 100
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
    df_st["Active_Women"] / women_population * 100
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
