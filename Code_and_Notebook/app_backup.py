import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from pathlib import Path

st.set_page_config(
    page_title="Nassau Candy | Factory Optimization",
    page_icon="🏭",
    layout="wide"
)

DATA_DIR = Path(__file__).parent

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    recommendations = pd.read_csv(
        DATA_DIR / "recommendations.csv"
    )
    locations = pd.read_csv(DATA_DIR / "factory_locations.csv")
    mapping = pd.read_csv(DATA_DIR / "factory_mapping.csv")
    coverage = pd.read_csv(DATA_DIR / "destination_coverage.csv")

    return orders, recommendations, locations, mapping, coverage

try:
    orders, recommendations, locations, mapping, coverage = load_data()
except Exception as exc:
    st.error(f"Could not load project CSV files: {exc}")
    st.stop()

# ---------------------------------------------------
# Normalize expected fields
# ---------------------------------------------------
for col in ["Sales", "Gross Profit", "Units"]:
    if col in orders.columns:
        orders[col] = pd.to_numeric(orders[col], errors="coerce")

if "Profit_Margin_Percent" in recommendations.columns:
    recommendations["Profit_Margin_Percent"] = pd.to_numeric(
        recommendations["Profit_Margin_Percent"],
        errors="coerce"
    )

for col in [
    "Distance Reduction km",
    "Distance Reduction Percent",
    "Mapped_Order_Records"
]:
    if col in recommendations.columns:
        recommendations[col] = pd.to_numeric(
            recommendations[col], errors="coerce"
        )

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.title("🏭 Nassau Candy Distributor")
st.subheader("Factory Reallocation & Shipping Optimization")
st.caption(
    "Decision-support prototype | Geographic scenarios are estimates, "
    "not verified shipping savings."
)

# ---------------------------------------------------
# Sidebar filters
# ---------------------------------------------------
st.sidebar.header("Scenario Controls")

products = sorted(
    orders["Product Name"].dropna().astype(str).unique()
) if "Product Name" in orders.columns else []

regions = sorted(
    orders["Region"].dropna().astype(str).unique()
) if "Region" in orders.columns else []

ship_modes = sorted(
    orders["Ship Mode"].dropna().astype(str).unique()
) if "Ship Mode" in orders.columns else []

selected_product = st.sidebar.selectbox(
    "Select product",
    ["All products"] + products
)

selected_region = st.sidebar.selectbox(
    "Destination region",
    ["All regions"] + regions
)

selected_ship_mode = st.sidebar.selectbox(
    "Shipping mode",
    ["All shipping modes"] + ship_modes
)

priority = st.sidebar.slider(
    "Optimization priority: speed vs. profit",
    min_value=0,
    max_value=100,
    value=70,
    help="Higher values emphasize geographic distance improvement. "
         "Profitability is not predicted by this prototype."
)

st.sidebar.info(
    "The priority slider changes the ranking emphasis only. "
    "It does not estimate shipping time or financial savings."
)

# ---------------------------------------------------
# Filter orders
# ---------------------------------------------------
filtered_orders = orders.copy()

if selected_product != "All products":
    filtered_orders = filtered_orders[
        filtered_orders["Product Name"].astype(str) == selected_product
    ]

if selected_region != "All regions" and "Region" in filtered_orders.columns:
    filtered_orders = filtered_orders[
        filtered_orders["Region"].astype(str) == selected_region
    ]

if selected_ship_mode != "All shipping modes":
    filtered_orders = filtered_orders[
        filtered_orders["Ship Mode"].astype(str) == selected_ship_mode
    ]

# Filter recommendation rows by product and selected region / mode
filtered_recs = recommendations.copy()

if selected_product != "All products":
    filtered_recs = filtered_recs[
        filtered_recs["Product Name"].astype(str) == selected_product
    ]

filtered_recs = filtered_recs.copy()

# ---------------------------------------------------
# KPI row
# ---------------------------------------------------
total_sales = (
    filtered_orders["Sales"].sum()
    if "Sales" in filtered_orders.columns else 0
)
total_profit = (
    filtered_orders["Gross Profit"].sum()
    if "Gross Profit" in filtered_orders.columns else 0
)
record_count = len(filtered_orders)

