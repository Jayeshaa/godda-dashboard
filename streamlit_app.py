import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# -------------------------
# Load Data
# -------------------------
df1 = pd.read_csv("godda1.csv")   # Employment
df2 = pd.read_csv("godda7.csv")   # Work & governance

# Clean column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# -------------------------
# Detect Block Columns
# -------------------------
block_col1 = [c for c in df1.columns if "block" in c.lower()][0]
block_col2 = [c for c in df2.columns if "block" in c.lower()][0]

# Convert to string (FIX for TypeError)
df1[block_col1] = df1[block_col1].astype(str)
df2[block_col2] = df2[block_col2].astype(str)

# -------------------------
# Create Unified Block List (SAFE)
# -------------------------
all_blocks = sorted(
    set(df1[block_col1].dropna())
    .union(set(df2[block_col2].dropna()))
)

# -------------------------
# Sidebar Filter
# -------------------------
selected_blocks = st.sidebar.multiselect(
    "Select Blocks",
    all_blocks,
    default=all_blocks
)

df1_f = df1[df1[block_col1].isin(selected_blocks)]
df2_f = df2[df2[block_col2].isin(selected_blocks)]

# -------------------------
# Title
# -------------------------
st.title("📊 MGNREGA Smart Dashboard — Godda")

# =========================================================
# 🔹 EMPLOYMENT SECTION
# =========================================================
st.markdown("## 👥 Employment Analysis")

reg_col = [c for c in df1.columns if "registered workers total" in c.lower()][0]
active_col = [c for c in df1.columns if "active workers" in c.lower()][0]
job_applied_col = [c for c in df1.columns if "jobcards applied" in c.lower()][0]
job_issued_col = [c for c in df1.columns if "jobcards issued" in c.lower()][0]
payment_col = [c for c in df1.columns if "amount involved" in c.lower()][0]
fto_col = [c for c in df1.columns if "timely fto" in c.lower()][0]
transaction_col = [c for c in df1.columns if "transaction" in c.lower()][0]

sc_col = [c for c in df1.columns if "sc" in c.lower()][0]
st_col = [c for c in df1.columns if "st" in c.lower()][0]
other_col = [c for c in df1.columns if "others" in c.lower()][0]
women_col = [c for c in df1.columns if "women" in c.lower()][0]

# KPIs
c1, c2, c3, c4 = st.columns(4)

total_reg = df1_f[reg_col].sum()
total_act = df1_f[active_col].sum()
emp_ratio = (total_act / total_reg * 100) if total_reg else 0

total_app = df1_f[job_applied_col].sum()
total_iss = df1_f[job_issued_col].sum()
card_eff = (total_iss / total_app * 100) if total_app else 0

c1.metric("👥 Registered", f"{total_reg:,.0f}")
c2.metric("⚙️ Active", f"{total_act:,.0f}", f"{emp_ratio:.1f}%")
c3.metric("🪪 Job Cards", f"{card_eff:.1f}%")
c4.metric("💰 Payments", f"{df1_f[payment_col].sum():,.0f}", f"FTO {df1_f[fto_col].mean():.1f}%")

# Charts
st.subheader("📌 Job Cards")
st.plotly_chart(px.bar(df1_f, x=block_col1, y=[job_applied_col, job_issued_col], barmode="group"),
                use_container_width=True)

st.subheader("👥 Worker Composition")
st.plotly_chart(px.bar(df1_f, x=block_col1, y=[sc_col, st_col, other_col]),
                use_container_width=True)

st.subheader("👩 Women Participation")
st.plotly_chart(px.bar(df1_f, x=block_col1, y=[women_col, reg_col], barmode="group"),
                use_container_width=True)

st.subheader("💰 Payments vs Workers")
st.plotly_chart(px.scatter(df1_f, x=reg_col, y=payment_col,
                           size=transaction_col, hover_name=block_col1),
                use_container_width=True)

# =========================================================
# 🔹 RANKING
# =========================================================
st.markdown("## 🏆 Block Ranking")

rank_df = df1_f.copy()

rank_df["Score"] = (
    0.35 * (rank_df[active_col] / rank_df[reg_col]) +
    0.25 * (rank_df[job_issued_col] / rank_df[job_applied_col]) +
    0.20 * (rank_df[fto_col] / 100) +
    0.20 * (rank_df[payment_col] / rank_df[payment_col].max())
)

rank_df = rank_df.sort_values("Score")
rank_df["Rank"] = range(1, len(rank_df)+1)

st.dataframe(rank_df[[block_col1, "Score", "Rank"]])

st.success(f"🏆 Best Block: {rank_df.iloc[-1][block_col1]}")
st.error(f"⚠️ Worst Block: {rank_df.iloc[0][block_col1]}")

# =========================================================
# 🔹 WORK & GOVERNANCE
# =========================================================
st.markdown("## 🏗️ Work & Governance")

issues_col = [c for c in df2.columns if "issues" in c.lower()][0]
amount_col = [c for c in df2.columns if "amount" in c.lower()][0]
plant_completed = [c for c in df2.columns if "completed" in c.lower() and "plantation" in c.lower()][0]
plant_ongoing = [c for c in df2.columns if "ongoing" in c.lower()][0]
as_identified = [c for c in df2.columns if "identified" in c.lower()][0]
as_completed = [c for c in df2.columns if "sarovar" in c.lower() and "completed" in c.lower()][0]

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("⚠️ Issues", f"{df2_f[issues_col].sum():,.0f}")
k2.metric("💰 Amount", f"₹{df2_f[amount_col].sum():,.0f}")
k3.metric("🌱 Completed", f"{df2_f[plant_completed].sum():,.0f}")
k4.metric("🔄 Ongoing", f"{df2_f[plant_ongoing].sum():,.0f}")

# Charts
st.subheader("🌱 Plantation")
st.plotly_chart(px.bar(df2_f, x=block_col2, y=[plant_completed, plant_ongoing], barmode="group"),
                use_container_width=True)

st.subheader("🌊 Amrit Sarovar")
st.plotly_chart(px.bar(df2_f, x=block_col2, y=[as_identified, as_completed], barmode="group"),
                use_container_width=True)

st.subheader("⚠️ Issues")
st.plotly_chart(px.bar(df2_f, x=block_col2, y=issues_col, color=issues_col),
                use_container_width=True)

# Risk Score
st.subheader("🔥 Risk Score")

df2_f = df2_f.copy()
df2_f["Risk"] = df2_f[issues_col] + (df2_f[amount_col] / 100000)

st.plotly_chart(px.bar(df2_f, x=block_col2, y="Risk", color="Risk"),
                use_container_width=True)

st.error(f"🚨 High Risk: {df2_f.sort_values('Risk', ascending=False).iloc[0][block_col2]}")
st.success(f"✅ Low Risk: {df2_f.sort_values('Risk').iloc[0][block_col2]}")

# -------------------------
# Footer
# -------------------------
#st.success("🚀 Dashboard: Employment + Performance + Work + Governance Risk")
