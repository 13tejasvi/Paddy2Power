
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Paddy2Power BioRefinery",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Paddy2Power BioRefinery")
st.caption("Conceptual process design for converting paddy straw into bioethanol")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    [
        "Project Dashboard",
        "Home",
        "Virtual Plant",
        "Material Balance",
        "Economic Assessment",
        "Research Explorer",
        "Patent Explorer",
        "Residue Valorisation"
    ]
)

st.sidebar.info(
    "Prototype status: Conceptual model. "
    "Default values are illustrative and require research validation."
)

if page == "Home":
    st.header("Turning Agricultural Waste into Value")
    st.write(
        "Paddy2Power explores a potential biorefinery route that "
        "converts paddy straw into fermentable sugars and bioethanol, "
        "while identifying useful routes for the remaining biomass."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Target sugar recovery", "≥30%", help="Project target, not a measured result")
    c2.metric("Main product", "Bioethanol")
    c3.metric("Feedstock", "Paddy straw")

    st.subheader("Project objectives")
    st.markdown("""
    - Develop a conceptual paddy straw-to-bioethanol process.
    - Estimate theoretical and recovered fermentable sugar.
    - Estimate ethanol production using adjustable assumptions.
    - Explore equipment, operating costs and potential revenue.
    - Identify useful applications for lignin-rich residual biomass.
    """)

    st.warning(
        "This is a preliminary calculation tool, not an experimentally "
        "validated industrial process. Results depend on feedstock "
        "composition, pretreatment, enzymes, fermentation and recovery."
    )

elif page == "Virtual Plant":
    st.header("Virtual Plant — Process Flow")

    stages = [
        ("1. Feedstock receiving", "Collect, inspect and weigh paddy straw."),
        ("2. Size reduction", "Cut or mill straw to a suitable particle size."),
        ("3. Pretreatment", "Use a selected pretreatment to open the biomass structure."),
        ("4. Solid-liquid separation", "Separate liquid and solid fractions where required."),
        ("5. Conditioning", "Adjust the material to suitable hydrolysis conditions."),
        ("6. Enzymatic hydrolysis", "Convert accessible carbohydrates into fermentable sugars."),
        ("7. Sugar assessment", "Measure or estimate the recovered fermentable sugars."),
        ("8. Fermentation", "Microorganisms convert suitable sugars into ethanol."),
        ("9. Ethanol recovery", "Distillation and further purification recover ethanol."),
        ("10. Residue management", "Assess remaining solids for heat or other supported uses."),
    ]

    for name, description in stages:
        with st.container(border=True):
            st.subheader(name)
            st.write(description)

    st.subheader("Process flow diagram")
    flow_data = pd.DataFrame({
        "Stage": [
            "Straw", "Size reduction", "Pretreatment",
            "Hydrolysis", "Fermentation", "Recovery"
        ],
        "Order": [1, 2, 3, 4, 5, 6],
        "Illustrative flow": [100, 95, 90, 85, 75, 65]
    })

    fig = px.funnel(
        flow_data,
        x="Illustrative flow",
        y="Stage",
        title="Illustrative stage sequence — not measured mass flow"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "The funnel values are placeholders to visualise the stages. "
        "They are not a verified material balance."
    )
    
    st.subheader("Biorefinery Process Flow")

    flow_stages = [
        "Paddy Straw",
        "Size Reduction",
        "Pretreatment",
        "Solid-Liquid Separation",
        "Enzymatic Hydrolysis",
        "Sugar Recovery",
        "Fermentation",
        "Ethanol Purification"
    ]

    for i, stage in enumerate(flow_stages):
        st.markdown(f"**{stage}**")
        if i < len(flow_stages) - 1:
            st.markdown("↓")

    st.markdown("---")
    st.subheader("Residue and Utility Streams")

    st.write(
        "Residual solids → composition assessment → potential "
        "boiler fuel, lignin recovery, or materials applications."
    )
    st.write(
        "Utilities: water, electricity, process heat and chemicals. "
        "Wastewater requires appropriate treatment."
    )

    st.caption(
        "Conceptual process flow only. Actual stream quantities, "
        "energy demand and product yields require validation."
    )


elif page == "Material Balance":
    st.header("Material Balance Calculator")
    st.write("Change the assumptions below to explore the calculated outputs.")

    c1, c2 = st.columns(2)

    with c1:
        straw = st.number_input(
            "Dry paddy straw (kg)", min_value=1.0,
            value=1000.0, step=100.0
        )
        sugar_fraction = st.slider(
            "Theoretical fermentable sugar potential (% of dry straw)",
            min_value=5, max_value=70, value=40
        )
        recovery = st.slider(
            "Sugar recovery target (%)",
            min_value=0, max_value=100, value=30
        )

    with c2:
        ethanol_yield = st.number_input(
            "Ethanol yield (kg per kg recovered sugar)",
            min_value=0.0, max_value=0.511,
            value=0.46, step=0.01, format="%.3f"
        )
        fermentation_efficiency = st.slider(
            "Fermentation efficiency (%)",
            min_value=0, max_value=100, value=85
        )
        ethanol_recovery = st.slider(
            "Ethanol recovery (%)",
            min_value=0, max_value=100, value=95
        )

    theoretical_sugar = straw * sugar_fraction / 100
    recovered_sugar = theoretical_sugar * recovery / 100

    ethanol_before_recovery = (
        recovered_sugar
        * ethanol_yield
        * fermentation_efficiency / 100
    )
    ethanol_kg = ethanol_before_recovery * ethanol_recovery / 100
    ethanol_litres = ethanol_kg / 0.789

    a, b, c = st.columns(3)
    a.metric("Theoretical sugar potential", f"{theoretical_sugar:,.2f} kg")
    b.metric("Recovered sugar", f"{recovered_sugar:,.2f} kg")
    c.metric("Estimated recovered ethanol", f"{ethanol_litres:,.2f} L")

    chart = pd.DataFrame({
        "Material": ["Dry straw input", "Theoretical sugar", "Recovered sugar"],
        "Mass (kg)": [straw, theoretical_sugar, recovered_sugar]
    })
    fig = px.bar(
        chart, x="Material", y="Mass (kg)",
        title="Illustrative material quantities"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        f"Sugar recovery relative to theoretical potential: "
        f"**{recovery}%**"
    )
    st.caption(
        "The 30% value is a project target when selected, not a claim "
        "that the process has achieved it. Theoretical sugar fraction, "
        "yield and efficiencies must be justified with reliable sources. "
        "This simplified model does not account for every process loss."
    )

elif page == "Economic Assessment":
    st.header("Preliminary Economic Assessment")
    st.write(
        "Enter estimated costs for one batch. The defaults are examples "
        "only and are not market-verified quotations."
    )

    straw_cost = st.number_input(
        "Feedstock and transport cost (₹/batch)",
        min_value=0.0, value=2000.0, step=500.0
    )
    pretreatment_cost = st.number_input(
        "Pretreatment cost (₹/batch)",
        min_value=0.0, value=3500.0, step=500.0
    )
    enzyme_cost = st.number_input(
        "Enzyme and chemicals cost (₹/batch)",
        min_value=0.0, value=2500.0, step=500.0
    )
    utilities_cost = st.number_input(
        "Utilities cost (₹/batch)",
        min_value=0.0, value=2000.0, step=500.0
    )
    labour_cost = st.number_input(
        "Labour and maintenance cost (₹/batch)",
        min_value=0.0, value=1500.0, step=500.0
    )

    ethanol_litres = st.number_input(
        "Estimated ethanol output (litres/batch)",
        min_value=0.0, value=56.0, step=5.0
    )
    ethanol_price = st.number_input(
        "Assumed ethanol selling price (₹/litre)",
        min_value=0.0, value=70.0, step=5.0
    )
    residue_revenue = st.number_input(
        "Verified residue revenue (₹/batch)",
        min_value=0.0, value=0.0, step=500.0
    )

    total_cost = (
        straw_cost + pretreatment_cost + enzyme_cost
        + utilities_cost + labour_cost
    )
    revenue = ethanol_litres * ethanol_price + residue_revenue
    margin = revenue - total_cost
    unit_cost = total_cost / ethanol_litres if ethanol_litres > 0 else None

    x, y, z = st.columns(3)
    x.metric("Estimated batch operating cost", f"₹{total_cost:,.2f}")
    y.metric("Estimated batch revenue", f"₹{revenue:,.2f}")
    z.metric("Revenue minus listed costs", f"₹{margin:,.2f}")

    if unit_cost is not None:
        st.metric("Listed operating cost per litre", f"₹{unit_cost:,.2f}/L")

    st.warning(
        "This is not a full profitability or feasibility result. "
        "It excludes capital investment, financing, taxes, depreciation "
        "and other costs unless separately added. Verify the ethanol "
        "price, all cost inputs and production basis before presenting."
    )

elif page == "Residue Valorisation":
    st.header("Residue Valorisation")
    st.write(
        "The remaining solids may contain lignin, unconverted cellulose, "
        "hemicellulose, ash and other components. They must not be assumed "
        "to be pure lignin."
    )

    residue_options = pd.DataFrame({
        "Potential route": [
            "Boiler or process heat",
            "Lignin recovery",
            "Materials applications"
        ],
        "What to investigate": [
            "Heating value, moisture, ash, emissions and boiler suitability",
            "Lignin content, recovery method, purity and separation cost",
            "Composition, safety, performance and application-specific testing"
        ],
        "Evidence required": [
            "Energy balance and suitable combustion data",
            "Analytical data and a validated separation method",
            "Relevant studies and experimental validation"
        ]
    })

    st.dataframe(residue_options, use_container_width=True, hide_index=True)

    st.subheader("Important considerations")
    st.markdown("""
    - Measure or estimate the mass of residual solids.
    - Determine their composition before selecting a use.
    - Consider wastewater, chemicals, ash and environmental impacts.
    - Count residue revenue only when a supported price and usable product exist.
    """)


elif page == "Research Explorer":
    st.header("Research Explorer")
    st.write(
        "Explore scientific literature related to paddy straw "
        "pretreatment, fermentable sugar recovery, bioethanol, "
        "and residue valorisation."
    )

    research_topics = [
        (
            "Paddy straw pretreatment and bioethanol",
            "https://scholar.google.com/scholar?q=rice+straw+pretreatment+bioethanol"
        ),
        (
            "Enzymatic hydrolysis and sugar recovery",
            "https://scholar.google.com/scholar?q=rice+straw+enzymatic+hydrolysis+sugar+recovery"
        ),
        (
            "Lignin-rich residue valorisation",
            "https://scholar.google.com/scholar?q=rice+straw+lignin+residue+valorisation"
        ),
        (
            "Bioethanol techno-economic assessment",
            "https://scholar.google.com/scholar?q=rice+straw+bioethanol+techno-economic+assessment"
        )
    ]

    for topic, link in research_topics:
        with st.container(border=True):
            st.subheader(topic)
            st.link_button("Find research papers", link)

    st.info(
        "These links open literature searches, not verified individual "
        "papers. Check each paper's methods, results and limitations "
        "before using its data in your project."
    )



    st.subheader("Research Evidence Table")

    try:
        research_df = pd.read_csv("research_data.csv")
        st.dataframe(
            research_df,
            use_container_width=True,
            hide_index=True
        )
        st.caption(
            "Search links are starting points. Verify actual papers "
            "and their findings before using numerical values."
        )
    except FileNotFoundError:
        st.warning(
            "research_data.csv was not found. Check that it is "
            "committed in the repository."
        )


elif page == "Patent Explorer":
    st.header("Patent Explorer")

    st.write(
        "Explore existing patent documents related to biomass "
        "pretreatment, rice straw conversion, bioethanol production, "
        "and lignin-rich residue utilisation."
    )

    patent_topics = [
        (
            "Rice straw pretreatment",
            "https://patents.google.com/?q=rice+straw+pretreatment"
        ),
        (
            "Cellulosic biomass to bioethanol",
            "https://patents.google.com/?q=cellulosic+biomass+bioethanol"
        ),
        (
            "Enzymatic hydrolysis of biomass",
            "https://patents.google.com/?q=biomass+enzymatic+hydrolysis"
        ),
        (
            "Lignin and biomass residue valorisation",
            "https://patents.google.com/?q=lignin+biomass+valorisation"
        )
    ]

    for topic, link in patent_topics:
        with st.container(border=True):
            st.subheader(topic)
            st.link_button("Search patents", link)

    st.info(
        "These links open patent searches, not verified individual "
        "patents. Before citing a patent, check its publication number, "
        "claims, applicant, filing date and current legal status."
    )



    st.subheader("Patent Evidence Table")

    try:
        patent_df = pd.read_csv("patent_data.csv")
        st.dataframe(
            patent_df,
            use_container_width=True,
            hide_index=True
        )
        st.caption(
            "The entries are search topics, not confirmed patents. "
            "Verify publication numbers, claims and legal status "
            "before citing any patent."
        )
    except FileNotFoundError:
        st.warning(
            "patent_data.csv was not found. Check that it is "
            "committed in the repository."
        )


elif page == "Project Dashboard":
    st.title("Paddy2Power BioRefinery")
    st.subheader("Paddy Straw to Bioethanol and Residue Valorisation")

    st.write(
        "A conceptual biorefinery that explores converting paddy "
        "straw into fermentable sugars and bioethanol while "
        "investigating useful applications for the remaining solids."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Target sugar recovery", "≥30%", help="Project target, not a validated result.")

    with col2:
        st.metric("Feedstock", "Paddy straw")

    with col3:
        st.metric("Platform", "Dry-lab prototype")

    st.subheader("Process overview")

    stages = [
        "1. Straw preparation",
        "2. Pretreatment",
        "3. Solid-liquid separation",
        "4. Enzymatic hydrolysis",
        "5. Sugar recovery",
        "6. Fermentation",
        "7. Ethanol purification",
        "8. Residue valorisation"
    ]

    for stage in stages:
        st.write("➡️ " + stage)

    st.info(
        "This is a conceptual design. The ≥30% sugar-recovery value "
        "is a target, not an experimentally demonstrated result. "
        "Material-balance and economic outputs depend on the "
        "assumptions entered in their respective pages."
    )



    st.subheader("Download Project Summary")

    report_text = """
Paddy2Power BioRefinery
Paddy Straw to Bioethanol and Residue Valorisation

PROJECT OVERVIEW
A conceptual biorefinery exploring the conversion of paddy straw
into fermentable sugars and bioethanol, with possible applications
for the remaining solids.

PROCESS STAGES
1. Straw preparation and size reduction
2. Pretreatment
3. Solid-liquid separation
4. Enzymatic hydrolysis
5. Sugar recovery
6. Fermentation
7. Ethanol purification
8. Residue assessment and valorisation

PROJECT TARGET
Target sugar recovery: at least 30% of theoretical fermentable
sugar potential. This is a target, not a validated experimental result.

VALIDATION REQUIREMENTS
- Verify feedstock composition and literature values.
- Validate material balances and ethanol yield assumptions.
- Estimate energy, water, chemical and wastewater requirements.
- Verify operating costs and product prices with reliable sources.
- Assess residue composition before selecting an application.

NOTE
This report describes a conceptual dry-lab project, not a validated
industrial process or a demonstrated commercial profit.
"""

    st.download_button(
        label="Download Project Summary",
        data=report_text,
        file_name="Paddy2Power_Project_Summary.txt",
        mime="text/plain"
    )