mapped_records = (
    filtered_recs["Mapped_Order_Records"].sum()
    if "Mapped_Order_Records" in filtered_recs.columns else 0
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Order records", f"{record_count:,}")
c2.metric("Sales", f"${total_sales:,.2f}")
c3.metric("Gross profit", f"${total_profit:,.2f}")
c4.metric("Mapped records in shortlist", f"{mapped_records:,.0f}")

st.divider()

# ---------------------------------------------------
# Tabs: all four required modules
# ---------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏭 Factory Simulator",
    "🔄 What-If Scenarios",
    "📋 Recommendations",
    "⚠️ Risk & Impact"
])

# ---------------------------------------------------
# Module 1: Factory Optimization Simulator
# ---------------------------------------------------
with tab1:
    st.header("Factory Optimization Simulator")
    st.write(
        "Compare geographic distance scenarios for a selected product. "
        "Factory eligibility and capacity must be confirmed separately."
    )

    if filtered_recs.empty:
        st.warning("No recommendation rows match the current selection.")
    else:
        product_options = sorted(
            filtered_recs["Product Name"].dropna().astype(str).unique()
        )

        sim_product = st.selectbox(
            "Product to simulate",
            product_options,
            key="sim_product"
        )

        product_recs = filtered_recs[
            filtered_recs["Product Name"].astype(str) == sim_product
        ].copy()

        current_factory = (
            product_recs["Authorized_Current_Factory"].iloc[0]
            if "Authorized_Current_Factory" in product_recs.columns
            else product_recs["Current Factory"].iloc[0]
        )

        st.metric("Current assigned factory", current_factory)

        st.dataframe(
            product_recs[
                [
                    c for c in [
                        "Product Name",
                        "Authorized_Current_Factory",
                        "Candidate Factory",
                        "Mapped_Order_Records",
                        "Distance Reduction km",
                        "Distance Reduction Percent",
                        "Profit_Margin_Percent",
                        "Final Approval"
                    ] if c in product_recs.columns
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        if "Candidate Factory" in product_recs.columns:
            fig = px.bar(
                product_recs.sort_values(
                    "Distance Reduction km", ascending=False
                ),
                x="Candidate Factory",
                y="Distance Reduction km",
                color="Distance Reduction km",
                title="Distance Difference by Candidate Factory",
                labels={
                    "Candidate Factory": "Candidate factory",
                    "Distance Reduction km": "Estimated distance difference (km)"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

    st.info(
        "No predicted lead times are displayed because the source date "
        "data has not yet been validated for model training."
    )

# ---------------------------------------------------
# Module 2: What-if scenario analysis
# ---------------------------------------------------
with tab2:
    st.header("What-If Scenario Analysis")
    st.write(
        "Compare the existing factory with the best available "
        "distance-only alternative for each product."
    )

    if filtered_recs.empty:
        st.warning("No scenarios available for these filters.")
    else:
        scenario_cols = [
            c for c in [
                "Product Name",
                "Authorized_Current_Factory",
                "Candidate Factory",
                "Mapped_Order_Records",
                "Distance Reduction km",
                "Distance Reduction Percent"
            ] if c in filtered_recs.columns
        ]

        scenarios = filtered_recs[scenario_cols].copy()

        if "Distance Reduction km" in scenarios.columns:
            scenarios["Scenario Result"] = np.where(
                scenarios["Distance Reduction km"] > 0,
                "Potential distance improvement",
                np.where(
                    scenarios["Distance Reduction km"] < 0,
                    "Distance would increase",
                    "No change"
                )
            )

        st.dataframe(
            scenarios.sort_values(
                "Distance Reduction km", ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        if (
            "Distance Reduction km" in scenarios.columns
            and not scenarios.empty
        ):
            fig = px.bar(
                scenarios.sort_values(
                    "Distance Reduction km", ascending=True
                ),
                x="Distance Reduction km",
                y="Product Name",
                color="Scenario Result",
                orientation="h",
                title="Potential Distance Difference by Product"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.warning(
        "These are straight-line distance estimates for mapped destinations, "
        "not actual route distances or validated shipping-time reductions."
    )

# ---------------------------------------------------
# Module 3: Recommendation dashboard
# ---------------------------------------------------
with tab3:
    st.header("Recommendation Dashboard")

    if filtered_recs.empty:
        st.warning("No recommendations match the current selection.")
    else:
        ranked = filtered_recs.copy()

        if "Distance Reduction km" in ranked.columns:
            # Slider controls ranking emphasis; not a profit forecast.
            ranked["Distance_Score"] = (
                ranked["Distance Reduction km"].clip(lower=0)
            )

            if "Profit_Margin_Percent" in ranked.columns:
                ranked["Margin_Score"] = (
                    ranked["Profit_Margin_Percent"].fillna(0).clip(lower=0)
                )
            else:
                ranked["Margin_Score"] = 0

            dmax = ranked["Distance_Score"].max()
            pmax = ranked["Margin_Score"].max()

            ranked["Distance_Score_Normalized"] = (
                ranked["Distance_Score"] / dmax if dmax > 0 else 0
            )
            ranked["Margin_Score_Normalized"] = (
                ranked["Margin_Score"] / pmax if pmax > 0 else 0
            )

            distance_weight = priority / 100
            margin_weight = 1 - distance_weight

            ranked["Illustrative_Rank_Score"] = (
                distance_weight * ranked["Distance_Score_Normalized"]
                + margin_weight * ranked["Margin_Score_Normalized"]
            )

            ranked = ranked.sort_values(
                "Illustrative_Rank_Score", ascending=False
            )

        st.caption(
            f"Ranking emphasis: {priority}% distance / "
            f"{100-priority}% current product margin. "
            "This is an illustrative ranking, not optimized profit."
        )

        st.dataframe(
            ranked[
                [
                    c for c in [
                        "Product Name",
                        "Authorized_Current_Factory",
                        "Candidate Factory",
                        "Mapped_Order_Records",
                        "Distance Reduction km",
                        "Profit_Margin_Percent",
                        "Evidence Level",
                        "Review Priority",
                        "Final Approval"
                    ] if c in ranked.columns
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download filtered recommendations",
            data=ranked.to_csv(index=False).encode("utf-8"),
            file_name="filtered_nassau_recommendations.csv",
            mime="text/csv"
        )

# ---------------------------------------------------
# Module 4: Risk and impact panel
# ---------------------------------------------------
with tab4:
    st.header("Risk & Impact Panel")

    if filtered_recs.empty:
        st.warning("No risk records match the current selection.")
    else:
        risk = filtered_recs.copy()

        if "Distance Reduction km" in risk.columns:
            negative = int((risk["Distance Reduction km"] < 0).sum())
            positive = int((risk["Distance Reduction km"] > 0).sum())
        else:
            negative, positive = 0, 0

        if "Mapped_Order_Records" in risk.columns:
            limited = int((risk["Mapped_Order_Records"] < 10).sum())
        else:
            limited = 0

        if "Final Approval" in risk.columns:
            pending = int(
                risk["Final Approval"].astype(str)
                .str.contains("Pending", case=False).sum()
            )
        else:
            pending = len(risk)

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Potential improvements", positive)
        r2.metric("Distance increases", negative)
        r3.metric("Very limited evidence", limited)
        r4.metric("Pending validation", pending)

        risk["Risk Flag"] = np.select(
            [
                risk["Distance Reduction km"] < 0,
                risk["Mapped_Order_Records"] < 10
            ],
            [
                "Distance increases",
                "Very limited mapped evidence"
            ],
            default="Eligibility and cost review required"
        )

        st.subheader("Products requiring attention")
        st.dataframe(
            risk[
                [
                    c for c in [
                        "Product Name",
                        "Candidate Factory",
                        "Mapped_Order_Records",
                        "Distance Reduction km",
                        "Profit_Margin_Percent",
                        "Risk Flag",
                        "Final Approval"
                    ] if c in risk.columns
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.warning(
        "Profit impact is not yet calculated because candidate manufacturing "
        "costs, shipping costs, capacity, and eligibility have not been "
        "validated. Current product margin is not a forecast of candidate "
        "factory profitability."
    )

    st.info(
        "Shipping lead-time predictions are disabled until the date and "
        "lead-time data issues are resolved and a predictive model is validated."
    )

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.divider()
st.caption(
    "Nassau Candy Distributor | Prototype for analytical decision support. "
    "Validate factory eligibility, capacity, cost assumptions, and source "
    "data before operational decisions."
)
