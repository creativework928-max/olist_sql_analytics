"""
Brazilian E-Commerce SQL Analytics & Business Intelligence Platform
===================================================================

File:
    dashboard/app.py

Purpose:
    Professional Streamlit dashboard for exploring the Olist Brazilian
    E-Commerce Public Dataset stored in SQLite.

Architecture:
    CSV
      ↓
    ETL / Database Loader
      ↓
    SQLite Database
      ↓
    SQL Analytics
      ↓
    Streamlit Dashboard

Run from the project root:
    streamlit run dashboard/app.py

Expected project structure:
    olist_sql_analytics/
    ├── database/
    │   └── olist_ecommerce.db
    ├── dashboard/
    │   └── app.py
    ├── outputs/
    │   ├── charts/
    │   └── csv/
    └── src/
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =============================================================================
# 1. APPLICATION CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Olist E-Commerce BI Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# 2. PROJECT PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = PROJECT_ROOT / "database" / "olist_ecommerce.db"
OUTPUT_CSV_PATH = PROJECT_ROOT / "outputs" / "csv"

OUTPUT_CSV_PATH.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 3. PROFESSIONAL COLOR PALETTE
# =============================================================================

COLORS = {
    "primary": "#2563EB",
    "secondary": "#14B8A6",
    "success": "#16A34A",
    "warning": "#F59E0B",
    "danger": "#DC2626",
    "purple": "#7C3AED",
    "pink": "#DB2777",
    "dark": "#0F172A",
    "gray": "#64748B",
    "light": "#F8FAFC",
    "white": "#FFFFFF",
    "border": "#E2E8F0",
}

CHART_COLORS = [
    "#2563EB",
    "#14B8A6",
    "#7C3AED",
    "#F59E0B",
    "#DB2777",
    "#16A34A",
    "#DC2626",
    "#0891B2",
    "#9333EA",
    "#EA580C",
]


# =============================================================================
# 4. CUSTOM CSS
# =============================================================================

st.markdown(
    f"""
    <style>

    /* Main application background */
    .stApp {{
        background-color: #F8FAFC;
    }}

    /* Main content */
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            #0F172A 0%,
            #172554 100%
        );
    }}

    section[data-testid="stSidebar"] * {{
        color: #F8FAFC !important;
    }}

    /* Dashboard title */
    .dashboard-title {{
        font-size: 2.35rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0.15rem;
        letter-spacing: -0.04em;
    }}

    .dashboard-subtitle {{
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }}

    /* Section titles */
    .section-title {{
        font-size: 1.35rem;
        font-weight: 750;
        color: #0F172A;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }}

    /* KPI cards */
    .kpi-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
        min-height: 145px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    }}

    .kpi-label {{
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .kpi-value {{
        color: #0F172A;
        font-size: 1.85rem;
        font-weight: 800;
        margin-top: 0.35rem;
    }}

    .kpi-description {{
        color: #94A3B8;
        font-size: 0.78rem;
        margin-top: 0.35rem;
    }}

    /* Information cards */
    .info-card {{
        background: #FFFFFF;
        border-left: 5px solid #2563EB;
        border-radius: 10px;
        padding: 1rem 1.1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }}

    /* Footer */
    .footer {{
        text-align: center;
        color: #94A3B8;
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
    }}

    /* Hide Streamlit default menu/footer where appropriate */
    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 5. DATABASE FUNCTIONS
# =============================================================================

@st.cache_resource
def get_connection() -> sqlite3.Connection:
    """
    Create a reusable SQLite database connection.

    Returns
    -------
    sqlite3.Connection
        SQLite connection object.
    """

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        check_same_thread=False,
    )

    return connection


@st.cache_data(ttl=600)
def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a DataFrame.

    Parameters
    ----------
    query : str
        SQL query.
    params : tuple
        Query parameters.

    Returns
    -------
    pandas.DataFrame
    """

    connection = get_connection()

    return pd.read_sql_query(
        query,
        connection,
        params=params,
    )


@st.cache_data(ttl=600)
def get_table_names() -> list[str]:
    """
    Return all user-created tables in the database.
    """

    query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """

    df = run_query(query)

    return df["name"].tolist()


# =============================================================================
# 6. DATABASE VALIDATION
# =============================================================================

try:
    connection = get_connection()
    table_names = get_table_names()

except Exception as exc:
    st.error(
        "Unable to connect to the SQLite database."
    )

    st.code(
        f"Expected database:\n{DATABASE_PATH}\n\n"
        f"Error:\n{exc}"
    )

    st.stop()


# =============================================================================
# 7. HELPER FUNCTIONS
# =============================================================================

def format_currency(value: float) -> str:
    """Format a number as Brazilian Real."""

    if pd.isna(value):
        return "R$ 0.00"

    return f"R$ {value:,.2f}"


def format_number(value: float) -> str:
    """Format a numeric value with thousands separators."""

    if pd.isna(value):
        return "0"

    return f"{value:,.0f}"


def format_percentage(value: float) -> str:
    """Format a decimal percentage."""

    if pd.isna(value):
        return "0.00%"

    return f"{value:.2f}%"


def style_figure(
    fig: go.Figure,
    title: Optional[str] = None,
) -> go.Figure:
    """
    Apply the project's professional Plotly theme.
    """

    fig.update_layout(
        title=title,
        template="plotly_white",
        font=dict(
            family="Arial, sans-serif",
            color=COLORS["dark"],
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(
            l=45,
            r=25,
            t=65 if title else 30,
            b=45,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor=COLORS["border"],
    )

    fig.update_yaxes(
        gridcolor="#E2E8F0",
        zeroline=False,
    )

    return fig


def save_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
) -> None:
    """Save a DataFrame to the outputs/csv directory."""

    output_path = OUTPUT_CSV_PATH / filename

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )


def create_kpi(
    column,
    label: str,
    value: str,
    description: str,
) -> None:
    """Render a professional KPI card."""

    with column:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# 8. SIDEBAR
# =============================================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size: 1.6rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        ">
            🛒 Olist BI
        </div>

        <div style="
            color: #CBD5E1;
            font-size: 0.85rem;
            margin-bottom: 1.5rem;
        ">
            Brazilian E-Commerce Analytics
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Select dashboard section",
        [
            "Executive Overview",
            "Sales Performance",
            "Product Analytics",
            "Customer Analytics",
            "Seller Analytics",
            "Reviews & Payments",
            "Data Explorer",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Database")

    st.caption(
        f"**SQLite database**\n\n"
        f"`{DATABASE_PATH.name}`"
    )

    st.caption(
        f"**Tables:** {len(table_names)}"
    )

    st.divider()

    st.markdown(
        """
        **Project**

        Brazilian E-Commerce SQL Analytics

        **Technology**

        SQLite · SQL · Pandas · Plotly · Streamlit
        """
    )


# =============================================================================
# 9. HEADER
# =============================================================================

st.markdown(
    '<div class="dashboard-title">'
    'Brazilian E-Commerce BI Dashboard'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive business intelligence platform powered by the '
    'Olist Brazilian E-Commerce Public Dataset'
    '</div>',
    unsafe_allow_html=True,
)


# =============================================================================
# 10. EXECUTIVE OVERVIEW
# =============================================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # KPI QUERY
    # -------------------------------------------------------------------------

    kpi_query = """
        SELECT
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT o.customer_id) AS total_customers,
            COUNT(DISTINCT oi.product_id) AS total_products,
            COUNT(DISTINCT oi.seller_id) AS total_sellers,
            COALESCE(SUM(oi.price), 0) AS total_sales,
            COALESCE(AVG(oi.price), 0) AS avg_item_price
        FROM orders o
        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id;
    """

    kpi_df = run_query(kpi_query)

    total_orders = kpi_df.loc[0, "total_orders"]
    total_customers = kpi_df.loc[0, "total_customers"]
    total_products = kpi_df.loc[0, "total_products"]
    total_sellers = kpi_df.loc[0, "total_sellers"]
    total_sales = kpi_df.loc[0, "total_sales"]
    avg_item_price = kpi_df.loc[0, "avg_item_price"]

    # -------------------------------------------------------------------------
    # KPI CARDS
    # -------------------------------------------------------------------------

    cols = st.columns(6)

    create_kpi(
        cols[0],
        "Total Orders",
        format_number(total_orders),
        "Unique customer orders",
    )

    create_kpi(
        cols[1],
        "Customers",
        format_number(total_customers),
        "Unique customers",
    )

    create_kpi(
        cols[2],
        "Products",
        format_number(total_products),
        "Products sold",
    )

    create_kpi(
        cols[3],
        "Sellers",
        format_number(total_sellers),
        "Active sellers",
    )

    create_kpi(
        cols[4],
        "Sales",
        format_currency(total_sales),
        "Product-item sales",
    )

    create_kpi(
        cols[5],
        "Avg Item Price",
        format_currency(avg_item_price),
        "Average product price",
    )

    # -------------------------------------------------------------------------
    # MONTHLY SALES
    # -------------------------------------------------------------------------

    st.markdown(
        '<div class="section-title">Sales Trend</div>',
        unsafe_allow_html=True,
    )

    monthly_query = """
        SELECT
            strftime('%Y-%m', o.order_purchase_timestamp) AS month,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(SUM(oi.price), 2) AS revenue
        FROM orders o
        INNER JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.order_purchase_timestamp IS NOT NULL
        GROUP BY month
        ORDER BY month;
    """

    monthly_df = run_query(monthly_query)

    if not monthly_df.empty:

        monthly_df["month"] = pd.to_datetime(
            monthly_df["month"],
            format="%Y-%m",
        )

        fig = px.line(
            monthly_df,
            x="month",
            y="revenue",
            markers=True,
            color_discrete_sequence=[COLORS["primary"]],
            labels={
                "month": "Month",
                "revenue": "Revenue (R$)",
            },
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7),
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Revenue: R$ %{y:,.2f}"
                "<extra></extra>"
            ),
        )

        fig = style_figure(
            fig,
            "Monthly Revenue Trend",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        save_dataframe(
            monthly_df,
            "dashboard_monthly_sales.csv",
        )

    # -------------------------------------------------------------------------
    # TOP CATEGORIES
    # -------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        category_query = """
            SELECT
                COALESCE(
                    pct.product_category_name_english,
                    p.product_category_name,
                    'Unknown'
                ) AS category,
                ROUND(SUM(oi.price), 2) AS revenue
            FROM order_items oi
            INNER JOIN products p
                ON oi.product_id = p.product_id
            LEFT JOIN product_category_translation pct
                ON p.product_category_name =
                   pct.product_category_name
            GROUP BY category
            ORDER BY revenue DESC
            LIMIT 10;
        """

        category_df = run_query(category_query)

        fig = px.bar(
            category_df.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
            color="revenue",
            color_continuous_scale=[
                "#DBEAFE",
                "#2563EB",
            ],
            labels={
                "revenue": "Revenue (R$)",
                "category": "Category",
            },
        )

        fig = style_figure(
            fig,
            "Top 10 Product Categories by Revenue",
        )

        fig.update_coloraxes(
            showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        save_dataframe(
            category_df,
            "dashboard_top_categories.csv",
        )

    # -------------------------------------------------------------------------
    # ORDER STATUS
    # -------------------------------------------------------------------------

    with col2:

        status_query = """
            SELECT
                order_status,
                COUNT(*) AS orders
            FROM orders
            GROUP BY order_status
            ORDER BY orders DESC;
        """

        status_df = run_query(status_query)

        fig = px.pie(
            status_df,
            names="order_status",
            values="orders",
            hole=0.55,
            color_discrete_sequence=CHART_COLORS,
        )

        fig.update_traces(
            textposition="outside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Orders: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            ),
        )

        fig = style_figure(
            fig,
            "Order Status Distribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        save_dataframe(
            status_df,
            "dashboard_order_status.csv",
        )


# =============================================================================
# 11. SALES PERFORMANCE
# =============================================================================

elif page == "Sales Performance":

    st.markdown(
        '<div class="section-title">Sales Performance Analytics</div>',
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # DAILY / MONTHLY SALES
    # -------------------------------------------------------------------------

    sales_query = """
        SELECT
            strftime('%Y-%m', o.order_purchase_timestamp) AS month,
            COUNT(DISTINCT o.order_id) AS orders,
            COUNT(oi.order_item_id) AS items,
            ROUND(SUM(oi.price), 2) AS revenue,
            ROUND(SUM(oi.freight_value), 2) AS freight
        FROM orders o
        INNER JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.order_purchase_timestamp IS NOT NULL
        GROUP BY month
        ORDER BY month;
    """

    sales_df = run_query(sales_query)

    if not sales_df.empty:

        sales_df["month"] = pd.to_datetime(
            sales_df["month"],
            format="%Y-%m",
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                sales_df,
                x="month",
                y="revenue",
                color_discrete_sequence=[COLORS["primary"]],
                labels={
                    "month": "Month",
                    "revenue": "Revenue (R$)",
                },
            )

            fig = style_figure(
                fig,
                "Monthly Revenue",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with col2:

            fig = px.line(
                sales_df,
                x="month",
                y="orders",
                markers=True,
                color_discrete_sequence=[COLORS["secondary"]],
                labels={
                    "month": "Month",
                    "orders": "Orders",
                },
            )

            fig = style_figure(
                fig,
                "Monthly Order Volume",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        save_dataframe(
            sales_df,
            "dashboard_sales_performance.csv",
        )

        st.download_button(
            "⬇ Download Sales Data",
            data=sales_df.to_csv(index=False).encode("utf-8"),
            file_name="sales_performance.csv",
            mime="text/csv",
        )

    # -------------------------------------------------------------------------
    # PAYMENT TYPE
    # -------------------------------------------------------------------------

    st.markdown(
        '<div class="section-title">Payment Analysis</div>',
        unsafe_allow_html=True,
    )

    payment_query = """
        SELECT
            payment_type,
            COUNT(*) AS payment_count,
            ROUND(SUM(payment_value), 2) AS payment_value,
            ROUND(AVG(payment_value), 2) AS avg_payment
        FROM order_payments
        GROUP BY payment_type
        ORDER BY payment_value DESC;
    """

    payment_df = run_query(payment_query)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            payment_df,
            x="payment_type",
            y="payment_value",
            color="payment_type",
            color_discrete_sequence=CHART_COLORS,
            labels={
                "payment_type": "Payment Type",
                "payment_value": "Payment Value (R$)",
            },
        )

        fig = style_figure(
            fig,
            "Payment Value by Payment Type",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:

        fig = px.pie(
            payment_df,
            names="payment_type",
            values="payment_count",
            hole=0.5,
            color_discrete_sequence=CHART_COLORS,
        )

        fig = style_figure(
            fig,
            "Payment Transaction Distribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.dataframe(
        payment_df,
        use_container_width=True,
        hide_index=True,
    )


# =============================================================================
# 12. PRODUCT ANALYTICS
# =============================================================================

elif page == "Product Analytics":

    st.markdown(
        '<div class="section-title">Product Analytics</div>',
        unsafe_allow_html=True,
    )

    product_query = """
        SELECT
            oi.product_id,
            COALESCE(
                pct.product_category_name_english,
                p.product_category_name,
                'Unknown'
            ) AS category,
            COUNT(oi.order_item_id) AS units_sold,
            COUNT(DISTINCT oi.order_id) AS orders,
            ROUND(SUM(oi.price), 2) AS revenue,
            ROUND(AVG(oi.price), 2) AS avg_price
        FROM order_items oi
        INNER JOIN products p
            ON oi.product_id = p.product_id
        LEFT JOIN product_category_translation pct
            ON p.product_category_name =
               pct.product_category_name
        GROUP BY
            oi.product_id,
            category
        ORDER BY revenue DESC;
    """

    product_df = run_query(product_query)

    if not product_df.empty:

        top_products = product_df.head(15).copy()

        fig = px.bar(
            top_products.sort_values("revenue"),
            x="revenue",
            y="product_id",
            color="revenue",
            orientation="h",
            color_continuous_scale=[
                "#CCFBF1",
                "#0F766E",
            ],
            hover_data=[
                "category",
                "units_sold",
                "orders",
                "avg_price",
            ],
            labels={
                "revenue": "Revenue (R$)",
                "product_id": "Product ID",
            },
        )

        fig = style_figure(
            fig,
            "Top 15 Products by Revenue",
        )

        fig.update_coloraxes(
            showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # -------------------------------------------------------------
        # CATEGORY TABLE
        # -------------------------------------------------------------

        category_product_query = """
            SELECT
                COALESCE(
                    pct.product_category_name_english,
                    p.product_category_name,
                    'Unknown'
                ) AS category,
                COUNT(DISTINCT oi.product_id) AS products,
                COUNT(oi.order_item_id) AS units_sold,
                ROUND(SUM(oi.price), 2) AS revenue,
                ROUND(AVG(oi.price), 2) AS avg_price
            FROM order_items oi
            INNER JOIN products p
                ON oi.product_id = p.product_id
            LEFT JOIN product_category_translation pct
                ON p.product_category_name =
                   pct.product_category_name
            GROUP BY category
            ORDER BY revenue DESC;
        """

        category_df = run_query(
            category_product_query
        )

        st.markdown(
            '<div class="section-title">'
            'Category Performance'
            '</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            category_df,
            use_container_width=True,
            hide_index=True,
        )

        save_dataframe(
            product_df,
            "dashboard_product_analysis.csv",
        )

        st.download_button(
            "⬇ Download Product Analysis",
            data=product_df.to_csv(index=False).encode("utf-8"),
            file_name="product_analysis.csv",
            mime="text/csv",
        )


# =============================================================================
# 13. CUSTOMER ANALYTICS
# =============================================================================

elif page == "Customer Analytics":

    st.markdown(
        '<div class="section-title">Customer Analytics</div>',
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # CUSTOMER ORDER ANALYSIS
    # -------------------------------------------------------------------------

    customer_query = """
        SELECT
            c.customer_state AS state,
            COUNT(DISTINCT c.customer_unique_id) AS customers,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(SUM(oi.price), 2) AS revenue,
            ROUND(
                SUM(oi.price) /
                NULLIF(COUNT(DISTINCT o.order_id), 0),
                2
            ) AS avg_order_value
        FROM customers c
        INNER JOIN orders o
            ON c.customer_id = o.customer_id
        INNER JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY c.customer_state
        ORDER BY revenue DESC;
    """

    customer_df = run_query(customer_query)

    if not customer_df.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                customer_df.sort_values("revenue"),
                x="revenue",
                y="state",
                orientation="h",
                color="revenue",
                color_continuous_scale=[
                    "#DBEAFE",
                    "#1D4ED8",
                ],
                labels={
                    "revenue": "Revenue (R$)",
                    "state": "State",
                },
            )

            fig = style_figure(
                fig,
                "Revenue by Customer State",
            )

            fig.update_coloraxes(
                showscale=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with col2:

            fig = px.scatter(
                customer_df,
                x="customers",
                y="revenue",
                size="orders",
                color="avg_order_value",
                hover_name="state",
                color_continuous_scale="Viridis",
                labels={
                    "customers": "Customers",
                    "revenue": "Revenue (R$)",
                    "orders": "Orders",
                    "avg_order_value": "Average Order Value",
                },
            )

            fig = style_figure(
                fig,
                "Customer Base vs Revenue",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        st.dataframe(
            customer_df,
            use_container_width=True,
            hide_index=True,
        )

        save_dataframe(
            customer_df,
            "dashboard_customer_analysis.csv",
        )


# =============================================================================
# 14. SELLER ANALYTICS
# =============================================================================

elif page == "Seller Analytics":

    st.markdown(
        '<div class="section-title">Seller Analytics</div>',
        unsafe_allow_html=True,
    )

    seller_query = """
        SELECT
            s.seller_id,
            s.seller_state AS state,
            COUNT(DISTINCT oi.order_id) AS orders,
            COUNT(oi.order_item_id) AS items_sold,
            ROUND(SUM(oi.price), 2) AS revenue,
            ROUND(AVG(oi.price), 2) AS avg_item_price
        FROM sellers s
        INNER JOIN order_items oi
            ON s.seller_id = oi.seller_id
        GROUP BY
            s.seller_id,
            s.seller_state
        ORDER BY revenue DESC;
    """

    seller_df = run_query(seller_query)

    if not seller_df.empty:

        top_sellers = seller_df.head(20).copy()

        fig = px.bar(
            top_sellers.sort_values("revenue"),
            x="revenue",
            y="seller_id",
            orientation="h",
            color="revenue",
            color_continuous_scale=[
                "#EDE9FE",
                "#6D28D9",
            ],
            hover_data=[
                "state",
                "orders",
                "items_sold",
                "avg_item_price",
            ],
            labels={
                "revenue": "Revenue (R$)",
                "seller_id": "Seller ID",
            },
        )

        fig = style_figure(
            fig,
            "Top 20 Sellers by Revenue",
        )

        fig.update_coloraxes(
            showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # Seller state analysis

        seller_state_query = """
            SELECT
                s.seller_state AS state,
                COUNT(DISTINCT s.seller_id) AS sellers,
                COUNT(oi.order_item_id) AS items_sold,
                ROUND(SUM(oi.price), 2) AS revenue
            FROM sellers s
            INNER JOIN order_items oi
                ON s.seller_id = oi.seller_id
            GROUP BY s.seller_state
            ORDER BY revenue DESC;
        """

        seller_state_df = run_query(
            seller_state_query
        )

        st.markdown(
            '<div class="section-title">'
            'Seller Performance by State'
            '</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            seller_state_df,
            use_container_width=True,
            hide_index=True,
        )

        save_dataframe(
            seller_df,
            "dashboard_seller_analysis.csv",
        )


# =============================================================================
# 15. REVIEWS & PAYMENTS
# =============================================================================

elif page == "Reviews & Payments":

    st.markdown(
        '<div class="section-title">Reviews & Customer Experience</div>',
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # REVIEW SCORES
    # -------------------------------------------------------------------------

    review_query = """
        SELECT
            review_score,
            COUNT(*) AS reviews,
            ROUND(
                COUNT(*) * 100.0 /
                SUM(COUNT(*)) OVER (),
                2
            ) AS percentage
        FROM order_reviews
        WHERE review_score IS NOT NULL
        GROUP BY review_score
        ORDER BY review_score;
    """

    review_df = run_query(review_query)

    if not review_df.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                review_df,
                x="review_score",
                y="reviews",
                color="review_score",
                color_continuous_scale=[
                    "#DC2626",
                    "#F59E0B",
                    "#16A34A",
                ],
                labels={
                    "review_score": "Review Score",
                    "reviews": "Number of Reviews",
                },
            )

            fig = style_figure(
                fig,
                "Customer Review Score Distribution",
            )

            fig.update_coloraxes(
                showscale=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with col2:

            avg_review = run_query(
                """
                SELECT
                    ROUND(AVG(review_score), 2) AS avg_score,
                    COUNT(*) AS total_reviews
                FROM order_reviews
                WHERE review_score IS NOT NULL;
                """
            )

            score = avg_review.loc[0, "avg_score"]
            count = avg_review.loc[0, "total_reviews"]

            create_kpi(
                st.container(),
                "Average Review Score",
                f"{score:.2f} / 5",
                f"Based on {count:,.0f} reviews",
            )

            st.markdown(
                "<br>",
                unsafe_allow_html=True,
            )

            st.info(
                "Higher review scores indicate stronger "
                "customer satisfaction. Review distributions "
                "can help identify customer-experience issues."
            )

        st.dataframe(
            review_df,
            use_container_width=True,
            hide_index=True,
        )

    # -------------------------------------------------------------------------
    # PAYMENT INSTALLMENTS
    # -------------------------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Payment Installment Analysis'
        '</div>',
        unsafe_allow_html=True,
    )

    installment_query = """
        SELECT
            payment_installments,
            COUNT(*) AS transactions,
            ROUND(SUM(payment_value), 2) AS payment_value,
            ROUND(AVG(payment_value), 2) AS avg_payment
        FROM order_payments
        GROUP BY payment_installments
        ORDER BY payment_installments;
    """

    installment_df = run_query(
        installment_query
    )

    if not installment_df.empty:

        fig = px.bar(
            installment_df,
            x="payment_installments",
            y="payment_value",
            color="payment_value",
            color_continuous_scale=[
                "#CCFBF1",
                "#0F766E",
            ],
            labels={
                "payment_installments": "Installments",
                "payment_value": "Payment Value (R$)",
            },
        )

        fig = style_figure(
            fig,
            "Payment Value by Number of Installments",
        )

        fig.update_coloraxes(
            showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.dataframe(
            installment_df,
            use_container_width=True,
            hide_index=True,
        )


# =============================================================================
# 16. DATA EXPLORER
# =============================================================================

elif page == "Data Explorer":

    st.markdown(
        '<div class="section-title">Database Explorer</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Use this section to inspect the tables available in "
        "the SQLite database. Only SELECT queries are allowed "
        "through the dashboard query interface."
    )

    selected_table = st.selectbox(
        "Select a table",
        table_names,
    )

    if selected_table:

        # SQLite identifiers cannot safely be parameterized.
        # The table name is therefore validated against the
        # database's actual table list before being inserted.
        if selected_table not in table_names:
            st.error("Invalid table selected.")
            st.stop()

        count_query = f"""
            SELECT COUNT(*) AS row_count
            FROM "{selected_table}";
        """

        count_df = run_query(count_query)

        row_count = int(
            count_df.loc[0, "row_count"]
        )

        st.metric(
            "Rows",
            f"{row_count:,}",
        )

        preview_query = f"""
            SELECT *
            FROM "{selected_table}"
            LIMIT 1000;
        """

        preview_df = run_query(
            preview_query
        )

        st.dataframe(
            preview_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇ Download Table Preview",
            data=preview_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name=f"{selected_table}_preview.csv",
            mime="text/csv",
        )

    # -------------------------------------------------------------------------
    # CUSTOM SELECT QUERY
    # -------------------------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'SQL Query Explorer'
        '</div>',
        unsafe_allow_html=True,
    )

    query = st.text_area(
        "Enter a SELECT query",
        value=(
            "SELECT *\n"
            "FROM orders\n"
            "LIMIT 20;"
        ),
        height=160,
    )

    if st.button(
        "▶ Run Query",
        type="primary",
    ):

        cleaned_query = query.strip().lower()

        allowed = (
            cleaned_query.startswith("select")
            or cleaned_query.startswith("with")
        )

        blocked_keywords = [
            "insert ",
            "update ",
            "delete ",
            "drop ",
            "alter ",
            "create ",
            "replace ",
            "attach ",
            "detach ",
            "pragma ",
        ]

        contains_blocked_keyword = any(
            keyword in cleaned_query
            for keyword in blocked_keywords
        )

        if not allowed:
            st.error(
                "Only SELECT or WITH queries are allowed."
            )

        elif contains_blocked_keyword:
            st.error(
                "This query contains a restricted SQL operation."
            )

        else:

            try:

                result_df = run_query(
                    query
                )

                st.success(
                    f"Query executed successfully. "
                    f"{len(result_df):,} rows returned."
                )

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True,
                )

                st.download_button(
                    "⬇ Download Query Results",
                    data=result_df.to_csv(
                        index=False
                    ).encode("utf-8"),
                    file_name="sql_query_results.csv",
                    mime="text/csv",
                )

            except Exception as exc:

                st.error(
                    f"SQL execution error: {exc}"
                )


# =============================================================================
# 17. FOOTER
# =============================================================================

st.markdown(
    """
    <div class="footer">
        <strong>Brazilian E-Commerce SQL Analytics Platform</strong><br>
        Built with SQLite · SQL · Python · Pandas · Plotly · Streamlit<br>
        Olist Brazilian E-Commerce Public Dataset
    </div>
    """,
    unsafe_allow_html=True,
)

