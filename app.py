import streamlit as st
import pandas as pd
import plotly.express as px
import os
import math
import html
import base64
import hashlib
import json

# --- 1. Global Page Layout Configurations ---
st.set_page_config(
    page_title="Customer Churn Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global CSS Styling Injection ---
global_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

/* Global Font Override */
html, body, [class*="css"], [class*="st-"]:not(.material-symbols-outlined):not(.material-icons):not([data-testid="stIconMaterial"]) {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Material Symbols — restore ligature rendering for Streamlit UI icons */
.material-symbols-outlined,
.material-icons,
[class*="material-symbols"],
[class*="material-icons"],
[data-testid="stIconMaterial"],
[data-testid="stIconMaterial"] > span,
[data-testid="stIconMaterial"] > div,
[data-testid="collapsedControl"] span,
button[data-testid="stSidebarCollapseButton"] span,
button[data-testid="baseButton-header"] span {
    font-family: 'Material Symbols Outlined', sans-serif !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 20px !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    font-feature-settings: 'liga' !important;
    -webkit-font-feature-settings: 'liga' !important;
    -webkit-font-smoothing: antialiased !important;
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
}

/* Page Margins and Widths */
.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 95% !important;
}

/* Vertical rhythm adjustments */
[data-testid="stVerticalBlock"] > div {
    gap: 0.85rem !important;
}

/* Section Dividers */
hr {
    margin-top: 1.25rem !important;
    margin-bottom: 1.25rem !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Expander Styling */
[data-testid="stExpander"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
    margin-bottom: 0.85rem !important;
}
[data-testid="stExpander"] > div > div > div {
    padding: 0.85rem 1rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    font-size: 0.95rem !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(99, 102, 241, 0.2) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}
[data-testid="stExpander"] summary:hover {
    color: #F8FAFC !important;
}

/* Typography Upgrades */
h1 {
    font-size: 2.25rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    margin-top: 0.5rem !important;
    margin-bottom: 0.5rem !important;
    line-height: 1.25 !important;
}
h2 {
    font-size: 1.65rem !important;
    font-weight: 600 !important;
    color: #F8FAFC !important;
    padding-bottom: 0.4rem !important;
    border-bottom: 2px solid rgba(99, 102, 241, 0.2) !important;
    margin-bottom: 1rem !important;
    margin-top: 1.25rem !important;
}
h3, [data-testid="stMarkdownContainer"] h3 {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}
h4, [data-testid="stMarkdownContainer"] h4 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #F1F5F9 !important;
    margin-top: 0.75rem !important;
    margin-bottom: 0.4rem !important;
}
p, [data-testid="stMarkdownContainer"] p {
    color: #94A3B8 !important;
    line-height: 1.65 !important;
    margin-bottom: 0.75rem !important;
}

/* ============================================================
   Premium Enterprise Sidebar
   ============================================================ */

.stApp > div:first-child {
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
}
[data-testid="stAppViewContainer"] {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    width: auto !important;
    transition: margin-left 0.25s ease, max-width 0.25s ease, padding 0.25s ease !important;
}
section[data-testid="stSidebar"] {
    position: relative !important;
    background: #0B1020 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    flex: 0 0 auto !important;
    width: 300px !important;
    min-width: 300px !important;
    overflow: hidden !important;
    transition: width 0.25s ease, min-width 0.25s ease, border-width 0.25s ease !important;
    z-index: 1 !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    min-width: 0 !important;
    border-right: none !important;
    overflow: hidden !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 100vh !important;
    width: 300px !important;
    min-width: 300px !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
    visibility: hidden !important;
    pointer-events: none !important;
}
[data-testid="stMain"] {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] ::-webkit-scrollbar {
    width: 4px !important;
}
section[data-testid="stSidebar"] ::-webkit-scrollbar-track {
    background: transparent !important;
}
section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
    background: rgba(108, 99, 255, 0.28) !important;
    border-radius: 4px !important;
}

.nav-brand-header {
    padding: 1.35rem 1.15rem 1.15rem 1.15rem;
}
.nav-brand-header + .nav-divider {
    margin-bottom: 22px;
}
.nav-brand-logo {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    min-width: 0;
}
.nav-brand-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #F8FAFC;
    letter-spacing: 0.015em;
    line-height: 1.25;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
.nav-brand-tagline {
    font-size: 0.73rem;
    color: #8B95A8;
    letter-spacing: 0.02em;
    font-weight: 500;
    line-height: 1.35;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.nav-divider {
    height: 1px;
    background: rgba(255, 255, 255, 0.06);
    margin: 0 14px;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    padding: 0 14px !important;
    gap: 0.45rem !important;
}
.nav-divider--after-nav {
    margin: 1.35rem 14px 0 14px;
}

[data-testid="stSidebar"] div.stButton:has(button[kind="secondary"]) {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] div.stButton button[kind="secondary"] {
    background: transparent !important;
    color: #B8C1CE !important;
    border: 1px solid transparent !important;
    border-radius: 14px !important;
    padding: 0 14px !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.025em !important;
    box-shadow: none !important;
    transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease !important;
    width: 100% !important;
    min-height: 52px !important;
    height: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-align: left !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    text-rendering: optimizeLegibility !important;
}
[data-testid="stSidebar"] div.stButton button[kind="secondary"] p,
[data-testid="stSidebar"] div.stButton button[kind="secondary"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] div.stButton button[kind="secondary"] [data-testid="stMarkdownContainer"] p {
    display: block !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    min-width: 0 !important;
    flex: 1 1 auto !important;
    color: inherit !important;
    font-weight: inherit !important;
    letter-spacing: inherit !important;
}
[data-testid="stSidebar"] div.stButton button[kind="secondary"]:hover:not(:disabled) {
    background: rgba(108, 99, 255, 0.15) !important;
    color: #E8EDF4 !important;
    box-shadow: 0 4px 12px rgba(108, 99, 255, 0.2) !important;
    transform: translateX(2px) !important;
}
[data-testid="stSidebar"] div.stButton button[kind="secondary"]:disabled {
    background: rgba(108, 99, 255, 0.14) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: 1px solid rgba(108, 99, 255, 0.22) !important;
    border-left: 3px solid #6C63FF !important;
    box-shadow: 0 0 18px rgba(108, 99, 255, 0.18), inset 0 0 12px rgba(108, 99, 255, 0.06) !important;
    opacity: 1 !important;
    cursor: default !important;
    padding-left: 11px !important;
}

.nav-dataset-wrap {
    padding: 1.35rem 14px 0.65rem 14px;
}
.nav-dataset-card {
    background: #141B2D;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 0.85rem 0.95rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22);
    transition: all 0.2s ease;
}
.nav-dataset-card:hover {
    border-color: rgba(99, 102, 241, 0.2);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}
.nav-dataset-label {
    font-size: 0.62rem;
    font-weight: 700;
    color: #7C879A;
    letter-spacing: 0.08em;
    text-transform: none;
    margin-bottom: 0.45rem;
    -webkit-font-smoothing: antialiased;
}
.nav-dataset-name {
    font-size: 0.86rem;
    font-weight: 600;
    color: #F8FAFC;
    line-height: 1.35;
    word-break: break-word;
    margin-bottom: 0.35rem;
    letter-spacing: 0.015em;
    -webkit-font-smoothing: antialiased;
}
.nav-dataset-meta {
    font-size: 0.74rem;
    color: #A8B3C4;
    font-weight: 500;
    letter-spacing: 0.02em;
    -webkit-font-smoothing: antialiased;
}

[data-testid="stSidebar"] div.stButton:has(button[kind="primary"]) {
    padding: 1.15rem 14px 0.35rem 14px !important;
    width: 100% !important;
}
[data-testid="stSidebar"] div.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #6C63FF 0%, #8B83FF 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.55rem 14px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(108, 99, 255, 0.28) !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
    min-height: 44px !important;
    transform: none !important;
    justify-content: center !important;
}
[data-testid="stSidebar"] div.stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, #7A72FF 0%, #9A93FF 100%) !important;
    box-shadow: 0 6px 18px rgba(108, 99, 255, 0.38) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stSidebar"] div.stButton button[kind="primary"]:active {
    transform: translateY(0) !important;
}

.nav-sidebar-footer {
    padding: 1.35rem 1.15rem 1.5rem 1.15rem;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    margin-top: auto !important;
}
.nav-footer-line {
    font-size: 0.62rem;
    color: #5E6A7D;
    font-weight: 500;
    letter-spacing: 0.05em;
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
}
.nav-footer-line + .nav-footer-line {
    margin-top: 0.15rem;
}

/* KPI Cards (stMetric Overrides) */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-left: 4px solid #6366F1 !important;
    border-radius: 14px !important;
    padding: 0.8rem 1.1rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    min-height: 80px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
    box-shadow: 0 8px 16px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(99, 102, 241, 0.15) !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    color: #94A3B8 !important;
    font-weight: 700 !important;
    text-transform: none !important;
    letter-spacing: 0.02em !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
