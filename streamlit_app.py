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