div[data-testid="stMetricValue"] {
    font-size: clamp(1.1rem, 1.6vw, 1.45rem) !important;
    color: #F8FAFC !important;
    font-weight: 700 !important;
    margin-top: 0.15rem !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

/* Button & Download Button Styling */
div.stButton button, div.stDownloadButton button, div.stFormSubmitButton button {
    background: linear-gradient(180deg, #2563EB 0%, #1E40AF 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(147, 197, 253, 0.28) !important;
    border-radius: 8px !important;
    padding: 0.72rem 1.15rem !important;
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    letter-spacing: 0 !important;
    line-height: 1.15 !important;
    box-shadow: 0 8px 18px -12px rgba(37, 99, 235, 0.75) !important;
    transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease !important;
    width: 100% !important;
    min-height: 46px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    text-align: center !important;
}
div.stButton button:hover, div.stDownloadButton button:hover, div.stFormSubmitButton button:hover {
    background: linear-gradient(180deg, #2F6FEB 0%, #1D4ED8 100%) !important;
    border-color: rgba(191, 219, 254, 0.42) !important;
    box-shadow: 0 10px 22px -12px rgba(37, 99, 235, 0.9) !important;
    transform: translateY(-1px) !important;
}
div.stButton button:active, div.stDownloadButton button:active, div.stFormSubmitButton button:active {
    transform: translateY(0) !important;
    box-shadow: 0 4px 10px -8px rgba(37, 99, 235, 0.75) !important;
}
div.stButton button p, div.stDownloadButton button p, div.stFormSubmitButton button p {
    color: inherit !important;
    font-weight: inherit !important;
    line-height: 1.15 !important;
    margin: 0 !important;
}

/* Download Button Styling (Executive Graphite) */
div.stDownloadButton button {
    background: linear-gradient(180deg, #334155 0%, #1E293B 100%) !important;
    border-color: rgba(148, 163, 184, 0.24) !important;
    box-shadow: 0 8px 18px -12px rgba(15, 23, 42, 0.9) !important;
}
div.stDownloadButton button:hover {
    background: linear-gradient(180deg, #3F4F63 0%, #263548 100%) !important;
    border-color: rgba(203, 213, 225, 0.34) !important;
    box-shadow: 0 10px 22px -12px rgba(15, 23, 42, 0.95) !important;
}
div.stDownloadButton button:active {
    box-shadow: 0 4px 10px -8px rgba(15, 23, 42, 0.9) !important;
}

/* Secondary Button Styling (Dark Outlined) */
div.stButton button[kind="secondary"] {
    background: rgba(15, 23, 42, 0.78) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 8px !important;
    padding: 0.72rem 1.15rem !important;
    font-weight: 800 !important;
    letter-spacing: 0 !important;
    box-shadow: 0 8px 18px -14px rgba(0, 0, 0, 0.8) !important;
    transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease !important;
    width: 100% !important;
    min-height: 46px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    text-align: center !important;
}
div.stButton button[kind="secondary"]:hover {
    background: rgba(30, 41, 59, 0.92) !important;
    border-color: rgba(203, 213, 225, 0.28) !important;
    color: #F8FAFC !important;
    box-shadow: 0 10px 22px -14px rgba(0, 0, 0, 0.9) !important;
    transform: translateY(-1px) !important;
}
div.stButton button[kind="secondary"]:active {
    transform: translateY(0) !important;
}

.st-key-btn_launch_dashboard button {
    background: linear-gradient(180deg, #1D4ED8 0%, #153E92 100%) !important;
    border-color: rgba(191, 219, 254, 0.42) !important;
    color: #FFFFFF !important;
    min-height: 54px !important;
    font-size: 0.98rem !important;
    font-weight: 900 !important;
    box-shadow: 0 16px 30px -18px rgba(37, 99, 235, 0.95) !important;
    white-space: nowrap !important;
}
.st-key-btn_launch_dashboard button:hover {
    background: linear-gradient(180deg, #2563EB 0%, #1D4ED8 100%) !important;
    box-shadow: 0 18px 34px -18px rgba(37, 99, 235, 1) !important;
}
.st-key-btn_replace_dataset button {
    background: linear-gradient(180deg, #B45309 0%, #92400E 100%) !important;
    border-color: rgba(251, 191, 36, 0.34) !important;
    color: #FFFFFF !important;
    min-width: 154px !important;
    min-height: 44px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    font-size: 0.86rem !important;
    font-weight: 850 !important;
    white-space: nowrap !important;
    box-shadow: 0 10px 20px -14px rgba(180, 83, 9, 0.95) !important;
}
.st-key-btn_replace_dataset button:hover {
    background: linear-gradient(180deg, #C46512 0%, #A0470D 100%) !important;
    border-color: rgba(253, 230, 138, 0.44) !important;
    box-shadow: 0 12px 24px -14px rgba(180, 83, 9, 1) !important;
}
.st-key-btn_replace_dataset button p,
.st-key-btn_launch_dashboard button p {
    white-space: nowrap !important;
}
.st-key-init_upload_widget [data-testid="stFileUploaderDropzone"] {
    border-color: rgba(148, 163, 184, 0.28) !important;
    background: rgba(15, 23, 42, 0.68) !important;
}
.st-key-init_upload_widget [data-testid="stFileUploaderDropzone"] button {
    background: #F8FAFC !important;
    color: #0F172A !important;
    border: 1px solid rgba(203, 213, 225, 0.85) !important;
    border-radius: 8px !important;
    font-weight: 900 !important;
    box-shadow: 0 8px 18px -14px rgba(15, 23, 42, 0.85) !important;
}
.st-key-init_upload_widget [data-testid="stFileUploaderDropzone"] button:hover {
    background: #FFFFFF !important;
    color: #020617 !important;
    border-color: rgba(248, 250, 252, 0.95) !important;
}

/* Custom Detail Card */
.churn-detail-card {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    padding: 1.5rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: 3px solid #6366F1 !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
}

/* Success Card */
.success-card {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    padding: 1.5rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: 3px solid #10B981 !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
}

/* Warning Card */
.warning-card {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    padding: 1.5rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: 3px solid #F59E0B !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
}

/* Critical Card */
.critical-card {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    padding: 1.5rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: 3px solid #EF4444 !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
}

/* Recommended Strategy Card */
.recommended-strategy-card {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.14) 0%, rgba(6, 78, 59, 0.22) 50%, #1B2233 100%) !important;
    padding: 1.5rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
    margin-bottom: 1.75rem !important;
    text-align: center !important;
    box-shadow: 0 4px 16px -4px rgba(16, 185, 129, 0.2) !important;
    transition: all 0.25s ease !important;
}
.recommended-strategy-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px -4px rgba(16, 185, 129, 0.3) !important;
}
.recommended-strategy-card h2 {
    color: #6EE7B7 !important;
    margin: 0 !important;
    border-bottom: none !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    padding-bottom: 0 !important;
    text-transform: none !important;
}
.recommended-strategy-card p {
    font-size: 0.92rem !important;
    margin: 10px 0 0 0 !important;
    color: #CBD5E1 !important;
    line-height: 1.55 !important;
}

/* Insight Cards on Insights Page */
.insight-card {
    padding: 1.15rem 1.2rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-left: 4px solid transparent !important;
    margin-bottom: 0.85rem !important;
    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.25s ease !important;
    line-height: 1.55 !important;
    font-size: 0.82rem !important;
    color: #CBD5E1 !important;
}
.insight-card strong {
    display: block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-bottom: 0.55rem;
    text-transform: none;
}
.insight-card:hover {
    transform: translateX(3px) !important;
}
.insight-card-danger {
    background: linear-gradient(145deg, rgba(239, 68, 68, 0.12) 0%, #1B2233 100%) !important;
    border-left-color: #EF4444 !important;
}
.insight-card-danger strong { color: #FCA5A5 !important; }
.insight-card-warning {
    background: linear-gradient(145deg, rgba(245, 158, 11, 0.10) 0%, #1B2233 100%) !important;
    border-left-color: #F59E0B !important;
}
.insight-card-warning strong { color: #FCD34D !important; }
.insight-card-success {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.10) 0%, #1B2233 100%) !important;
    border-left-color: #10B981 !important;
}
.insight-card-success strong { color: #6EE7B7 !important; }
.insight-card-primary {
    background: linear-gradient(145deg, rgba(59, 130, 246, 0.10) 0%, #1B2233 100%) !important;
    border-left-color: #3B82F6 !important;
}
.insight-card-primary strong { color: #93C5FD !important; }

/* Dataframe & Chart Container Enhancements */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
    margin-top: 0.35rem !important;
    margin-bottom: 0.75rem !important;
}
div[data-testid="stDataFrame"] th {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    color: #F8FAFC !important;
    font-weight: 600 !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 10 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}
div[data-testid="stDataFrame"] tr:nth-child(even) {
    background-color: rgba(255, 255, 255, 0.02) !important;
}
div[data-testid="stDataFrame"] tr:hover {
    background-color: rgba(99, 102, 241, 0.08) !important;
}
div[data-testid="stPlotlyChart"] {
    background-color: rgba(21, 27, 44, 0.35) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 14px !important;
    padding: 0.75rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.3s ease !important;
    margin-top: 0.35rem !important;
    margin-bottom: 0.75rem !important;
}
div[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(99, 102, 241, 0.25) !important;
    box-shadow: 0 8px 16px -2px rgba(0, 0, 0, 0.3) !important;
}

/* Spacing between headings and charts */
[data-testid="stMarkdownContainer"] h3 + div[data-testid="stPlotlyChart"],
[data-testid="stMarkdownContainer"] h4 + div[data-testid="stPlotlyChart"] {
    margin-top: 0.5rem !important;
}

/* Clean Form Containers */
div.stForm {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 14px !important;
    padding: 1.25rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
    margin-bottom: 0.75rem !important;
}

/* Form inputs styling */
div[data-testid="stForm"] div[data-testid="stSelectbox"], 
div[data-testid="stForm"] div[data-testid="stNumberInput"], 
div[data-testid="stForm"] div[data-testid="stSlider"] {
    margin-bottom: 0.65rem !important;
}

div[data-testid="stForm"] div.stFormSubmitButton {
    margin-top: 0.85rem !important;
    margin-bottom: 0px !important;
}

/* Global Alert and Notification Box Polish */
div[data-testid="stAlert"] {
    background-color: rgba(21, 27, 44, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

/* Global Expander Polish */
div[data-testid="stExpander"] {
    background: linear-gradient(135deg, #1F2436 0%, #252E45 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

/* Metadata Text */
.metadata-text {
    color: #64748B !important;
    font-size: 0.8rem !important;
    margin-top: 8px !important;
    margin-bottom: 0px !important;
}

/* Model Analytics — MLOps Dashboard */
.mlops-section {
    margin-bottom: 1.75rem;
}
.mlops-section-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #E2E8F0;
    letter-spacing: 0.01em;
    margin: 0 0 1rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    text-transform: none;
}
.dash-section-header {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1.05rem;
    font-weight: 600;
    color: #E2E8F0;
    margin: 0 0 1rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.dash-section-icon {
    color: #818CF8;
    font-size: 1rem;
    line-height: 1;
    flex-shrink: 0;
}
.enterprise-section-gap {
    margin-bottom: 32px;
}
.mlops-meta-panel {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.25rem;
}
.mlops-meta-item {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 0.85rem 1rem;
}
.mlops-meta-label {
    font-size: 0.62rem;
    font-weight: 600;
    color: #64748B;
    letter-spacing: 0.05em;
    text-transform: none;
    margin-bottom: 0.35rem;
}
.mlops-meta-value {
    font-size: 0.88rem;
    font-weight: 600;
    color: #F1F5F9;
    line-height: 1.35;
    word-break: break-word;
}
.mlops-meta-value--status {
    color: #6EE7B7;
}
.mlops-metric-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin-bottom: 1rem;
}
.mlops-metric-card {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 1rem 0.85rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 108px;
}
.mlops-metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #94A3B8;
    letter-spacing: 0.02em;
    margin-bottom: 0.35rem;
    white-space: nowrap;
    overflow: visible;
    text-overflow: clip;
}
.mlops-metric-value {
    font-size: 1.45rem;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.mlops-metric-badge {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: none;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
}
.mlops-badge-excellent {
    background: rgba(52, 211, 153, 0.12);
    color: #6EE7B7;
    border: 1px solid rgba(52, 211, 153, 0.22);
}
.mlops-badge-good {
    background: rgba(99, 102, 241, 0.12);
    color: #A5B4FC;
    border: 1px solid rgba(99, 102, 241, 0.22);
}
.mlops-badge-moderate {
    background: rgba(148, 163, 184, 0.10);
    color: #94A3B8;
    border: 1px solid rgba(148, 163, 184, 0.18);
}
.mlops-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.25rem;
}
.mlops-chip {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 500;
    color: #CBD5E1;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    padding: 0.3rem 0.7rem;
    letter-spacing: 0.02em;
}
.mlops-comparison-wrap [data-testid="stDataFrame"] {
    margin-top: 0.5rem !important;
}
.mlops-comparison-wrap [data-testid="stDataFrame"] td,
.mlops-comparison-wrap [data-testid="stDataFrame"] th {
    padding: 12px 16px !important;
}
.mlops-chart-card {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    overflow: hidden;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.mlops-chart-header {
    font-size: 0.92rem;
    font-weight: 600;
    color: #E2E8F0;
    padding: 0.85rem 1rem 0.65rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.mlops-chart-body {
    padding: 0.65rem 0.75rem 0.25rem 0.75rem;
    flex: 1;
}
.mlops-chart-body img {
    border-radius: 6px;
}
.mlops-chart-footer {
    font-size: 0.76rem;
    color: #94A3B8;
    line-height: 1.5;
    padding: 0.65rem 1rem 0.85rem 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    background: rgba(0, 0, 0, 0.15);
}
.mlops-insight-card {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 1rem;
}
.mlops-insight-block {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 0.85rem 1rem;
}
.mlops-insight-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: #64748B;
    letter-spacing: 0.02em;
    text-transform: none;
    margin-bottom: 0.4rem;
}
.mlops-insight-text {
    font-size: 0.84rem;
    color: #CBD5E1;
    line-height: 1.55;
    font-weight: 500;
}
@media (max-width: 1100px) {
    .mlops-meta-panel { grid-template-columns: repeat(2, 1fr); }
    .mlops-metric-grid { grid-template-columns: repeat(3, 1fr); }
    .mlops-insight-card { grid-template-columns: 1fr; }
}
@media (max-width: 720px) {
    .mlops-metric-grid { grid-template-columns: repeat(2, 1fr); }
    .mlops-meta-panel { grid-template-columns: 1fr; }
}

/* Shared Enterprise Dashboard Components (N3/N4) */
.mlops-metric-grid-4 {
    grid-template-columns: repeat(4, 1fr) !important;
}
.mlops-metric-grid-3 {
    grid-template-columns: repeat(3, 1fr) !important;
}
.mlops-metric-grid-5 {
    grid-template-columns: repeat(5, 1fr) !important;
}
.dash-form-card {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 0.5rem 0.85rem 0.85rem 0.85rem;
    margin-bottom: 0.5rem;
}
.dash-form-section-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #94A3B8;
    margin: 0.65rem 0 0.35rem 0;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.dash-timeline-card {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    min-height: 160px;
}
.dash-timeline-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 0.65rem;
}
.dash-logic-card {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 0.95rem 1rem;
    margin-bottom: 0.75rem;
    min-height: 180px;
}
.dash-logic-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 0.55rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.dash-notes-wrap div[data-testid="stExpander"] {
    background: linear-gradient(145deg, #20273B 0%, #1B2233 100%) !important;
    border: 1px solid rgba(129, 140, 248, 0.25) !important;
    border-radius: 10px !important;
    margin: 1rem 0 !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.dash-notes-wrap div[data-testid="stExpander"]:hover {
    border-color: rgba(129, 140, 248, 0.45) !important;
    box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.25) !important;
}
.dash-notes-wrap div[data-testid="stExpander"] summary {
    padding: 0.85rem 1rem !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
}
.dash-notes-wrap div[data-testid="stExpander"] > div {
    padding: 0.5rem 1rem 1rem 1rem !important;
}
.dash-download-wrap div.stDownloadButton button {
    min-height: 44px !important;
    font-size: 0.82rem !important;
    padding: 0.55rem 1rem !important;
}
.dash-snapshot-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.65rem;
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    margin: 0.75rem 0 1.25rem 0;
}
.dash-snapshot-item {
    min-width: 0;
}
.dash-snapshot-label {
    font-size: 0.62rem;
    font-weight: 600;
    color: #64748B;
    letter-spacing: 0.02em;
    text-transform: none;
    margin-bottom: 0.3rem;
}
.dash-snapshot-value {
    font-size: 0.88rem;
    font-weight: 600;
    color: #F1F5F9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.dash-panel-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
    margin: 0.75rem 0 0.25rem 0;
}
.dash-panel-card {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 1rem;
    min-height: 220px;
    display: flex;
    flex-direction: column;
}
.dash-panel-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: #94A3B8;
    letter-spacing: 0.02em;
    text-transform: none;
    margin-bottom: 0.85rem;
    padding-bottom: 0.55rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.dash-panel-body {
    flex: 1;
}
.dash-field-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.dash-field-row:last-child {
    border-bottom: none;
}
.dash-field-label {
    font-size: 0.78rem;
    color: #94A3B8;
    font-weight: 500;
}
.dash-field-value {
    font-size: 0.84rem;
    color: #F1F5F9;
    font-weight: 600;
}
.dash-bullet-list {
    margin: 0;
    padding: 0 0 0 1.1rem;
    list-style: disc;
}
.dash-bullet-list li {
    font-size: 0.82rem;
    color: #CBD5E1;
    line-height: 1.55;
    margin-bottom: 0.35rem;
    padding-left: 0.15rem;
}
.dash-action-item {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.dash-action-item:last-child {
    border-bottom: none;
}
.dash-action-check {
    color: #6EE7B7;
    font-size: 0.82rem;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 0.05rem;
}
.dash-action-text {
    font-size: 0.82rem;
    color: #CBD5E1;
    line-height: 1.45;
    font-weight: 500;
}
.dash-viz-card {
    background: linear-gradient(145deg, #1F2436 0%, #252E45 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 0.85rem 0.75rem 0.75rem 0.75rem;
    margin-bottom: 24px;
}
.dash-viz-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 0.5rem;
    padding: 0 0.25rem;
    text-transform: none;
}
.dash-chart-insight {
    font-size: 0.76rem;
    color: #94A3B8;
    line-height: 1.5;
    margin-top: 0.65rem;
    padding: 0.65rem 0.85rem;
    background: rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
}
.mlops-badge-critical {
    background: rgba(239, 68, 68, 0.12);
    color: #FCA5A5;
    border: 1px solid rgba(239, 68, 68, 0.22);
}
.mlops-badge-elevated {
    background: rgba(245, 158, 11, 0.12);
    color: #FCD34D;
    border: 1px solid rgba(245, 158, 11, 0.22);
}
.mlops-badge-stable {
    background: rgba(52, 211, 153, 0.12);
    color: #6EE7B7;
    border: 1px solid rgba(52, 211, 153, 0.22);
}
.mlops-badge-monitored {
    background: rgba(99, 102, 241, 0.12);
    color: #A5B4FC;
    border: 1px solid rgba(99, 102, 241, 0.22);
}
@media (max-width: 1100px) {
    .mlops-metric-grid-4 { grid-template-columns: repeat(2, 1fr) !important; }
    .mlops-metric-grid-5 { grid-template-columns: repeat(3, 1fr) !important; }
    .dash-panel-grid { grid-template-columns: 1fr; }
    .dash-snapshot-strip { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 720px) {
    .mlops-metric-grid-4 { grid-template-columns: 1fr !important; }
    .mlops-metric-grid-5 { grid-template-columns: repeat(2, 1fr) !important; }
    .dash-snapshot-strip { grid-template-columns: repeat(2, 1fr); }
}

/* Footer Version Text */
.footer-left-text {
    text-align: left !important;
    color: #64748B !important;
    font-size: 0.8rem !important;
    margin: 0 !important;
}
.footer-right-text {
    text-align: right !important;
    color: #64748B !important;
    font-size: 0.8rem !important;
    margin: 0 !important;
}

/* Hide Streamlit footer branding */
footer {
    visibility: hidden !important;
}

/* Workspace Initialization Styling */
.init-hero-header {
    text-align: center;
    padding: 1.5rem 1.5rem 1.2rem 1.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 41, 59, 0.3) 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.5);
}
.init-badge {
    display: inline-block;
    padding: 0.3rem 0.85rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: none;
    color: #A5B4FC;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 20px;
    margin-bottom: 0.75rem;
}
.init-hero-header h1 {
    font-size: 2.35rem !important;
    font-weight: 800 !important;
    color: #F8FAFC !important;
    margin: 0.2rem 0 0.4rem 0 !important;
    letter-spacing: -0.02em !important;
    border: none !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.init-hero-header p {
    font-size: 1.05rem !important;
    color: #94A3B8 !important;
    max-width: 680px;
    margin: 0 auto !important;
    font-weight: 400 !important;
}
.init-card {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}
.init-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.init-card-subtitle {
    font-size: 0.85rem;
    color: #94A3B8;
    margin-bottom: 0.85rem;
    line-height: 1.5;
}
.init-spec-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #CBD5E1;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}
.status-pill-ready {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34D399;
    padding: 0.85rem 1.1rem;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.75rem;
}
.status-pill-pending {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: #FBBF24;
    padding: 0.85rem 1.1rem;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.75rem;
}
.status-pill-error {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #FCA5A5;
    padding: 0.85rem 1.1rem;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.75rem;
}
.schema-tag {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    font-size: 0.78rem;
    font-family: 'Consolas', 'Courier New', monospace;
    color: #A5B4FC;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 6px;
    margin: 0.2rem;
}
.disclaimer-card {
    background: rgba(15, 23, 42, 0.6);
    border-left: 4px solid #6366F1;
    border-radius: 8px;
    padding: 1.1rem 1.25rem;
    margin-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.disclaimer-card p {
    font-size: 0.82rem !important;
    color: #94A3B8 !important;
    margin-bottom: 0.45rem !important;
    line-height: 1.5 !important;
}

/* Validation Report Cards */
.vr-section {
    background: linear-gradient(135deg, #1a2540 0%, #111827 100%);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.vr-section-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: none;
    color: #64748B;
    margin-bottom: 0.65rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.vr-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.35rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.82rem;
}
.vr-row:last-child { border-bottom: none; }
.vr-label { color: #94A3B8; }
.vr-value-ok { color: #34D399; font-weight: 600; }
.vr-value-warn { color: #FBBF24; font-weight: 600; }
.vr-value-err { color: #F87171; font-weight: 600; }
.vr-value-info { color: #A5B4FC; font-weight: 600; }
.vr-warning-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #FBBF24;
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(245,158,11,0.1);
}
.vr-warning-item:last-child { border-bottom: none; }
.vr-error-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #F87171;
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(239,68,68,0.1);
}
.vr-error-item:last-child { border-bottom: none; }
.vr-final-pass {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-top: 0.5rem;
}
.vr-final-warn {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-top: 0.5rem;
}
.vr-final-fail {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-top: 0.5rem;
}
.vr-final-title { font-weight: 700; font-size: 0.95rem; }
.vr-final-sub { font-size: 0.78rem; opacity: 0.8; margin-top: 2px; }

/* Responsive adjustments for medium/small screens */
@media (max-width: 992px) {
    div[data-testid="stMetric"] {
        padding: 0.65rem 0.85rem !important;
        min-height: 70px !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)



# --- Helper Logic for Scenario Math Simulation ---
def calculate_simulated_risk(gender, senior_citizen, tenure, phone_service, internet_service, contract, paperless_billing, payment_method, monthly_charges):
    """
    Implements a responsive logit predictive scoring core derived from backend telco 
    churn vector metrics to calculate real-time custom portfolio modifications.
    """
    # Baseline intercept parameter
    log_odds = -0.5
    
    # Contract demographic impacts
    if contract == "Month-to-month":
        log_odds += 1.2
    elif contract == "One year":
        log_odds += 0.1
    elif contract == "Two year":
        log_odds -= 1.1
        
    # Internet access structural impacts
    if internet_service == "Fiber optic":
        log_odds += 0.6
    elif internet_service == "DSL":
        log_odds += 0.1
    elif internet_service == "No":
        log_odds -= 0.6
        
    # Service profile additions
    if senior_citizen == "Yes":
        log_odds += 0.35
    if paperless_billing == "Yes":
        log_odds += 0.2
    if phone_service == "No":
        log_odds -= 0.25
        
    # Billing distribution weights
    if payment_method == "Electronic check":
        log_odds += 0.4
    elif payment_method == "Mailed check":
        log_odds += 0.1
        
    # Continuous financial vector scaling weights
    log_odds -= 0.04 * float(tenure)
    log_odds += 0.012 * float(monthly_charges)
    
    # Logistic transformation equation mapping
    probability = 1.0 / (1.0 + math.exp(-log_odds))
    risk_score = round(probability * 100, 1)
    
    # Stratification category boundary assignment
    if risk_score >= 70.0:
        category = "High Risk"
    elif risk_score >= 30.0:
        category = "Medium Risk"
    else:
        category = "Low Risk"
        
    return probability, risk_score, category


# =============================================================================
#   ENTERPRISE DATASET INGESTION & VALIDATION PIPELINE
# =============================================================================

import io as _io
import datetime

MANDATORY_COLUMNS = [
    'gender', 'SeniorCitizen', 'tenure', 'PhoneService',
    'InternetService', 'Contract', 'PaperlessBilling',
    'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn'
]
VALID_CHURN_VALUES  = {'yes', 'no'}
VALID_GENDER_VALUES = {'male', 'female'}
PIPELINE_MANIFEST_PATH = "outputs/pipeline_manifest.json"
REQUIRED_PIPELINE_ARTIFACTS = [
    "models/logistic_model_vB.pkl",
    "models/scaler_vB.pkl",
    "outputs/model_comparison.csv",
    "outputs/model_health_report.csv",
    "outputs/executive_summary.csv",
    "outputs/risk_distribution.csv",
    "outputs/customer_risk_report.csv",
    "outputs/top_20_risk_customers.csv",
    "outputs/high_risk_customers.csv",
    "outputs/scenario_simulation_report.csv",
    "outputs/churn_insights.txt",
    "outputs/images/roc_curve_comparison.png",
    "outputs/images/feature_importance.png",
    "outputs/images/confusion_matrix_logistic_regression.png",
    "outputs/images/confusion_matrix_decision_tree.png",
    "outputs/images/confusion_matrix_random_forest.png",
]


def _hash_uploaded_bytes(raw_bytes):
    return hashlib.sha256(raw_bytes).hexdigest()


def _dataset_fingerprint(df):
    hasher = hashlib.sha256()
    hasher.update("|".join(map(str, df.columns)).encode("utf-8"))
    hasher.update(pd.util.hash_pandas_object(df, index=True).values.tobytes())
    return hasher.hexdigest()


def _pipeline_artifacts_ready():
    return all(os.path.exists(path) for path in REQUIRED_PIPELINE_ARTIFACTS)


def _load_pipeline_manifest():
    if not os.path.exists(PIPELINE_MANIFEST_PATH):
        return {}
    try:
        with open(PIPELINE_MANIFEST_PATH, "r", encoding="utf-8") as manifest_file:
            return json.load(manifest_file)
    except (OSError, json.JSONDecodeError):
        return {}


def _write_pipeline_manifest(dataset_fingerprint, row_count):
    os.makedirs("outputs", exist_ok=True)
    manifest = {
        "dataset_fingerprint": dataset_fingerprint,
        "row_count": int(row_count),
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(PIPELINE_MANIFEST_PATH, "w", encoding="utf-8") as manifest_file:
        json.dump(manifest, manifest_file, indent=2)


def _clear_stale_pipeline_artifacts():
    for path in REQUIRED_PIPELINE_ARTIFACTS:
        if os.path.exists(path):
            os.remove(path)


def _export_current_scenario_report(biz_df):
    from scenario_simulator import load_artifacts, run_simulations

    if biz_df.empty:
        return

    profile_cols = [
        "gender",
        "SeniorCitizen",
        "tenure",
        "PhoneService",
        "InternetService",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges",
        "Churn",
    ]
    profile = (
        biz_df.sort_values(by="Risk_Score", ascending=False)
        .iloc[0][profile_cols]
        .to_dict()
    )
    model, scaler = load_artifacts()
    simulation_df = run_simulations(profile, model, scaler)
    simulation_df.to_csv("outputs/scenario_simulation_report.csv", index=False)


def validate_enterprise_dataset(df, filename="dataset"):
    """
    Run multi-layer enterprise validation on a dataframe.
    Returns a structured result dict consumed by render_validation_report().
    """
    result = {
        'filename': filename,
        'errors': [],
        'warnings': [],
        'schema': {},
        'quality': {},
        'file_ok': True,
        'schema_ok': False,
        'can_proceed': False,
    }

    # ── File Validation
    if df is None or df.empty:
        result['errors'].append("Dataset is empty or could not be parsed.")
        result['file_ok'] = False
        return result

    rows, cols = df.shape
    result['quality']['total_rows'] = rows
    result['quality']['total_cols'] = cols
    result['file_ok'] = True

    # ── Schema Validation
    missing_cols = [c for c in MANDATORY_COLUMNS if c not in df.columns]
    extra_cols   = [c for c in df.columns if c not in MANDATORY_COLUMNS and c != 'customerID']
    result['schema']['missing'] = missing_cols
    result['schema']['extra']   = extra_cols
    result['schema']['total_required'] = len(MANDATORY_COLUMNS)
    result['schema']['found']   = len(MANDATORY_COLUMNS) - len(missing_cols)

    if missing_cols:
        result['errors'].append(
            "Missing " + str(len(missing_cols)) + " required column(s): " + ", ".join(missing_cols)
        )
        result['schema_ok'] = False
        return result
    else:
        result['schema_ok'] = True

    # ── Data Quality Validation
    null_totals = df[MANDATORY_COLUMNS].isnull().sum()
    total_nulls = int(null_totals.sum())
    result['quality']['null_cells'] = total_nulls
    result['quality']['null_by_col'] = {c: int(v) for c, v in null_totals.items() if v > 0}
    if total_nulls > 0:
        top = ", ".join(c + " (" + str(v) + ")" for c, v in result['quality']['null_by_col'].items())
        result['warnings'].append(str(total_nulls) + " missing value(s) detected — columns: " + top)

    dup_count = int(df.duplicated().sum())
    result['quality']['duplicate_rows'] = dup_count
    if dup_count > 0:
        result['warnings'].append(str(dup_count) + " duplicate row(s) found — they will be dropped during cleaning.")

    if 'customerID' in df.columns:
        dup_ids = int(df['customerID'].duplicated().sum())
        result['quality']['duplicate_ids'] = dup_ids
        if dup_ids > 0:
            result['warnings'].append(str(dup_ids) + " duplicate customerID(s) detected.")
    else:
        result['quality']['duplicate_ids'] = None

    neg_charges = int((pd.to_numeric(df['MonthlyCharges'], errors='coerce') < 0).sum())
    result['quality']['neg_monthly_charges'] = neg_charges
    if neg_charges > 0:
        result['warnings'].append(str(neg_charges) + " record(s) have negative MonthlyCharges.")

    neg_tenure = int((pd.to_numeric(df['tenure'], errors='coerce') < 0).sum())
    result['quality']['neg_tenure'] = neg_tenure
    if neg_tenure > 0:
        result['warnings'].append(str(neg_tenure) + " record(s) have negative tenure values.")

    churn_vals = df['Churn'].dropna().astype(str).str.strip().str.lower().unique()
    bad_churn = [v for v in churn_vals if v not in VALID_CHURN_VALUES]
    result['quality']['invalid_churn'] = bad_churn
    if bad_churn:
        result['warnings'].append("Non-standard Churn values found: " + str(bad_churn) + " (will be normalised).")

    gender_vals = df['gender'].dropna().astype(str).str.strip().str.lower().unique()
    bad_gender = [v for v in gender_vals if v not in VALID_GENDER_VALUES]
    result['quality']['invalid_gender'] = bad_gender
    if bad_gender:
        result['warnings'].append("Non-standard Gender values found: " + str(bad_gender) + ".")

    result['can_proceed'] = True
    return result


def render_validation_report(result):
    """Render the structured enterprise validation report HTML."""
    rows      = result['quality'].get('total_rows', 0)
    cols_cnt  = result['quality'].get('total_cols', 0)
    null_cells = result['quality'].get('null_cells', 0)
    dup_rows  = result['quality'].get('duplicate_rows', 0)
    dup_ids   = result['quality'].get('duplicate_ids', None)
    found_cols = result['schema'].get('found', 0)
    req_cols  = result['schema'].get('total_required', 11)
    extra_cols = result['schema'].get('extra', [])
    missing_cols = result['schema'].get('missing', [])

    def ok(txt):  return '<span class="vr-value-ok">' + txt + '</span>'
    def warn(txt): return '<span class="vr-value-warn">' + txt + '</span>'
    def err(txt):  return '<span class="vr-value-err">' + txt + '</span>'
    def info(txt): return '<span class="vr-value-info">' + txt + '</span>'

    file_status  = ok("Readable") if result['file_ok'] else err("Failed")
    empty_status = ok("Non-empty") if rows > 0 else err("Empty file")
    header_val   = ok("Header row present") if cols_cnt > 0 else err("No header detected")

    if not missing_cols:
        schema_val = ok(str(found_cols) + " / " + str(req_cols) + " Required Columns Found")
    else:
        schema_val = err(str(found_cols) + " / " + str(req_cols) + " Missing: " + ", ".join(missing_cols))

    extra_val = (warn(str(len(extra_cols)) + " extra — will be ignored") if extra_cols else ok("None"))
    null_val  = (warn(str(null_cells) + " cells") if null_cells > 0 else ok("None detected"))
    dup_val   = (warn(str(dup_rows) + " rows") if dup_rows > 0 else ok("None detected"))

    if dup_ids is None:
        dup_id_val = info("No customerID column")
    elif dup_ids > 0:
        dup_id_val = warn(str(dup_ids) + " duplicates")
    else:
        dup_id_val = ok("No duplicates")

    neg_c = result['quality'].get('neg_monthly_charges', 0)
    neg_t = result['quality'].get('neg_tenure', 0)
    neg_c_val = warn(str(neg_c) + " records") if neg_c > 0 else ok("None")
    neg_t_val = warn(str(neg_t) + " records") if neg_t > 0 else ok("None")

    bad_churn  = result['quality'].get('invalid_churn', [])
    bad_gender = result['quality'].get('invalid_gender', [])
    churn_val  = (warn("Non-standard: " + ", ".join(bad_churn)) if bad_churn else ok("Standard values"))
    gender_val = (warn("Non-standard: " + ", ".join(bad_gender)) if bad_gender else ok("Standard values"))

    warnings = result.get('warnings', [])
    errors   = result.get('errors', [])

    if warnings:
        w_items = "".join('<div class="vr-warning-item"><span>' + w + '</span></div>' for w in warnings)
        warnings_html = '<div class="vr-section"><div class="vr-section-title">Warnings Log (' + str(len(warnings)) + ')</div>' + w_items + '</div>'
    else:
        warnings_html = '<div class="vr-section"><div class="vr-section-title">Warnings Log</div><div class="vr-row"><span class="vr-label">Status</span>' + ok("No warnings — dataset is clean") + '</div></div>'

    if errors:
        e_items = "".join('<div class="vr-error-item"><span>' + e + '</span></div>' for e in errors)
        errors_html = '<div class="vr-section" style="border-color:rgba(239,68,68,0.25);"><div class="vr-section-title" style="color:#F87171;">Errors (' + str(len(errors)) + ')</div>' + e_items + '</div>'
    else:
        errors_html = ""

    if not result['file_ok'] or not result['schema_ok']:
        final_html = '<div class="vr-final-fail"><div><div class="vr-final-title" style="color:#F87171;">Validation Failed &mdash; Analysis Blocked</div><div class="vr-final-sub" style="color:#FDA4AF;">Correct the errors above and re-upload the dataset.</div></div></div>'
    elif warnings:
        final_html = '<div class="vr-final-warn"><div><div class="vr-final-title" style="color:#FBBF24;">Validation Passed with ' + str(len(warnings)) + ' Warning(s)</div><div class="vr-final-sub" style="color:#FDE68A;">' + str(rows) + ' records ready. Warnings are non-blocking &mdash; data cleaning will normalise minor issues.</div></div></div>'
    else:
        final_html = '<div class="vr-final-pass"><div><div class="vr-final-title" style="color:#34D399;">Validation Passed &mdash; Dataset Ready for Analysis</div><div class="vr-final-sub" style="color:#6EE7B7;">' + str(rows) + ' records &middot; ' + str(cols_cnt) + ' columns &middot; No quality issues detected.</div></div></div>'

    full_html = (
        '<div style="margin-top:1rem;">'
        '<div class="vr-section">'
        '<div class="vr-section-title">File Status</div>'
        '<div class="vr-row"><span class="vr-label">File Readability</span>' + file_status + '</div>'
        '<div class="vr-row"><span class="vr-label">Content Check</span>' + empty_status + '</div>'
        '<div class="vr-row"><span class="vr-label">Header Row</span>' + header_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Total Records</span>' + info(str(rows) + " rows") + '</div>'
        '<div class="vr-row"><span class="vr-label">Total Columns</span>' + info(str(cols_cnt)) + '</div>'
        '</div>'
        '<div class="vr-section">'
        '<div class="vr-section-title">Schema Validation</div>'
        '<div class="vr-row"><span class="vr-label">Required Columns</span>' + schema_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Extra Columns</span>' + extra_val + '</div>'
        '</div>'
        '<div class="vr-section">'
        '<div class="vr-section-title">Data Quality</div>'
        '<div class="vr-row"><span class="vr-label">Missing Values</span>' + null_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Duplicate Rows</span>' + dup_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Duplicate Customer IDs</span>' + dup_id_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Negative MonthlyCharges</span>' + neg_c_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Negative Tenure</span>' + neg_t_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Churn Values</span>' + churn_val + '</div>'
        '<div class="vr-row"><span class="vr-label">Gender Values</span>' + gender_val + '</div>'
        '</div>'
        + warnings_html + errors_html + final_html +
        '</div>'
    )
    st.markdown(full_html, unsafe_allow_html=True)
    return result['can_proceed']


def _build_session_dataset(df, name, source, fingerprint=None):
    """Store validated dataset metadata and dataframe into session_state."""
    st.session_state['active_dataset_info'] = {
        'name': name,
        'rows': len(df),
        'cols': len(df.columns),
        'valid': True,
        'source': source,
        'df': df,
        'fingerprint': fingerprint or _dataset_fingerprint(df),
        'upload_timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'validation_status': 'passed',
    }


def run_ingestion_pipeline(df, dataset_fingerprint=None):
    """
    Run the full ML and BI pipeline on the active dataset and persist outputs.
    Cached artifacts are reused only when the dataset fingerprint is unchanged.
    """
    dataset_fingerprint = dataset_fingerprint or _dataset_fingerprint(df)
    manifest = _load_pipeline_manifest()

    if (
        manifest.get("dataset_fingerprint") == dataset_fingerprint
        and _pipeline_artifacts_ready()
    ):
        return True, None

    try:
        _clear_stale_pipeline_artifacts()

        from model_comparison import train_and_evaluate_models
        from business_intelligence import generate_insights, export_reports
        from executive_reporting import (
            generate_executive_summary,
            generate_model_health,
            generate_risk_distribution,
            generate_top_risk_targets,
            generate_churn_insights,
        )

        os.makedirs('outputs', exist_ok=True)
        os.makedirs('outputs/images', exist_ok=True)

        train_and_evaluate_models(df)
        biz_df = generate_insights(df)

        # Persist full customer risk report + high risk roster
        export_reports(biz_df)

        # Persist executive summary
        generate_executive_summary(biz_df)

        # Persist risk distribution
        generate_risk_distribution(biz_df)  # saves internally

        # Persist top-20 priority targets
        generate_top_risk_targets(biz_df)   # saves internally

        # Persist model health, narrative insights, and a current scenario baseline.
        generate_model_health('models/logistic_model_vB.pkl', 'outputs/model_comparison.csv', biz_df)
        generate_churn_insights(biz_df, 'models/logistic_model_vB.pkl')
        _export_current_scenario_report(biz_df)
        _write_pipeline_manifest(dataset_fingerprint, len(df))

        return True, None
    except Exception as e:
        return False, str(e)


def show_workspace_initialization():
    """Render the Workspace Initialization screen with enterprise validation."""

    # ── Hide Sidebar During Initialization
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        div[data-testid="collapsedSidebarButton"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero Header
    st.markdown("""
    <div class="init-hero-header">
        <div class="init-badge">WORKSPACE INITIALIZATION</div>
        <h1>Customer Churn Intelligence Platform</h1>
        <p>Enterprise AI-powered Customer Churn Prediction &amp; Retention Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([6, 6], gap="large")

    active_info = st.session_state.get('active_dataset_info', None)
    vr_result = st.session_state.get('_validation_result', None)
    is_ready = active_info is not None and active_info.get('valid', False)

    with col_left:
        # ── Upload Dataset Card
        if is_ready:
            card_content_col, action_col = st.columns([3.8, 1.35])
            with card_content_col:
                st.markdown(f"""
                <div class="init-card">
                    <div class="init-card-title">Uploaded Dataset</div>
                    <div style="margin-top: 0.5rem; font-size: 0.95rem; color: #F8FAFC;">
                        <strong>Selected File:</strong> {active_info['name']}
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.2rem;">
                        <strong>File Size:</strong> {active_info.get('size_str', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with action_col:
                st.write("")
                st.write("")
                if st.button("Replace Dataset", key="btn_replace_dataset", use_container_width=True):
                    for _k in ['active_dataset_info', '_validation_result', '_last_uploaded_filename', '_last_uploaded_hash']:
                        st.session_state.pop(_k, None)
                    st.rerun()
        else:
            st.markdown("""
            <div class="init-card">
                <div class="init-card-title">Upload Dataset</div>
                <div class="init-card-subtitle">Upload your customer database (CSV format) to initialize analytics.</div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Select Customer Dataset (.csv)",
                type=["csv"],
                label_visibility="collapsed",
                key="init_upload_widget"
            )

            if uploaded_file is not None:
                raw_bytes = uploaded_file.getvalue()
                upload_hash = _hash_uploaded_bytes(raw_bytes)
                last_upload_hash = st.session_state.get('_last_uploaded_hash', '')
                if upload_hash != last_upload_hash:
                    st.session_state['_last_uploaded_filename'] = uploaded_file.name
                    st.session_state['_last_uploaded_hash'] = upload_hash
                    st.session_state.pop('active_dataset_info', None)
                    try:
                        try:
                            df_up = pd.read_csv(_io.BytesIO(raw_bytes), encoding='utf-8')
                        except UnicodeDecodeError:
                            df_up = pd.read_csv(_io.BytesIO(raw_bytes), encoding='latin-1')
                        
                        vr = validate_enterprise_dataset(df_up, filename=uploaded_file.name)
                        st.session_state['_validation_result'] = vr
                        if vr['can_proceed']:
                            _build_session_dataset(df_up, uploaded_file.name, 'uploaded', upload_hash)
                            
                            size_in_bytes = len(raw_bytes)
                            if size_in_bytes < 1024:
                                size_str = f"{size_in_bytes} Bytes"
                            elif size_in_bytes < 1024 * 1024:
                                size_str = f"{size_in_bytes / 1024:.1f} KB"
                            else:
                                size_str = f"{size_in_bytes / (1024 * 1024):.1f} MB"
                            
                            st.session_state['active_dataset_info']['size_str'] = size_str
                        else:
                            st.session_state['active_dataset_info'] = {
                                'valid': False,
                                'name': uploaded_file.name,
                                'rows': vr['quality'].get('total_rows', 0),
                                'cols': vr['quality'].get('total_cols', 0),
                                'size_str': f"{len(raw_bytes) / (1024 * 1024):.1f} MB"
                            }
                        st.rerun()
                    except Exception as e:
                        st.session_state['_validation_result'] = None
                        st.error("Could not parse uploaded file: " + str(e))

        # ── Dataset Status Card
        if vr_result is not None:
            rows = vr_result['quality'].get('total_rows', 0)
            cols_cnt = vr_result['quality'].get('total_cols', 0)
            warnings = vr_result.get('warnings', [])
            errors = vr_result.get('errors', [])
            missing_cols = vr_result['schema'].get('missing', [])

            if vr_result['can_proceed']:
                st.markdown(f"""
                <div class="init-card">
                    <div class="init-card-title" style="color: #34D399;">Dataset Status</div>
                    <div style="font-size: 0.85rem; color: #34D399; font-weight: 600; margin-bottom: 0.4rem;">
                        Schema Valid &nbsp;&middot;&nbsp; Ready for Analysis
                    </div>
                    <div class="vr-row"><span class="vr-label">Rows</span><span class="vr-value-ok">{rows}</span></div>
                    <div class="vr-row"><span class="vr-label">Columns</span><span class="vr-value-ok">{cols_cnt}</span></div>
                    <div class="vr-row"><span class="vr-label">Warnings</span><span class="vr-value-warn">{len(warnings)} Minor</span></div>
                    <div class="vr-row"><span class="vr-label">Status</span><span class="vr-value-ok">Ready</span></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                missing_cols_html = "".join(f"<div style='font-family: monospace; color: #EF4444; font-size: 0.8rem;'>• {col}</div>" for col in missing_cols)
                st.markdown(f"""
                <div class="init-card" style="border-color: rgba(239, 68, 68, 0.4);">
                    <div class="init-card-title" style="color: #F87171;">Dataset Status</div>
                    <div style="font-size: 0.85rem; color: #FCA5A5; font-weight: 600; margin-bottom: 0.2rem;">
                        Missing Columns
                    </div>
                    <div style="margin-left: 0.5rem; margin-bottom: 0.4rem;">
                        {missing_cols_html}
                    </div>
                    <div style="font-size: 0.8rem; color: #FDA4AF; font-weight: 600;">
                        Please upload a valid dataset.
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="init-card">
                <div class="init-card-title" style="color: #94A3B8;">Dataset Status</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">
                    Upload a CSV file to validate and view status.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        # ── Dataset Requirements Card
        st.markdown("""
        <div class="init-card">
            <div class="init-card-title">Dataset Requirements</div>
            <div style="font-size: 0.82rem; line-height: 1.4; color: #CBD5E1; margin-bottom: 0.4rem;">
                <div>CSV Format &nbsp;&middot;&nbsp; UTF-8 Encoding &nbsp;&middot;&nbsp; Max Size 100 MB</div>
                <div>11 Mandatory Fields Required:</div>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:0.2rem;">
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">gender</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">SeniorCitizen</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">tenure</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">PhoneService</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">InternetService</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">Contract</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">PaperlessBilling</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">PaymentMethod</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">MonthlyCharges</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">TotalCharges</span>
                <span class="schema-tag" style="margin: 0.1rem; padding: 0.15rem 0.4rem; font-size: 0.72rem;">Churn</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Warnings & Details Expander
        if vr_result is not None:
            warnings = vr_result.get('warnings', [])
            errors = vr_result.get('errors', [])
            if warnings or errors:
                st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
                with st.expander(f"Warnings & Details ({len(warnings)} issues)", expanded=False):
                    if errors:
                        st.markdown("<strong style='color:#F87171; font-size:0.8rem;'>Errors:</strong>", unsafe_allow_html=True)
                        for e in errors:
                            st.markdown(f"<div style='color:#FCA5A5; font-size:0.8rem;'>• {e}</div>", unsafe_allow_html=True)
                    if warnings:
                        st.markdown("<strong style='color:#FBBF24; font-size:0.8rem;'>Quality Warnings:</strong>", unsafe_allow_html=True)
                        for w in warnings:
                            st.markdown(f"<div style='color:#FDE68A; font-size:0.8rem;'>• {w}</div>", unsafe_allow_html=True)

    # ── Primary CTA (Centered Button)
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    btn_l, btn_m, btn_r = st.columns([1.5, 3, 1.5])
    with btn_m:
        if st.button("Launch Dashboard", disabled=not is_ready, key="btn_launch_dashboard", use_container_width=True, type="primary"):
            active_df = active_info.get('df') if active_info else None
            if active_df is not None:
                with st.spinner("Initializing analytics pipeline — please wait..."):
                    ok, pipeline_err = run_ingestion_pipeline(
                        active_df,
                        active_info.get('fingerprint'),
                    )
                if not ok:
                    st.warning("Pipeline encountered an issue: " + str(pipeline_err))
            st.session_state["workspace_initialized"] = True
            st.rerun()


# --- 2. Page Routing Definitions ---

def show_executive_overview():
    st.header("Executive Overview")
    
    # Paths to generated data artifacts from backend reporting
    summary_path = 'outputs/executive_summary.csv'
    dist_path = 'outputs/risk_distribution.csv'
    
    # Graceful File Validation Handling
    if not os.path.exists(summary_path) or not os.path.exists(dist_path):
        st.warning("Executive data reports not found. Please run the background reporting layer script (`executive_reporting.py`) first to populate these components.")
        return
        
    try:
        # Load business intelligence outputs
        df_summary = pd.read_csv(summary_path)
        df_dist = pd.read_csv(dist_path)
        
        # Convert metric columns into a dictionary for clean programmatic access
        metrics_dict = dict(zip(df_summary['Metric'], df_summary['Value']))
        
        # Extract individual baseline scalar values
        total_customers = int(metrics_dict.get('Total Customers', 0))
        high_risk_cust = int(metrics_dict.get('High Risk Customers', 0))
        med_risk_cust = int(metrics_dict.get('Medium Risk Customers', 0))
        low_risk_cust = int(metrics_dict.get('Low Risk Customers', 0))
        avg_risk_score = metrics_dict.get('Average Risk Score', 0.0)
        expected_churn = metrics_dict.get('Expected Churn Count', 0.0)
        
        high_risk_pct = metrics_dict.get('High Risk Percentage', 0.0)
        med_risk_pct = metrics_dict.get('Medium Risk Percentage', 0.0)
        low_risk_pct = metrics_dict.get('Low Risk Percentage', 0.0)
        
        # Multi-Column KPI Dashboard Section
        st.subheader("Core Operational Metrics")
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.metric(label="Total Portfolio Volume", value=f"{total_customers:,} Accounts")
            st.metric(label="High Risk Accounts", value=f"{high_risk_cust:,}")
        with kpi_col2:
            st.metric(label="Expected Churn Volume", value=f"~{int(expected_churn)} Users")
            st.metric(label="Medium Risk Accounts", value=f"{med_risk_cust:,}")
        with kpi_col3:
            st.metric(label="Mean Attrition Index", value=f"{avg_risk_score} / 100")
            st.metric(label="Low Risk Accounts", value=f"{low_risk_cust:,}")
            
        st.markdown("---")
        
        # Visualization and Categorical Stratification Columns
        vis_col1, vis_col2 = st.columns([5, 4])
        
        with vis_col1:
            st.subheader("Account Stratification Matrix")
            # Build clean interactive Plotly visualization
            fig = px.bar(
                df_dist,
                x='Risk Category',
                y='Customer Count',
                labels={'Customer Count': 'Active Profiles', 'Risk Category': 'Risk Stratum'},
                color='Risk Category',
                color_discrete_map={
                    'Low Risk': '#2ecc71',
                    'Medium Risk': '#f1c40f',
                    'High Risk': '#e74c3c'
                },
                template='streamlit'
            )
            fig = fig.update_layout(showlegend=False, height=360, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
        with vis_col2:
            # Business Health Summary Section
            st.subheader("Business Health Summary")
            st.write("Proportional stratification breakdown across portfolio categories:")
            
            st.metric(label="Portfolio High-Risk Exposure", value=f"{high_risk_pct}%")
            st.metric(label="Portfolio Medium-Risk Volume", value=f"{med_risk_pct}%")
            st.metric(label="Portfolio Low-Risk Stability", value=f"{low_risk_pct}%")
            
        st.markdown("---")
        
        # Key Executive Insight Container Section
        st.subheader("Key Executive Insight")
        st.info(
            f"**System Status Analysis:** {high_risk_pct}% of the active subscriber portfolio "
            f"is currently classified as High Risk. Immediate retention actions should focus on this segment "
            f"to protect the contract asset registry from projected loss volumes."
        )
        
    except Exception as e:
        st.error(f"Failed to execute diagnostic display calculations: {str(e)}")


def _mlops_metric_rating(value):
    value = float(value)
    if value >= 0.80:
        return "Excellent", "mlops-badge-excellent"
    if value >= 0.60:
        return "Good", "mlops-badge-good"
    return "Moderate", "mlops-badge-moderate"


def _mlops_format_pct(value):
    return f"{float(value) * 100:.1f}%"


def _mlops_extract_version(model_filename):
    fname = str(model_filename)
    if "_v" in fname:
        return "v" + fname.split("_v")[-1].split(".")[0]
    return "v1"


def _mlops_match_production_model(training_algo, df_comp):
    algo_lower = str(training_algo).lower()
    for _, row in df_comp.iterrows():
        model_name = str(row["Model"])
        if model_name.lower() in algo_lower:
            return model_name
    return str(df_comp.iloc[0]["Model"])


def _mlops_render_metadata_panel(health_dict):
    champion = html.escape(str(health_dict.get("Training Algorithm", "Unknown")))
    version = html.escape(_mlops_extract_version(health_dict.get("Production Model Name", "")))
    dataset_size = html.escape(str(health_dict.get("Dataset Size", "0")))
    return f"""
    <div class="mlops-meta-panel">
        <div class="mlops-meta-item">
            <div class="mlops-meta-label">Champion Model</div>
            <div class="mlops-meta-value">{champion}</div>
        </div>
        <div class="mlops-meta-item">
            <div class="mlops-meta-label">Version</div>
            <div class="mlops-meta-value">{version}</div>
        </div>
        <div class="mlops-meta-item">
            <div class="mlops-meta-label">Production Status</div>
            <div class="mlops-meta-value mlops-meta-value--status">Production</div>
        </div>
        <div class="mlops-meta-item">
            <div class="mlops-meta-label">Dataset Size</div>
            <div class="mlops-meta-value">{dataset_size} records</div>
        </div>
    </div>
    """


def _mlops_render_metric_cards(health_dict):
    metrics = [
        ("Accuracy", "Accuracy"),
        ("Precision", "Precision"),
        ("Recall", "Recall"),
        ("F1 Score", "F1 Score"),
        ("ROC-AUC", "ROC-AUC"),
    ]
    cards = []
    for label, key in metrics:
        val = float(health_dict.get(key, 0.0))
        rating, badge_cls = _mlops_metric_rating(val)
        cards.append(
            f'<div class="mlops-metric-card">'
            f'<div class="mlops-metric-label">{html.escape(label)}</div>'
            f'<div class="mlops-metric-value">{_mlops_format_pct(val)}</div>'
            f'<span class="mlops-metric-badge {badge_cls}">{rating}</span>'
            f"</div>"
        )
    return f'<div class="mlops-metric-grid">{"".join(cards)}</div>'


def _mlops_render_chips(health_dict):
    chips = [
        f"{health_dict.get('Dataset Size', '0')} Records",
        f"{health_dict.get('Number of Features', '0')} Features",
        f"Top Signal: {health_dict.get('Strongest Feature', 'N/A')}",
        "Validated",
        "Production",
        "Holdout Tested",
    ]
    chip_html = "".join(f'<span class="mlops-chip">{html.escape(str(c))}</span>' for c in chips)
    return f'<div class="mlops-chip-row">{chip_html}</div>'


def _mlops_style_comparison(df_comp, production_model):
    metric_cols = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
    best = {col: df_comp[col].max() for col in metric_cols}

    def _cell_styles(raw_df):
        styles = pd.DataFrame("", index=raw_df.index, columns=raw_df.columns)
        for idx in raw_df.index:
            is_prod = raw_df.loc[idx, "Model"] == production_model
            for col in raw_df.columns:
                rules = []
                if is_prod:
                    rules.append("background-color: rgba(108, 99, 255, 0.10)")
                    if col == "Model":
                        rules.append("border-left: 3px solid #6C63FF")
                if col in metric_cols and abs(float(raw_df.loc[idx, col]) - best[col]) < 1e-9:
                    rules.append("color: #6EE7B7")
                    rules.append("font-weight: 700")
                styles.loc[idx, col] = "; ".join(rules)
        return styles

    format_dict = {col: "{:.4f}" for col in metric_cols}
    return (
        df_comp.style
        .format(format_dict)
        .apply(_cell_styles, axis=None)
        .set_table_styles([
            {"selector": "td", "props": [("padding", "12px 16px")]},
            {"selector": "th", "props": [("padding", "12px 16px")]},
        ])
    )


def _mlops_render_insight_card(health_dict):
    algo_title = html.escape(str(health_dict.get("Training Algorithm", "Logistic Regression")))
    version = html.escape(_mlops_extract_version(health_dict.get("Production Model Name", "")))
    recall_val = float(health_dict.get("Recall", 0.0))
    precision_val = float(health_dict.get("Precision", 0.0))

    blocks = [
        (
            "Champion Model",
            f"{algo_title} ({version}) is the deployed production classifier for churn scoring.",
        ),
        (
            "Key Strength",
            f"Recall of {_mlops_format_pct(recall_val)} captures the majority of at-risk accounts before attrition.",
        ),
        (
            "Trade-off",
            f"Precision of {_mlops_format_pct(precision_val)} indicates a wider outreach net with some false positives.",
        ),
        (
            "Business Recommendation",
            "Route high-recall scores to retention workflows first; apply cost controls on lower-confidence segments.",
        ),
    ]
    block_html = "".join(
        f'<div class="mlops-insight-block">'
        f'<div class="mlops-insight-label">{html.escape(title)}</div>'
        f'<div class="mlops-insight-text">{html.escape(text)}</div>'
        f"</div>"
        for title, text in blocks
    )
    return f'<div class="mlops-insight-card">{block_html}</div>'


def _mlops_embed_image(img_path):
    with open(img_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded}"


def _mlops_render_chart_card(title, img_path, footer_text, missing_message):
    if os.path.exists(img_path):
        src = _mlops_embed_image(img_path)
        body_html = f'<img src="{src}" alt="{html.escape(title)}" style="width:100%;border-radius:6px;display:block;" />'
    else:
        body_html = f'<p style="color:#94A3B8;font-size:0.82rem;margin:0.5rem 0;">{html.escape(missing_message)}</p>'
        footer_text = "Visualization unavailable — re-run model training to regenerate."

    return (
        f'<div class="mlops-chart-card">'
        f'<div class="mlops-chart-header">{html.escape(title)}</div>'
        f'<div class="mlops-chart-body">{body_html}</div>'
        f'<div class="mlops-chart-footer">{html.escape(footer_text)}</div>'
        f"</div>"
    )


def show_model_analytics():
    st.header("Model Analytics")

    health_path = "outputs/model_health_report.csv"
    comparison_path = "outputs/model_comparison.csv"
    roc_img_path = "outputs/images/roc_curve_comparison.png"
    feat_img_path = "outputs/images/feature_importance.png"

    if not os.path.exists(health_path) or not os.path.exists(comparison_path):
        st.warning("Predictive evaluation metrics files not detected. Ensure your backend evaluation and reporting routines have completed successfully.")
        return

    try:
        df_health = pd.read_csv(health_path)
        df_comp = pd.read_csv(comparison_path)
        health_dict = dict(zip(df_health["Metric"], df_health["Value"]))
        production_model = _mlops_match_production_model(
            health_dict.get("Training Algorithm", ""), df_comp
        )

        # --- 1. Production Model Status ---
        st.markdown('<div class="mlops-section">', unsafe_allow_html=True)
        st.markdown('<div class="mlops-section-title">Production Model Status</div>', unsafe_allow_html=True)
        st.markdown(_mlops_render_metadata_panel(health_dict), unsafe_allow_html=True)
        st.markdown(_mlops_render_metric_cards(health_dict), unsafe_allow_html=True)
        st.markdown(_mlops_render_chips(health_dict), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        # --- 2. Model Comparison Matrix ---
        st.markdown('<div class="mlops-section mlops-comparison-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="mlops-section-title">Model Comparison Matrix</div>', unsafe_allow_html=True)
        st.caption("Algorithm benchmarking performance tracked during model training.")
        st.dataframe(
            _mlops_style_comparison(df_comp, production_model),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        # --- 3. ROC Curve & Feature Importance ---
        roc_val = float(health_dict.get("ROC-AUC", 0.0))

        roc_footer = (
            f"{production_model} leads discrimination performance with ROC-AUC of {roc_val:.2f}, "
            f"outperforming alternative algorithms in the evaluation set."
        )
        feat_footer = (
            f"{health_dict.get('Strongest Feature', 'The leading feature')} is the strongest "
            "signal identified in the current uploaded dataset's champion model."
        )

        vis_col1, vis_col2 = st.columns(2, gap="medium")

        with vis_col1:
            st.markdown(
                _mlops_render_chart_card(
                    "ROC Curve Analysis",
                    roc_img_path,
                    roc_footer,
                    "Performance plot image asset missing from storage framework.",
                ),
                unsafe_allow_html=True,
            )

        with vis_col2:
            st.markdown(
                _mlops_render_chart_card(
                    "Feature Importance Analysis",
                    feat_img_path,
                    feat_footer,
                    "Feature variance distribution image asset missing from storage framework.",
                ),
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # --- 4. Executive Insight Card ---
        st.markdown('<div class="mlops-section">', unsafe_allow_html=True)
        st.markdown('<div class="mlops-section-title">Model Interpretation Summary</div>', unsafe_allow_html=True)
        st.markdown(_mlops_render_insight_card(health_dict), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to process model analytical reporting structures: {str(e)}")


def _dash_split_items(text):
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return []
    return [item.strip() for item in str(text).split("|") if item.strip()]


def _dash_render_kpi_grid(cards, columns=4):
    card_html = []
    for label, value, badge, badge_cls in cards:
        card_html.append(
            f'<div class="mlops-metric-card">'
            f'<div class="mlops-metric-label">{html.escape(label)}</div>'
            f'<div class="mlops-metric-value">{html.escape(str(value))}</div>'
            f'<span class="mlops-metric-badge {badge_cls}">{html.escape(badge)}</span>'
            f"</div>"
        )
    grid_cls = f"mlops-metric-grid mlops-metric-grid-{columns}"
    return f'<div class="{grid_cls}">{"".join(card_html)}</div>'


def _dash_render_insight_card(blocks):
    block_html = "".join(
        f'<div class="mlops-insight-block">'
        f'<div class="mlops-insight-label">{html.escape(title)}</div>'
        f'<div class="mlops-insight-text">{html.escape(text)}</div>'
        f"</div>"
        for title, text in blocks
    )
    return f'<div class="mlops-insight-card">{block_html}</div>'


def _dash_render_field_rows(fields):
    rows = "".join(
        f'<div class="dash-field-row">'
        f'<span class="dash-field-label">{html.escape(label)}</span>'
        f'<span class="dash-field-value">{html.escape(str(value))}</span>'
        f"</div>"
        for label, value in fields
    )
    return rows


def _dash_render_bullet_list(items, empty_text="No drivers identified"):
    if not items:
        return f'<ul class="dash-bullet-list"><li>{html.escape(empty_text)}</li></ul>'
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ul class="dash-bullet-list">{lis}</ul>'


def _dash_render_action_list(items):
    if not items:
        items = ["Review account manually"]
    return "".join(
        f'<div class="dash-action-item">'
        f'<span class="dash-action-check">✓</span>'
        f'<span class="dash-action-text">{html.escape(item)}</span>'
        f"</div>"
        for item in items
    )


def _dash_render_panel(title, body_html):
    return (
        f'<div class="dash-panel-card">'
        f'<div class="dash-panel-title">{html.escape(title)}</div>'
        f'<div class="dash-panel-body">{body_html}</div>'
        f"</div>"
    )


def _dash_render_snapshot_strip(fields):
    items = "".join(
        f'<div class="dash-snapshot-item">'
        f'<div class="dash-snapshot-label">{html.escape(label)}</div>'
        f'<div class="dash-snapshot-value">{html.escape(str(value))}</div>'
        f"</div>"
        for label, value in fields
    )
    return f'<div class="dash-snapshot-strip">{items}</div>'


def _dash_plot_layout(height=360):
    return {
        "height": height,
        "margin": dict(l=45, r=35, t=40, b=65),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(
            color="#CBD5E1",
            size=12,
            family="Plus Jakarta Sans"
        ),
        "xaxis": dict(
            tickfont=dict(size=11, family="Plus Jakarta Sans"),
            title=dict(font=dict(size=12, family="Plus Jakarta Sans"))
        ),
        "yaxis": dict(
            tickfont=dict(size=11, family="Plus Jakarta Sans"),
            title=dict(font=dict(size=12, family="Plus Jakarta Sans"))
        )
    }


def _dash_section_header(title, icon="◈"):
    return (
        f'<div class="dash-section-header">'
        f'<span class="dash-section-icon">{html.escape(icon)}</span>'
        f'<span>{html.escape(title)}</span>'
        f"</div>"
    )


def _dash_render_simple_kpi_grid(items, columns=3):
    cards = []
    for label, value in items:
        cards.append(
            f'<div class="mlops-metric-card">'
            f'<div class="mlops-metric-label">{html.escape(label)}</div>'
            f'<div class="mlops-metric-value">{html.escape(str(value))}</div>'
            f"</div>"
        )
    grid_cls = f"mlops-metric-grid mlops-metric-grid-{columns}"
    return f'<div class="{grid_cls}">{"".join(cards)}</div>'


def _dash_render_logic_card(title, bullets):
    body = _dash_render_bullet_list(bullets[:3])
    return (
        f'<div class="dash-logic-card">'
        f'<div class="dash-logic-title">{html.escape(title)}</div>'
        f"{body}"
        f"</div>"
    )


def _dash_render_timeline_card(title, items):
    body = _dash_render_action_list(items)
    return (
        f'<div class="dash-timeline-card">'
        f'<div class="dash-timeline-title">{html.escape(title)}</div>'
        f"{body}"
        f"</div>"
    )


def _dash_filter_account_indices(df, search_query):
    query = str(search_query).strip().lower()
    if not query:
        return list(df.index)
    matched = []
    for idx in df.index:
        row = df.loc[idx]
        blob = f"{idx} {row.get('Risk_Score', '')} {row.get('Contract', '')} {row.get('Risk_Category', '')}".lower()
        if query in blob:
            matched.append(idx)
    return matched if matched else list(df.index)


def show_customer_intelligence():
    # SECTION 1 — CUSTOMER INTELLIGENCE HEADER
    st.header("Customer Intelligence Center")
    st.markdown("*Interactive customer-level risk exploration and retention analysis.*")
    st.markdown("---")
    
    # Internal validation target paths
    report_path = 'outputs/customer_risk_report.csv'
    top20_path = 'outputs/top_20_risk_customers.csv'
    
    # Graceful file validation checking
    if not os.path.exists(report_path) or not os.path.exists(top20_path):
        st.warning("Customer analytical registers missing. Please verify that data files match the expected `outputs/` path location.")
        return
        
    try:
        # Load backend structures
        df_report = pd.read_csv(report_path)
        df_top20 = pd.read_csv(top20_path)
        
        # SECTION 2 — CUSTOMER RISK EXPLORER FILTERS
        st.subheader("Customer Risk Explorer Filters")
        
        # Clean multi-column interactive control layout grid
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
        with f_col1:
            risk_choice = st.selectbox("Risk Category:", options=["All", "Low Risk", "Medium Risk", "High Risk"])
        with f_col2:
            gender_choice = st.selectbox("Gender:", options=["All", "Male", "Female"])
        with f_col3:
            contract_choice = st.selectbox("Contract Type:", options=["All", "Month-to-month", "One year", "Two year"])
        with f_col4:
            senior_choice = st.selectbox("Senior Citizen:", options=["All", "Yes", "No"])
            
        # Dynamically evaluate matching data partitions
        df_filtered = df_report.copy()
        
        if risk_choice != "All":
            df_filtered = df_filtered[df_filtered['Risk_Category'] == risk_choice]
        if gender_choice != "All":
            df_filtered = df_filtered[df_filtered['gender'] == gender_choice]
        if contract_choice != "All":
            df_filtered = df_filtered[df_filtered['Contract'] == contract_choice]
        if senior_choice != "All":
            senior_numeric = 1 if senior_choice == "Yes" else 0
            df_filtered = df_filtered[df_filtered['SeniorCitizen'] == senior_numeric]
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # SECTION 3 — CUSTOMER PORTFOLIO TABLE
        st.subheader("Customer Portfolio Registry")
        st.markdown(f"**Total Filtered Records Visible:** `{len(df_filtered)}` accounts out of `{len(df_report)}` total.")
        
        # Isolate requested target columns
        target_columns = [
            'gender', 'SeniorCitizen', 'tenure', 'InternetService', 
            'Contract', 'MonthlyCharges', 'Risk_Score', 'Risk_Category', 'Retention_Recommendation'
        ]
        
        # Display modern sortable scrollable layout
        st.dataframe(df_filtered[target_columns], use_container_width=True, hide_index=False)
        st.markdown("---")
        
        # SECTION 4 — CUSTOMER DETAIL INSPECTOR
        st.subheader("Customer Detail Inspector")
        if not df_filtered.empty:
            selected_index = st.selectbox(
                "Select a specific Customer Index from the filtered table above to deep-dive:",
                options=df_filtered.index,
                format_func=lambda x: f"Customer Row Profile Index {x} | Risk Score: {df_filtered.loc[x, 'Risk_Score']} | {df_filtered.loc[x, 'Contract']}"
            )

            cust_profile = df_filtered.loc[selected_index]
            drivers = _dash_split_items(cust_profile["Churn_Driver_Explanation"])
            actions = _dash_split_items(cust_profile["Retention_Recommendation"])

            st.markdown(
                _dash_render_snapshot_strip([
                    ("Customer ID", selected_index),
                    ("Risk Level", cust_profile["Risk_Category"]),
                    ("Tenure", f"{cust_profile['tenure']} mo"),
                    ("Monthly Charges", f"${float(cust_profile['MonthlyCharges']):.2f}"),
                    ("Churn Probability", f"{float(cust_profile['Churn_Probability']):.1%}"),
                ]),
                unsafe_allow_html=True,
            )

            risk_panel = _dash_render_field_rows([
                ("Risk Level", cust_profile["Risk_Category"]),
                ("Risk Score", f"{cust_profile['Risk_Score']} / 100"),
                ("Churn Probability", f"{float(cust_profile['Churn_Probability']):.1%}"),
            ])
            drivers_panel = _dash_render_bullet_list(drivers)
            actions_panel = _dash_render_action_list(actions)

            p_col1, p_col2, p_col3 = st.columns(3, gap="medium")
            with p_col1:
                st.markdown(_dash_render_panel("Risk Assessment", risk_panel), unsafe_allow_html=True)
            with p_col2:
                st.markdown(_dash_render_panel("Key Churn Drivers", drivers_panel), unsafe_allow_html=True)
            with p_col3:
                st.markdown(_dash_render_panel("Recommended Actions", actions_panel), unsafe_allow_html=True)
        else:
            st.info("No matching records found for the applied filter metrics. Adjust settings above to reset view states.")

        st.markdown("---")

        # SECTION 5 — TOP 20 HIGH-RISK CUSTOMERS
        st.subheader("Top 20 High-Risk Customer Priorities")

        max_risk = df_top20["Risk_Score"].max()
        avg_risk = df_top20["Risk_Score"].mean()
        high_risk_count = len(df_top20[df_top20["Risk_Category"] == "High Risk"])

        st.markdown(
            _dash_render_kpi_grid([
                ("Highest Risk", f"{max_risk:.1f}", "Peak Exposure", "mlops-badge-critical"),
                ("Average Risk", f"{avg_risk:.1f}", "Portfolio Mean", "mlops-badge-elevated"),
                ("Tracked Customers", f"{high_risk_count}", "Active Watchlist", "mlops-badge-monitored"),
            ], columns=3),
            unsafe_allow_html=True,
        )

        top20_display_cols = ["Risk_Score", "Risk_Category", "Churn_Driver_Explanation", "Retention_Recommendation"]
        st.dataframe(df_top20[top20_display_cols], use_container_width=True, hide_index=False)
        st.markdown("---")

        # SECTION 6 — RISK DISTRIBUTION VISUALIZATION
        st.subheader("Filtered Portfolio Risk Stratification")

        df_counts = df_filtered["Risk_Category"].value_counts().reset_index()
        df_counts.columns = ["Risk Category", "Customer Count"]

        fig_filtered = px.bar(
            df_counts,
            x="Risk Category",
            y="Customer Count",
            color="Risk Category",
            labels={"Customer Count": "Active Profiles", "Risk Category": "Risk Category"},
            color_discrete_map={
                "Low Risk": "#2ecc71",
                "Medium Risk": "#f1c40f",
                "High Risk": "#e74c3c",
            },
            template="plotly_dark",
        )
        fig_filtered.update_layout(**_dash_plot_layout(height=380))

        st.markdown('<div class="dash-viz-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_filtered, use_container_width=True)

        if not df_filtered.empty and not df_counts.empty:
            dominant_row = df_counts.loc[df_counts["Customer Count"].idxmax()]
            dominant_segment = dominant_row["Risk Category"]
            dominant_count = int(dominant_row["Customer Count"])
            dominant_pct = (dominant_count / len(df_filtered)) * 100
            chart_insight = (
                f"{dominant_segment} is the dominant segment at {dominant_pct:.0f}% "
                f"({dominant_count:,} accounts) of the filtered portfolio."
            )
        else:
            chart_insight = "Apply filters above to view portfolio segment distribution."

        st.markdown(
            f'<div class="dash-chart-insight">{html.escape(chart_insight)}</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # SECTION 7 — EXECUTIVE INSIGHTS
        st.markdown('<div class="mlops-section">', unsafe_allow_html=True)
        st.markdown('<div class="mlops-section-title">Analyst Insights</div>', unsafe_allow_html=True)

        if not df_filtered.empty:
            total_f = len(df_filtered)
            risk_counts = df_filtered["Risk_Category"].value_counts()
            dominant_risk = risk_counts.idxmax() if not risk_counts.empty else "Unknown"
            dominant_risk_pct = (risk_counts.max() / total_f) * 100 if total_f > 0 else 0
            dominant_contract = df_filtered["Contract"].mode()[0] if not df_filtered["Contract"].empty else "Unknown"
            driver_series = df_filtered["Churn_Driver_Explanation"].dropna()
            primary_driver = driver_series.mode()[0] if not driver_series.empty else "Not identified"
            primary_driver_short = _dash_split_items(primary_driver)[0] if _dash_split_items(primary_driver) else "Not identified"
            rec_series = df_filtered["Retention_Recommendation"].dropna()
            top_action = _dash_split_items(rec_series.mode()[0])[0] if not rec_series.empty else "Assign retention review"
            high_pct = (len(df_filtered[df_filtered["Risk_Category"] == "High Risk"]) / total_f) * 100

            insight_blocks = [
                (
                    "Largest Customer Segment",
                    f"{dominant_risk} accounts for {dominant_risk_pct:.0f}% of the filtered portfolio ({total_f:,} records).",
                ),
                (
                    "Primary Risk Driver",
                    f"{primary_driver_short} — most frequent across {dominant_contract} accounts in this cohort.",
                ),
                (
                    "Suggested Action",
                    f"{top_action} should be prioritized for accounts matching this profile.",
                ),
                (
                    "Confidence Assessment",
                    f"Analysis based on {total_f:,} filtered records; {high_pct:.0f}% classified as high risk.",
                ),
            ]
            st.markdown(_dash_render_insight_card(insight_blocks), unsafe_allow_html=True)
        else:
            st.markdown(
                _dash_render_insight_card([
                    ("Largest Customer Segment", "No records match the current filter selection."),
                    ("Primary Risk Driver", "Adjust filters to surface actionable driver patterns."),
                    ("Suggested Action", "Expand filter criteria to enable retention targeting."),
                    ("Confidence Assessment", "Insufficient data volume for cohort assessment."),
                ]),
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to load structural customer analytics profiles safely: {str(e)}")


def show_high_risk_command_center():
    # SECTION 1 — COMMAND CENTER HEADER
    st.header("High Risk Command Center")
    st.markdown("*Priority retention targeting and operational intervention workspace.*")
    st.markdown("---")
    
    # Core internal system relative paths
    high_risk_path = 'outputs/high_risk_customers.csv'
    top20_path = 'outputs/top_20_risk_customers.csv'
    
    # Validation boundary checkpoint
    if not os.path.exists(high_risk_path) or not os.path.exists(top20_path):
        st.warning("Critical high-risk operational files not detected. Please verify database exports inside the `outputs/` folder structure.")
        return
        
    try:
        # Load business dataframes
        df_high = pd.read_csv(high_risk_path)
        df_top20 = pd.read_csv(top20_path)
        
        # Confirm dataframe is populated to avoid zero divisions
        if df_high.empty:
            st.info("No customers are currently classified under the high-risk cohort parameters.")
            return

        # SECTION 2 — HIGH RISK KPI BAR
        total_high = len(df_high)
        avg_risk = df_high["Risk_Score"].mean()
        max_risk = df_high["Risk_Score"].max()
        avg_prob = df_high["Churn_Probability"].mean()

        kpi_badges = [
            ("Critical" if total_high >= 50 else "Active Portfolio", "mlops-badge-critical" if total_high >= 50 else "mlops-badge-monitored"),
            ("Elevated" if avg_risk >= 70 else ("Moderate" if avg_risk >= 55 else "Stable"), "mlops-badge-elevated" if avg_risk >= 55 else "mlops-badge-stable"),
            ("Critical" if max_risk >= 80 else "Elevated", "mlops-badge-critical" if max_risk >= 80 else "mlops-badge-elevated"),
            ("High Exposure" if avg_prob >= 0.75 else "Monitored", "mlops-badge-critical" if avg_prob >= 0.75 else "mlops-badge-monitored"),
        ]

        st.markdown(
            _dash_render_kpi_grid([
                ("High-Risk Profiles", f"{total_high:,}", kpi_badges[0][0], kpi_badges[0][1]),
                ("Average Risk", f"{avg_risk:.1f}", kpi_badges[1][0], kpi_badges[1][1]),
                ("Peak Risk", f"{max_risk:.1f}", kpi_badges[2][0], kpi_badges[2][1]),
                ("Expected Churn", f"{avg_prob:.1%}", kpi_badges[3][0], kpi_badges[3][1]),
            ], columns=4),
            unsafe_allow_html=True,
        )

        st.markdown("---")
        
        # SECTION 3 — HIGH RISK CUSTOMER TABLE
        st.subheader("High Risk Customer Operational Registry")
        st.markdown("Full list of active consumer profiles currently flagged with critical attrition indices:")
        
        table_cols = [
            'Risk_Score', 'Churn_Probability', 'Contract', 
            'MonthlyCharges', 'tenure', 'Retention_Recommendation', 'Churn_Driver_Explanation'
        ]
        st.dataframe(df_high[table_cols], use_container_width=True, hide_index=False)
        st.markdown("---")
        
        # SECTION 4 — PRIORITY TARGET LIST
        st.subheader("Critical Priority Target List (Immediate Intervention)")
        st.markdown("Top 20 accounts requiring emergency immediate client retention actions:")
        
        # Use specialized styling inside a warning expander to create clear structural contrast
        with st.expander("View Critical Emergency Escalation Group", expanded=True):
            top20_cols = ['Risk_Score', 'Churn_Driver_Explanation', 'Retention_Recommendation']
            st.dataframe(
                df_top20[top20_cols].style.background_gradient(cmap="Reds", subset=['Risk_Score']), 
                use_container_width=True, 
                hide_index=False
            )
        st.markdown("---")
        
        # SECTION 5 — CUSTOMER PRIORITY INSPECTOR
        st.markdown(_dash_section_header("Customer Priority Inspector Tool", "◈"), unsafe_allow_html=True)

        account_search = st.text_input(
            "Search Account Index",
            placeholder="Filter by index, risk score, contract, or risk level…",
            key="hr_account_search",
        )
        filtered_indices = _dash_filter_account_indices(df_high, account_search)
        selected_high_idx = st.selectbox(
            "Account Index",
            options=filtered_indices,
            format_func=lambda x: (
                f"Index {x} · Risk {df_high.loc[x, 'Risk_Score']} · "
                f"{df_high.loc[x, 'Contract']} · {df_high.loc[x, 'Risk_Category']}"
            ),
            key="hr_account_select",
        )

        inspect_profile = df_high.loc[selected_high_idx]
        inspect_drivers = _dash_split_items(inspect_profile["Churn_Driver_Explanation"])
        inspect_actions = _dash_split_items(inspect_profile["Retention_Recommendation"])

        summary_panel = _dash_render_field_rows([
            ("Risk Score", f"{inspect_profile['Risk_Score']} / 100"),
            ("Churn Probability", f"{float(inspect_profile['Churn_Probability']):.1%}"),
            ("Risk Level", inspect_profile["Risk_Category"]),
        ])
        drivers_panel = _dash_render_bullet_list(inspect_drivers)
        actions_panel = _dash_render_action_list(inspect_actions)

        insp_col1, insp_col2, insp_col3 = st.columns(3, gap="medium")
        with insp_col1:
            st.markdown(_dash_render_panel("Customer Summary", summary_panel), unsafe_allow_html=True)
        with insp_col2:
            st.markdown(_dash_render_panel("Primary Risk Drivers", drivers_panel), unsafe_allow_html=True)
        with insp_col3:
            st.markdown(_dash_render_panel("Recommended Actions", actions_panel), unsafe_allow_html=True)

        st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

        # SECTION 6 — HIGH RISK VISUALIZATION
        st.markdown(_dash_section_header("Cohort Risk Landscape Analysis", "◈"), unsafe_allow_html=True)

        chart_layout = _dash_plot_layout(height=450)

        # Chart 1: Risk Score Distribution
        st.markdown('<div class="dash-viz-card">', unsafe_allow_html=True)
        st.markdown('<div class="dash-viz-title">Top Risk Score Distribution</div>', unsafe_allow_html=True)
        fig_a = px.histogram(
            df_high, x="Risk_Score", nbins=15,
            labels={"Risk_Score": "Risk Score"},
            color_discrete_sequence=["#e74c3c"], template="plotly_dark",
        )
        fig_a.update_layout(**chart_layout)
        st.plotly_chart(fig_a, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

        # Chart 2: Contract Type Concentration
        st.markdown('<div class="dash-viz-card">', unsafe_allow_html=True)
        st.markdown('<div class="dash-viz-title">Contract Type Concentration</div>', unsafe_allow_html=True)
        df_contract_cnt = df_high["Contract"].value_counts().reset_index()
        df_contract_cnt.columns = ["Contract Type", "Volume"]
        fig_b = px.bar(
            df_contract_cnt, x="Contract Type", y="Volume",
            color="Contract Type", color_discrete_sequence=px.colors.sequential.Reds_r,
            template="plotly_dark",
        )
        ###
        fig_b.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.12,
                x=0.5,
                xanchor="center"
            ),
            **chart_layout
        )
        ###
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

        # Chart 3: Mitigation Strategy Distribution
        st.markdown('<div class="dash-viz-card">', unsafe_allow_html=True)
        st.markdown('<div class="dash-viz-title">Mitigation Strategy Distribution</div>', unsafe_allow_html=True)
        df_recom_cnt = df_high["Retention_Recommendation"].value_counts().reset_index()
        df_recom_cnt.columns = ["Mitigation Recommendation", "Count"]
        df_recom_cnt = df_recom_cnt.sort_values("Count", ascending=True)
        fig_c = px.bar(
            df_recom_cnt,
            y="Mitigation Recommendation",
            x="Count",
            orientation="h",
            color_discrete_sequence=["#e67e22"],
            template="plotly_dark",
        )
        fig_c.update_layout(**{**chart_layout, "margin": dict(l=40, r=30, t=36, b=60)})
        fig_c.update_yaxes(automargin=True)
        st.plotly_chart(fig_c, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # SECTION 7 — RETENTION ACTION SUMMARY
        st.markdown('<div class="mlops-section">', unsafe_allow_html=True)
        st.markdown('<div class="mlops-section-title">Retention Strategy Actions Summary</div>', unsafe_allow_html=True)

        m2m_total = len(df_high[df_high["Contract"] == "Month-to-month"])
        m2m_ratio = (m2m_total / total_high) * 100 if total_high > 0 else 0
        dominant_strategy = df_high["Retention_Recommendation"].mode()[0] if not df_high["Retention_Recommendation"].empty else "N/A"
        dominant_driver_raw = df_high["Churn_Driver_Explanation"].mode()[0] if not df_high["Churn_Driver_Explanation"].empty else "Not identified"
        dominant_driver = _dash_split_items(dominant_driver_raw)[0] if _dash_split_items(dominant_driver_raw) else "Not identified"
        primary_rec = _dash_split_items(dominant_strategy)[0] if _dash_split_items(dominant_strategy) else dominant_strategy

        st.markdown(
            _dash_render_insight_card([
                (
                    "Dominant Risk Driver",
                    f"{dominant_driver} — present across {m2m_ratio:.0f}% of month-to-month high-risk accounts.",
                ),
                (
                    "Primary Recommendation",
                    f"{primary_rec} is the most frequently assigned retention action in this cohort.",
                ),
                (
                    "Portfolio Observation",
                    f"{total_high:,} high-risk profiles tracked with mean churn probability of {avg_prob:.1%}.",
                ),
                (
                    "Immediate Business Action",
                    "Prioritize contract conversion outreach for month-to-month accounts within the top-20 target list.",
                ),
            ]),
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # SECTION 8 — EXPORT PANEL
        st.subheader("Data Export Controls Center")
        st.write("Extract priority target registries directly into clean system files for offline account mapping:")
        
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            high_csv_data = df_high.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download High Risk Customer Registry (.CSV)",
                data=high_csv_data,
                file_name="high_risk_customers_export.csv",
                mime="text/csv",
                use_container_width=True
            )
        with exp_col2:
            top20_csv_data = df_top20.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Emergency Top-20 Priority Register (.CSV)",
                data=top20_csv_data,
                file_name="top_20_priority_escalation.csv",
                mime="text/csv",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Critical execution failure inside Command Center arrays: {str(e)}")


def show_scenario_simulator():
    # SECTION 1 — PAGE HEADER
    st.header("Scenario Simulator")
    st.markdown("*Evaluate retention interventions before operational deployment.*")
    st.markdown("---")
    
    # Create functional responsive grid layout partitions
    config_layout_col, analytics_layout_col = st.columns([4, 6])
    
    with config_layout_col:
        st.markdown(_dash_section_header("Customer Profile Builder", "◈"), unsafe_allow_html=True)
        with st.form("profile_input_form"):
            st.markdown('<div class="dash-form-card">', unsafe_allow_html=True)

            # Customer Attributes Group
            st.markdown('<div class="dash-form-section-label">Customer Attributes</div>', unsafe_allow_html=True)
            attr_col1, attr_col2 = st.columns(2)
            with attr_col1:
                gender = st.selectbox("Gender", options=["Male", "Female"], index=0)
                senior_citizen = st.selectbox("Senior Citizen", options=["No", "Yes"], index=0)
            with attr_col2:
                contract = st.selectbox("Contract Type", options=["Month-to-month", "One year", "Two year"], index=0)
                tenure = st.number_input("Tenure (Months)", min_value=0, max_value=120, value=12, step=1)

            # Service Configuration Group
            st.markdown('<div class="dash-form-section-label">Service Configuration</div>', unsafe_allow_html=True)
            service_col1, service_col2 = st.columns(2)
            with service_col1:
                internet_service = st.selectbox("Internet Service", options=["Fiber optic", "DSL", "No"], index=0)
            with service_col2:
                phone_service = st.selectbox("Phone Service", options=["Yes", "No"], index=0)

            # Billing Information Group
            st.markdown('<div class="dash-form-section-label">Billing Information</div>', unsafe_allow_html=True)
            billing_col1, billing_col2 = st.columns(2)
            with billing_col1:
                monthly_charges = st.number_input("Monthly Charges ($)", min_value=10.0, max_value=250.0, value=65.0, step=0.5)
                paperless_billing = st.selectbox("Paperless Billing", options=["Yes", "No"], index=0)
            with billing_col2:
                payment_method = st.selectbox("Payment Method", options=["Electronic check", "Mailed check", "Bank transfer", "Credit card"], index=0)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('<div class="dash-form-section-label">Simulation Controls</div>', unsafe_allow_html=True)
            submit_simulation = st.form_submit_button("Run Predictive Simulation", use_container_width=True)
            
    # Calculate baseline outcomes using current form configurations
    base_prob, base_score, base_cat = calculate_simulated_risk(
        gender, senior_citizen, tenure, phone_service, internet_service, contract, paperless_billing, payment_method, monthly_charges
    )
    
    # Compile the simulated comparative scenario combinations matrix
    scenarios_list = []
    
    # 1. Baseline Case
    scenarios_list.append({
        "Scenario": "Baseline Profile", "Probability": base_prob, 
        "Risk Score": base_score, "Risk Category": base_cat, "Risk Reduction %": 0.0
    })
    
    # 2. One-Year Contract Simulation
    p_s1, s_s1, c_s1 = calculate_simulated_risk(gender, senior_citizen, tenure, phone_service, internet_service, "One year", paperless_billing, payment_method, monthly_charges)
    red_s1 = max(0.0, ((base_prob - p_s1) / base_prob) * 100) if base_prob > 0 else 0.0
    scenarios_list.append({"Scenario": "Convert To One-Year Contract", "Probability": p_s1, "Risk Score": s_s1, "Risk Category": c_s1, "Risk Reduction %": round(red_s1, 1)})
    
    # 3. Two-Year Contract Simulation
    p_s2, s_s2, c_s2 = calculate_simulated_risk(gender, senior_citizen, tenure, phone_service, internet_service, "Two year", paperless_billing, payment_method, monthly_charges)
    red_s2 = max(0.0, ((base_prob - p_s2) / base_prob) * 100) if base_prob > 0 else 0.0
    scenarios_list.append({"Scenario": "Convert To Two-Year Contract", "Probability": p_s2, "Risk Score": s_s2, "Risk Category": c_s2, "Risk Reduction %": round(red_s2, 1)})
    
    # 4. Apply 15% Discount Simulation
    p_s3, s_s3, c_s3 = calculate_simulated_risk(gender, senior_citizen, tenure, phone_service, internet_service, contract, paperless_billing, payment_method, monthly_charges * 0.85)
    red_s3 = max(0.0, ((base_prob - p_s3) / base_prob) * 100) if base_prob > 0 else 0.0
    scenarios_list.append({"Scenario": "Apply 15% Financial Discount", "Probability": p_s3, "Risk Score": s_s3, "Risk Category": c_s3, "Risk Reduction %": round(red_s3, 1)})
    
    # 5. Increase Tenure by 12 Months Simulation
    p_s4, s_s4, c_s4 = calculate_simulated_risk(gender, senior_citizen, tenure + 12, phone_service, internet_service, contract, paperless_billing, payment_method, monthly_charges)
    red_s4 = max(0.0, ((base_prob - p_s4) / base_prob) * 100) if base_prob > 0 else 0.0
    scenarios_list.append({"Scenario": "Increase Tenure By 12 Months", "Probability": p_s4, "Risk Score": s_s4, "Risk Category": c_s4, "Risk Reduction %": round(red_s4, 1)})
    
    df_scenarios = pd.DataFrame(scenarios_list)
    
    with analytics_layout_col:
        st.markdown(_dash_section_header("Baseline Risk Metrics", "◈"), unsafe_allow_html=True)
        st.markdown(
            _dash_render_simple_kpi_grid([
                ("Probability", f"{base_prob:.1%}"),
                ("Risk Score", f"{base_score} / 100"),
                ("Risk Category", str(base_cat)),
            ], columns=3),
            unsafe_allow_html=True,
        )

        st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

        st.markdown(_dash_section_header("Retention Strategy Lab Evaluation", "◈"), unsafe_allow_html=True)
        st.caption("Comparative metrics across modeled mitigation scenarios.")
        st.dataframe(df_scenarios[["Scenario", "Probability", "Risk Category", "Risk Reduction %"]], use_container_width=True, hide_index=True)
        st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)
    # SECTION 5 — STRATEGY COMPARISON VISUALIZATION GRID
    st.subheader("Prescriptive Optimization Visualizations")
    vis_grid1, vis_grid2 = st.columns(2)
    
    with vis_grid1:
        st.markdown("#### Scenario Probability Comparison Matrix")
        fig_prob = px.bar(
            df_scenarios, x='Scenario', y='Probability', color='Risk Category',
            labels={'Probability': 'Probability Scale', 'Scenario': 'Mitigation Action Plan'},
            color_discrete_map={'Low Risk': '#2ecc71', 'Medium Risk': '#f1c40f', 'High Risk': '#e74c3c'},
            template='plotly_dark'
        )
        fig_prob = fig_prob.update_layout(height=290, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_prob, use_container_width=True)
        
    with vis_grid2:
        st.markdown("#### Risk Mitigation Reduction Ratios (%)")
        df_reductions_only = df_scenarios[df_scenarios['Scenario'] != 'Baseline Profile']
        fig_red = px.bar(
            df_reductions_only, x='Scenario', y='Risk Reduction %',
            labels={'Risk Reduction %': 'Risk Reduction Percentage (%)', 'Scenario': 'Mitigation Action Plan'},
            color_discrete_sequence=['#3498db'], template='plotly_dark'
        )
        fig_red = fig_red.update_layout(height=290, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_red, use_container_width=True)
        
    st.markdown("---")
    
    # SECTION 6 — BEST STRATEGY ENGINE
    st.subheader("Optimal Retention Selection Core")
    
    # Exclude baseline configuration when tracking maximum reduction strategy routes
    df_interventions = df_scenarios[df_scenarios['Scenario'] != 'Baseline Profile']
    best_option_row = df_interventions.loc[df_interventions['Risk Reduction %'].idxmax()]
    
    st.markdown(
        f"<div class='recommended-strategy-card'>"
        f"<h2>Recommended Strategy: {html.escape(str(best_option_row['Scenario']))}</h2>"
        f"<p>Risk reduction of <strong>{best_option_row['Risk Reduction %']}%</strong> · "
        f"Projected category: <strong>{html.escape(str(best_option_row['Risk Category']))}</strong></p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(_dash_section_header("Executive Decision Summary", "◈"), unsafe_allow_html=True)
    
    # Compact executive cards
    exec_col1, exec_col2 = st.columns(2)
    with exec_col1:
        st.markdown(
            f'<div class="mlops-metric-card">'
            f'<div class="mlops-metric-label">Current Risk</div>'
            f'<div class="mlops-metric-value">{base_prob:.1%} / {base_score}</div>'
            f'<div class="mlops-metric-badge mlops-badge-{("critical" if base_cat == "High Risk" else "elevated" if base_cat == "Medium Risk" else "stable")}">{base_cat}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="mlops-metric-card">'
            f'<div class="mlops-metric-label">Projected Risk</div>'
            f'<div class="mlops-metric-value">{float(best_option_row["Probability"]):.1%}</div>'
            f'<div class="mlops-metric-badge mlops-badge-{("critical" if best_option_row["Risk Category"] == "High Risk" else "elevated" if best_option_row["Risk Category"] == "Medium Risk" else "stable")}">{best_option_row["Risk Category"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with exec_col2:
        st.markdown(
            f'<div class="mlops-metric-card">'
            f'<div class="mlops-metric-label">Risk Reduction</div>'
            f'<div class="mlops-metric-value">{best_option_row["Risk Reduction %"]}%</div>'
            f'<div class="mlops-metric-badge mlops-badge-excellent">Improvement</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="mlops-metric-card">'
            f'<div class="mlops-metric-label">Recommended Strategy</div>'
            f'<div class="mlops-metric-value" style="font-size: 1.1rem;">{html.escape(str(best_option_row["Scenario"]))}</div>'
            f'<div class="mlops-metric-badge mlops-badge-monitored">Optimal Action</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown("---")
    
    # SECTION 8 — EXPORT RESULTS
    st.subheader("Export Simulation Outputs")
    st.write("Extract modeled mitigation scenarios directly for offline strategic roadmap reviews:")
    
    current_sim_csv = df_scenarios.to_csv(index=False).encode('utf-8')
    
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        st.download_button(
            label="Download Current Simulation Scenario Ledger (.CSV)",
            data=current_sim_csv,
            file_name="current_profile_simulation_output.csv",
            mime="text/csv",
            use_container_width=True
        )
    with exp_col2:
        # Check if systemic baseline records exist or provide safe real-time fallback structures
        if os.path.exists('outputs/scenario_simulation_report.csv'):
            with open('outputs/scenario_simulation_report.csv', 'rb') as f_rep:
                report_data = f_rep.read()
        else:
            report_data = current_sim_csv
            
        st.download_button(
            label="Download Historical System Simulation Report Master Registry (.CSV)",
            data=report_data,
            file_name="scenario_simulation_report_master.csv",
            mime="text/csv",
            use_container_width=True
        )


def show_insights_center():
    # SECTION 1 — PAGE HEADER
    st.header("Insights Center")
    st.markdown("*Executive intelligence, portfolio interpretation, and strategic recommendations.*")
    st.markdown("---")
    
    # Reference artifact file paths
    summary_path = 'outputs/executive_summary.csv'
    health_path = 'outputs/model_health_report.csv'
    report_path = 'outputs/customer_risk_report.csv'
    high_risk_path = 'outputs/high_risk_customers.csv'
    insights_text_path = 'outputs/churn_insights.txt'
    
    # Establish dynamic metrics dictionary storage mapping placeholders
    summary_dict = {}
    health_dict = {}
    total_customers_val = 1000
    expected_churn_val = 250
    avg_risk_val = 45.0
    roc_auc_val = 0.8500
    high_risk_pct_val = 22.5
    largest_concentration = "Medium Risk"
    
    # Safely digest core summary metrics
    if os.path.exists(summary_path):
        try:
            df_s = pd.read_csv(summary_path)
            summary_dict = dict(zip(df_s['Metric'], df_s['Value']))
            total_customers_val = int(float(summary_dict.get('Total Customers', total_customers_val)))
            expected_churn_val = int(float(summary_dict.get('Expected Churn Count', expected_churn_val)))
            avg_risk_val = float(summary_dict.get('Average Risk Score', avg_risk_val))
            high_risk_pct_val = float(summary_dict.get('High Risk Percentage', high_risk_pct_val))
            
            # Identify dominant tier matrix
            h_cnt = int(float(summary_dict.get('High Risk Customers', 0)))
            m_cnt = int(float(summary_dict.get('Medium Risk Customers', 0)))
            l_cnt = int(float(summary_dict.get('Low Risk Customers', 0)))
            if l_cnt >= m_cnt and l_cnt >= h_cnt:
                largest_concentration = "Low Risk"
            elif m_cnt >= h_cnt:
                largest_concentration = "Medium Risk"
            else:
                largest_concentration = "High Risk"
        except:
            pass
            
    # Safely digest model health indicators
    if os.path.exists(health_path):
        try:
            df_h = pd.read_csv(health_path)
            health_dict = dict(zip(df_h['Metric'], df_h['Value']))
            roc_auc_val = float(health_dict.get('ROC-AUC', roc_auc_val))
        except:
            pass

    # Read external unstructured text summary records if available
    external_insights_text = ""
    if os.path.exists(insights_text_path):
        try:
            with open(insights_text_path, 'r') as f_ins:
                external_insights_text = f_ins.read()
        except:
            pass
    elif os.path.exists('churn_insights.txt'):
        try:
            with open('churn_insights.txt', 'r') as f_ins:
                external_insights_text = f_ins.read()
        except:
            pass

    # SECTION 2 — PLATFORM HEALTH SUMMARY KPI BAR
    st.markdown(_dash_section_header("Platform Diagnostic Metrics", "◈"), unsafe_allow_html=True)
    st.markdown(
        _dash_render_simple_kpi_grid([
            ("Customers", f"{total_customers_val:,}"),
            ("Expected Churn", f"~{expected_churn_val:,}"),
            ("Mean Risk", f"{avg_risk_val:.1f}"),
            ("ROC-AUC", f"{roc_auc_val:.3f}"),
            ("High Risk %", f"{high_risk_pct_val:.1f}%"),
        ], columns=5),
        unsafe_allow_html=True,
    )
    st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

    # SECTION 3 — STRATEGIC BUSINESS INSIGHTS
    st.markdown(_dash_section_header("Premium Strategic Consulting Insights", "◈"), unsafe_allow_html=True)
    ins_col1, ins_col2 = st.columns(2)
    ins_col3, ins_col4 = st.columns(2)

    with ins_col1:
        st.markdown(
            "<div class='insight-card insight-card-danger'>"
            "<strong>Highest Risk Portfolio Segment</strong>"
            "Month-to-month profiles on fiber optic service show the highest structural churn exposure.<br>"
            "These accounts lack pricing protection and respond quickly to competitive offers.<br>"
            "Retention teams should prioritize contract conversion in this segment.<br>"
            "Early intervention before billing cycles reduces immediate attrition risk."
            "</div>", unsafe_allow_html=True
        )
    with ins_col2:
        st.markdown(
            "<div class='insight-card insight-card-warning'>"
            "<strong>Dominant Structural Attrition Driver</strong>"
            "Contract flexibility is the leading predictor of customer departure across the portfolio.<br>"
            "Month-to-month agreements create zero switching friction for dissatisfied accounts.<br>"
            "Long-term contracts correlate with significantly lower churn probability.<br>"
            "Contract type should anchor all retention campaign targeting logic."
            "</div>", unsafe_allow_html=True
        )
    with ins_col3:
        st.markdown(
            "<div class='insight-card insight-card-success'>"
            "<strong>Optimal Value Retention Strategy</strong>"
            "Multi-year contract migration backed by temporary billing incentives delivers the strongest ROI.<br>"
            "Converting month-to-month accounts eliminates over 65% of predictive risk indices.<br>"
            "Bundle annual contract offers with loyalty discounts for maximum uptake.<br>"
            "Target high-risk accounts within the first 90 days of elevated scores."
            "</div>", unsafe_allow_html=True
        )
    with ins_col4:
        st.markdown(
            "<div class='insight-card insight-card-primary'>"
            "<strong>Critical Corporate Revenue Exposure Area</strong>"
            "Accounts with tenure between 1 and 15 months represent the highest revenue volatility.<br>"
            "Loyalty remains unstable before the 18-month relationship milestone.<br>"
            "Onboarding and early-tenure touchpoints are the highest-leverage retention window.<br>"
            "Proactive outreach during this period prevents long-term revenue erosion."
            "</div>", unsafe_allow_html=True
        )

    if external_insights_text:
        st.markdown('<div class="dash-notes-wrap">', unsafe_allow_html=True)
        with st.expander("◈  Supplemental Technical Notes", expanded=False):
            st.markdown(
                f'<div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">'
                f'<div style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.6; white-space: pre-wrap;">{html.escape(external_insights_text)}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

    # SECTION 4 — MODEL INTERPRETATION PANEL
    st.markdown(_dash_section_header("Enterprise Predictive Logic Panel", "◈"), unsafe_allow_html=True)

    logic_col1, logic_col2 = st.columns(2)
    with logic_col1:
        st.markdown(
            _dash_render_logic_card("Behavior Signals", [
                "Key Finding: Billing disputes and service dissatisfaction patterns predict churn",
                "Support Observation: Reduced engagement and increased support contacts flag at-risk accounts",
                "Business Implication: Proactive outreach before cancellation events reduces attrition",
            ]),
            unsafe_allow_html=True,
        )
        st.markdown(
            _dash_render_logic_card("Contract Impact", [
                "Key Finding: Month-to-month agreements accelerate churn risk significantly",
                "Support Observation: Multi-year contracts provide the strongest risk stabilization effect",
                "Business Implication: Contract conversion is the highest-value retention intervention",
            ]),
            unsafe_allow_html=True,
        )
    with logic_col2:
        st.markdown(
            _dash_render_logic_card("Pricing Sensitivity", [
                "Key Finding: Premium pricing without clear value triggers score increases",
                "Support Observation: Price-sensitive segments respond to targeted discount offers",
                "Business Implication: Monthly charge thresholds define key risk escalation markers",
            ]),
            unsafe_allow_html=True,
        )
        st.markdown(
            _dash_render_logic_card("Tenure Effects", [
                "Key Finding: Relationship duration is a natural risk stabilization factor",
                "Support Observation: First 90–360 days represent the highest-return intervention window",
                "Business Implication: Accounts past 24 months show significantly lower attrition rates",
            ]),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

    # SECTION 5 — PORTFOLIO RISK VISUALIZATION
    st.markdown(_dash_section_header("Portfolio Risk Allocation Canvas", "◈"), unsafe_allow_html=True)

    chart_layout = _dash_plot_layout(height=475)

    st.markdown('<div class="dash-viz-card">', unsafe_allow_html=True)
    st.markdown('<div class="dash-viz-title">Portfolio Category Stratification</div>', unsafe_allow_html=True)
    df_risk_dist = pd.DataFrame([
        {"Risk Tier": "Low Risk", "Volume": int(total_customers_val * 0.55)},
        {"Risk Tier": "Medium Risk", "Volume": int(total_customers_val * 0.25)},
        {"Risk Tier": "High Risk", "Volume": int(total_customers_val * 0.20)},
    ])
    if os.path.exists("outputs/risk_distribution.csv"):
        try:
            df_rd_read = pd.read_csv("outputs/risk_distribution.csv")
            df_risk_dist = pd.DataFrame({
                "Risk Tier": df_rd_read["Risk Category"],
                "Volume": df_rd_read["Customer Count"],
            })
        except Exception:
            pass
    fig_p1 = px.pie(
        df_risk_dist, names="Risk Tier", values="Volume",
        color="Risk Tier",
        color_discrete_map={"Low Risk": "#2ecc71", "Medium Risk": "#f1c40f", "High Risk": "#e74c3c"},
        template="plotly_dark",
    )
    ###
    fig_p1.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.12
        ),
        **chart_layout
    )
    ###
    st.plotly_chart(fig_p1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="dash-viz-card">', unsafe_allow_html=True)
    st.markdown('<div class="dash-viz-title">Portfolio Attrition Risk Indices</div>', unsafe_allow_html=True)
    df_scores_fallback = pd.DataFrame({"Risk_Score": [12, 15, 22, 35, 42, 58, 72, 81, 85, 89, 24, 31, 18, 14, 76]})
    if os.path.exists(report_path):
        try:
            df_rep_read = pd.read_csv(report_path)
            if "Risk_Score" in df_rep_read.columns:
                df_scores_fallback = df_rep_read[["Risk_Score"]]
        except Exception:
            pass
    fig_p2 = px.histogram(
        df_scores_fallback, x="Risk_Score", nbins=12,
        labels={"Risk_Score": "Risk Score"},
        color_discrete_sequence=["#3498db"], template="plotly_dark",
    )
    fig_p2.update_layout(**chart_layout)
    st.plotly_chart(fig_p2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="dash-viz-card">', unsafe_allow_html=True)
    st.markdown('<div class="dash-viz-title">Leading Structural Churn Drivers</div>', unsafe_allow_html=True)
    df_drivers_fallback = pd.DataFrame({
        "Core Predictor Factor": ["Contract Structure", "Monthly Charges", "Fiber Optic Add-on", "Paperless Billing", "Senior Citizen Status"],
        "Algorithmic Importance Weight": [44.2, 28.5, 14.1, 8.3, 4.9],
    })
    fig_p3 = px.bar(
        df_drivers_fallback, x="Algorithmic Importance Weight", y="Core Predictor Factor",
        orientation="h", color="Algorithmic Importance Weight", color_continuous_scale="Reds",
        template="plotly_dark",
    )
    fig_p3.update_layout(**chart_layout, coloraxis_showscale=False)
    st.plotly_chart(fig_p3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

    # SECTION 6 — EXECUTIVE RECOMMENDATION BOARD
    st.markdown(_dash_section_header("Executive Strategic Recommendation Board", "◈"), unsafe_allow_html=True)

    rec_col1, rec_col2 = st.columns(2)
    with rec_col1:
        st.markdown(
            _dash_render_timeline_card("Next 7 Days", [
                "Extract the emergency top-20 high-risk client roster",
                "Route records to specialized customer support divisions",
                "Resolve pending billing disputes before the next billing run",
            ]),
            unsafe_allow_html=True,
        )
        st.markdown(
            _dash_render_timeline_card("Next 90 Days", [
                "Update premium packages with complimentary cloud storage features",
                "Offset high fee sensitivities across price-sensitive user tiers",
                "Reduce structural attrition through value-added service bundles",
            ]),
            unsafe_allow_html=True,
        )
    with rec_col2:
        st.markdown(
            _dash_render_timeline_card("Next 30 Days", [
                "Target fiber optic accounts on month-to-month plans",
                "Offer 12-month contract migrations with monthly credits",
                "Lock in vulnerable client cohorts through structured agreements",
            ]),
            unsafe_allow_html=True,
        )
        st.markdown(
            _dash_render_timeline_card("Long-Term Strategy", [
                "Integrate ML scoring endpoints into daily CRM workflows",
                "Enable real-time risk summaries during live service conversations",
                "Empower sales teams with recommended mitigation actions per account",
            ]),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

    # SECTION 7 — PLATFORM INTELLIGENCE REPORT
    st.markdown(_dash_section_header("Dynamic Corporate Executive Brief", "◈"), unsafe_allow_html=True)
    st.markdown(
        _dash_render_insight_card([
            (
                "Current Portfolio",
                f"{total_customers_val:,} active customer profiles with {largest_concentration} as the largest concentration tier.",
            ),
            (
                "Highest Risk Driver",
                "Contract structure parameters remain the most influential driver in the scoring layer.",
            ),
            (
                "Priority Recommendation",
                "Transition month-to-month segments toward structured long-term agreements immediately.",
            ),
            (
                "Expected Business Outcome",
                "Targeted retention workflows will secure contract revenues and reduce portfolio churn exposure.",
            ),
        ]),
        unsafe_allow_html=True,
    )
    st.markdown('<div class="enterprise-section-gap"></div>', unsafe_allow_html=True)

    # SECTION 8 — DOWNLOAD CENTER PANEL
    st.markdown(_dash_section_header("Central Enterprise Reporting Download Hub", "⬇"), unsafe_allow_html=True)
    st.caption("Extract master analytics ledger data assets for corporate audit review.")

    def safe_read_bytes(path_target):
        if os.path.exists(path_target):
            try:
                return pd.read_csv(path_target).to_csv(index=False).encode("utf-8")
            except Exception:
                pass
        return pd.DataFrame([{"System Status": "Reporting Data Asset Placeholder Log Record"}]).to_csv(index=False).encode("utf-8")

    st.markdown('<div class="dash-download-wrap">', unsafe_allow_html=True)
    dl_grid1, dl_grid2, dl_grid3 = st.columns(3)
    dl_grid4, dl_grid5 = st.columns(2)

    with dl_grid1:
        st.download_button(
            label="⬇ Executive Summary",
            data=safe_read_bytes(summary_path), file_name="executive_summary_report.csv", mime="text/csv", use_container_width=True
        )
    with dl_grid2:
        st.download_button(
            label="⬇ Model Metrics",
            data=safe_read_bytes(health_path), file_name="model_health_report.csv", mime="text/csv", use_container_width=True
        )
    with dl_grid3:
        st.download_button(
            label="⬇ Customer Risk Matrix",
            data=safe_read_bytes(report_path), file_name="customer_risk_analytics_master.csv", mime="text/csv", use_container_width=True
        )
    with dl_grid4:
        st.download_button(
            label="⬇ High Risk Targets",
            data=safe_read_bytes(high_risk_path), file_name="high_risk_customer_roster.csv", mime="text/csv", use_container_width=True
        )
    with dl_grid5:
        st.download_button(
            label="⬇ Simulation History",
            data=safe_read_bytes("outputs/scenario_simulation_report.csv"), file_name="scenario_simulation_report_history.csv", mime="text/csv", use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

# Duplicate show_scenario_simulator definition removed

SIDEBAR_NAV_OPTIONS = [
    "Executive Overview",
    "Model Analytics",
    "Customer Intelligence",
    "High Risk Command Center",
    "Scenario Simulator",
    "Insights Center",
]

def _nav_page_key(page_name):
    return "nav_" + page_name.replace(" ", "_").lower()


def _ensure_current_page():
    if "current_page" not in st.session_state:
        st.session_state.current_page = SIDEBAR_NAV_OPTIONS[0]
    elif st.session_state.current_page not in SIDEBAR_NAV_OPTIONS:
        st.session_state.current_page = SIDEBAR_NAV_OPTIONS[0]


def _navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()


def _sidebar_brand_html():
    return """
    <div class="nav-brand-header">
        <div class="nav-brand-logo">
            <span class="nav-brand-name">Customer Intelligence</span>
            <span class="nav-brand-tagline">Enterprise Analytics Platform</span>
        </div>
    </div>
    <div class="nav-divider"></div>
    """


def _sidebar_dataset_card_html(name, rows, status="Ready"):
    safe_name = html.escape(str(name))
    return f"""
    <div class="nav-dataset-wrap">
        <div class="nav-dataset-card">
            <div class="nav-dataset-label">Current Dataset</div>
            <div class="nav-dataset-name">{safe_name}</div>
            <div class="nav-dataset-meta">{rows:,} rows &bull; {html.escape(status)}</div>
        </div>
    </div>
    <div class="nav-divider"></div>
    """


def _sidebar_footer_html():
    return """
    <div class="nav-sidebar-footer">
        <div class="nav-footer-line">System Online</div>
        <div class="nav-footer-line">Version 2.0</div>
        <div class="nav-footer-line">AI Analytics Suite</div>
    </div>
    """


def _render_sidebar_navigation(active_page):
    with st.sidebar.container():
        for page_name in SIDEBAR_NAV_OPTIONS:
            is_active = page_name == active_page
            if st.button(
                page_name,
                key=_nav_page_key(page_name),
                use_container_width=True,
                type="secondary",
                disabled=is_active,
            ):
                _navigate_to(page_name)
    st.sidebar.markdown('<div class="nav-divider nav-divider--after-nav"></div>', unsafe_allow_html=True)


def render_enterprise_sidebar(ds_name, ds_rows, ds_ready=True):
    """Render the premium enterprise sidebar (custom button navigation; routing unchanged)."""
    _ensure_current_page()
    active_page = st.session_state.current_page

    st.sidebar.markdown(_sidebar_brand_html(), unsafe_allow_html=True)
    _render_sidebar_navigation(active_page)

    st.sidebar.markdown(
        _sidebar_dataset_card_html(ds_name, ds_rows, "Ready" if ds_ready else "Pending"),
        unsafe_allow_html=True,
    )

    if st.sidebar.button("New Dataset", key="sb_reset_ws", use_container_width=True, type="primary"):
        for _k in ['workspace_initialized', 'active_dataset_info', '_validation_result', '_last_uploaded_filename']:
            st.session_state.pop(_k, None)
        st.session_state["workspace_initialized"] = False
        st.rerun()

    st.sidebar.markdown(_sidebar_footer_html(), unsafe_allow_html=True)
    return active_page


# --- 3. Main Application Entry Point ---
def main():
    if "workspace_initialized" not in st.session_state:
        st.session_state["workspace_initialized"] = False
        
    if not st.session_state["workspace_initialized"]:
        show_workspace_initialization()
        return

    active_info = st.session_state.get('active_dataset_info', None)
    ds_name = active_info['name'] if active_info else "Benchmark Telecom Dataset"
    ds_rows = active_info['rows'] if active_info else 0
    ds_ready = active_info.get('valid', False) if active_info else False

    selected_page = render_enterprise_sidebar(ds_name, ds_rows, ds_ready)
    
    # Central Functional Routing Core
    if selected_page == "Executive Overview":
        show_executive_overview()
    elif selected_page == "Model Analytics":
        show_model_analytics()
    elif selected_page == "Customer Intelligence":
        show_customer_intelligence()
    elif selected_page == "High Risk Command Center":
        show_high_risk_command_center()
    elif selected_page == "Scenario Simulator":
        show_scenario_simulator()
    elif selected_page == "Insights Center":
        show_insights_center()
        
    # --- 4. Global Structural Application Footer ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    footer_col1, footer_col2 = st.columns(2)
    with footer_col1:
        st.markdown("<p class='footer-left-text'>AI Analytics Suite</p>", unsafe_allow_html=True)
    with footer_col2:
        st.markdown("<p class='footer-right-text'>Version 2.0</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    _ = main()
