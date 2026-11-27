# ============================================================
# SMART EXPENSE SPLITTER - Version 3.8 (Sandbox-Proof Full-Viewport Live Stage)
# Pairs directly with logic.py. Zero extra pip installs.
# Run with:  python -m streamlit run app_v2.py
# ============================================================
import base64
import hashlib
import hmac
import html
import io
import os
from datetime import date
from urllib.parse import quote

import pandas as pd
import streamlit as st

import logic as lg

st.set_page_config(page_title="Smart Expense Splitter", page_icon="💸", layout="wide")

# ------------------------------------------------------------
# FULL-VIEWPORT GPU ANIMATED AURORA + LIQUID ORB CSS (No Iframe Sandbox!)
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    --spring: cubic-bezier(0.16, 1, 0.3, 1);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

html, body {
    background: #050311 !important;
    color: #f8fafc;
}

@keyframes orbFloatOne {
    0%   { transform: translate3d(-8vw, -6vh, 0) scale(1) rotate(0deg); }
    33%  { transform: translate3d(14vw, 8vh, 0) scale(1.18) rotate(120deg); }
    66%  { transform: translate3d(-4vw, 18vh, 0) scale(0.92) rotate(240deg); }
    100% { transform: translate3d(-8vw, -6vh, 0) scale(1) rotate(360deg); }
}

@keyframes orbFloatTwo {
    0%   { transform: translate3d(10vw, 12vh, 0) scale(1.05) rotate(0deg); }
    50%  { transform: translate3d(-16vw, -10vh, 0) scale(1.22) rotate(-180deg); }
    100% { transform: translate3d(10vw, 12vh, 0) scale(1.05) rotate(-360deg); }
}

@keyframes orbFloatThree {
    0%   { transform: translate3d(0vw, 15vh, 0) scale(0.95); }
    50%  { transform: translate3d(12vw, -14vh, 0) scale(1.15); }
    100% { transform: translate3d(0vw, 15vh, 0) scale(0.95); }
}

@keyframes gridPan {
    0%   { background-position: 0px 0px, 0px 0px; }
    100% { background-position: 48px 48px, 48px 48px; }
}

@keyframes cardFloatIn {
    0%   { opacity: 0; transform: translateY(16px) scale(0.985); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes pulseDot {
    0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.85); }
    65%      { box-shadow: 0 0 0 7px rgba(16, 185, 129, 0); }
}

@keyframes borderShimmer {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Deep Obsidian Base */
.stApp {
    background: #050311 !important;
    color: #f8fafc;
    overflow-x: hidden;
}

/* Full-screen live animated background stage (injected directly into DOM) */
.live-stage-bg {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
    background: radial-gradient(ellipse at 50% 0%, #160d35 0%, #050311 72%);
}

/* Animated perspective tech grid */
.live-grid {
    position: absolute;
    inset: -48px;
    background-image:
        linear-gradient(rgba(167, 139, 250, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.08) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(circle at 50% 45%, rgba(0,0,0,0.9) 15%, transparent 78%);
    -webkit-mask-image: radial-gradient(circle at 50% 45%, rgba(0,0,0,0.9) 15%, transparent 78%);
    animation: gridPan 14s linear infinite;
}

/* 3 GPU-accelerated glowing volumetric plasma blobs */
.plasma-orb {
    position: absolute;
    border-radius: 42% 58% 63% 37% / 45% 38% 62% 55%;
    filter: blur(68px);
    will-change: transform;
}
.orb-1 {
    width: 520px;
    height: 520px;
    top: 8%;
    left: 16%;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.62) 0%, rgba(109, 40, 217, 0.18) 65%, transparent 100%);
    animation: orbFloatOne 14s ease-in-out infinite;
}
.orb-2 {
    width: 480px;
    height: 480px;
    bottom: 6%;
    right: 14%;
    background: radial-gradient(circle, rgba(236, 72, 153, 0.52) 0%, rgba(192, 38, 211, 0.16) 65%, transparent 100%);
    animation: orbFloatTwo 17s ease-in-out infinite;
}
.orb-3 {
    width: 420px;
    height: 420px;
    top: 34%;
    left: 42%;
    background: radial-gradient(circle, rgba(34, 211, 238, 0.42) 0%, rgba(37, 99, 235, 0.14) 65%, transparent 100%);
    animation: orbFloatThree 12s ease-in-out infinite;
}

/* Keep Streamlit content interactive above the background */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {
    background: transparent !important;
    position: relative;
    z-index: 2;
}

header[data-testid="stHeader"] {
    background: rgba(5, 3, 17, 0.35) !important;
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(167, 139, 250, 0.12);
    z-index: 5;
}
header[data-testid="stHeader"] * {
    color: #cbd5e1 !important;
}

.block-container {
    animation: cardFloatIn 0.42s var(--spring) both;
    padding-top: 2rem;
    max-width: 1140px;
    position: relative;
    z-index: 3;
}

.stApp p, .stApp li, .stApp label, .stApp span, .stApp h2, .stApp h3, .stApp h4 {
    color: #f8fafc;
}
.stApp small, div[data-testid="stCaptionContainer"] p {
    color: #94a3b8 !important;
}

.stApp h1 {
    background: linear-gradient(95deg, #ffffff 0%, #d8b4fe 50%, #38bdf8 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    letter-spacing: -0.9px;
    animation: borderShimmer 5s ease infinite;
}

/* Frosted Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(8, 6, 22, 0.86) !important;
    backdrop-filter: blur(22px);
    border-right: 1px solid rgba(167, 139, 250, 0.24);
    z-index: 4;
}
section[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] div.stButton > button {
    background: linear-gradient(90deg, #e11d48, #f97316) !important;
    width: 100%;
}

/* Frosted Obsidian Glass Card for Login & Workspace Tabs */
div[data-testid="stTabs"] {
    background: rgba(10, 8, 26, 0.66) !important;
    backdrop-filter: blur(28px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(160%) !important;
    border: 1px solid rgba(192, 132, 252, 0.30) !important;
    border-radius: 24px !important;
    padding: 22px 28px 28px 28px !important;
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.72), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
}

/* Auth Header */
.auth-header-box {
    text-align: center;
    padding: 8px 12px 16px 12px;
}
.auth-brand {
    font-size: 2.15rem;
    font-weight: 800;
    letter-spacing: -0.9px;
    background: linear-gradient(95deg, #ffffff 10%, #e9d5ff 52%, #7dd3fc 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    -webkit-text-fill-color: transparent;
    margin: 10px 0 6px 0;
    line-height: 1.15;
}
.auth-tagline {
    color: #cbd5e1 !important;
    font-size: 0.94rem;
    margin: 0;
}
.auth-footer-pills {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
}
.f-pill {
    background: rgba(12, 10, 30, 0.68);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(192, 132, 252, 0.28);
    color: #e2e8f0 !important;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 5px 12px;
    border-radius: 999px;
}

/* Crisp Dark Inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"] > input,
textarea {
    background-color: rgba(6, 4, 18, 0.85) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(167, 139, 250, 0.30) !important;
    border-radius: 12px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #c084fc !important;
    box-shadow: 0 0 0 3px rgba(192, 132, 252, 0.26) !important;
}
input, textarea {
    color: #f8fafc !important;
    caret-color: #c084fc !important;
}
div[data-testid="stTabs"] input,
div[data-testid="stTabs"] textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #000000 !important;
}
div[data-baseweb="popover"] {
    background-color: #0b091d !important;
    border: 1px solid rgba(167, 139, 250, 0.38) !important;
}
div[data-baseweb="popover"] * {
    color: #f8fafc !important;
}
div[data-testid="stAlertContainer"]:has(> div[data-testid="stAlertContentError"]) {
    background-color: #b91c1c !important;
    border-color: #ef4444 !important;
}
div[data-testid="stAlertContentError"] p,
div[data-testid="stAlertContentError"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* Snappy Tactile Gradient Buttons */
div.stButton > button {
    background: linear-gradient(95deg, #6d28d9 0%, #9333ea 50%, #2563eb 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 12px !important;
    padding: 0.62rem 1.45rem !important;
    box-shadow: 0 10px 26px rgba(124, 58, 237, 0.42);
    transition: transform 0.14s var(--spring), box-shadow 0.16s ease !important;
}
div.stButton > button p {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
}
div.stButton > button:hover {
    transform: translateY(-2px) scale(1.018);
    box-shadow: 0 14px 34px rgba(147, 51, 234, 0.6), 0 0 18px rgba(56, 189, 248, 0.32);
}
div.stButton > button:active {
    transform: translateY(1px) scale(0.975);
}

/* Pill Tabs */
button[data-baseweb="tab"] {
    border-radius: 10px 10px 0 0 !important;
    font-weight: 700 !important;
    padding: 9px 16px !important;
    color: #94a3b8 !important;
    transition: all 0.14s var(--spring) !important;
}
button[data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background: rgba(139, 92, 246, 0.16) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(139, 92, 246, 0.26) !important;
    color: #e9d5ff !important;
}

/* KPI Metric Cards */
div[data-testid="stMetric"] {
    background: rgba(10, 8, 26, 0.74);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(167, 139, 250, 0.24);
    border-top: 3px solid #a855f7;
    border-radius: 16px;
    padding: 15px 18px;
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.45);
    transition: transform 0.16s var(--spring), border-color 0.16s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px) scale(1.015);
    border-color: #38bdf8;
}
div[data-testid="stMetricLabel"] p {
    color: #a5b4fc !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700 !important;
}

div[data-testid="stExpander"] {
    background: rgba(10, 8, 26, 0.74) !important;
    backdrop-filter: blur(18px);
    border-radius: 15px !important;
    border: 1px solid rgba(167, 139, 250, 0.24) !important;
}

.sec-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(16, 185, 129, 0.16);
    border: 1px solid rgba(16, 185, 129, 0.45);
    color: #6ee7b7 !important;
    padding: 5px 13px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
}
.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10b981;
    display: inline-block;
    animation: pulseDot 1.6s infinite;
}
.room-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(124, 58, 237, 0.28);
    border: 1px solid rgba(192, 132, 252, 0.45);
    color: #f8fafc !important;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px 6px 4px 0;
    max-width: 100%;
    vertical-align: middle;
}
.room-avatar {
    display: block;
    width: 32px;
    height: 32px;
    flex: 0 0 32px;
    border-radius: 50%;
    object-fit: cover;
}
.room-avatar-fallback {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(124, 58, 237, 0.42);
    color: #ffffff !important;
    font-size: 11px;
    font-weight: 700;
}
section[data-testid="stFileUploaderDropzone"] {
    background: rgba(10, 8, 26, 0.80) !important;
    border: 1.5px dashed rgba(192, 132, 252, 0.48) !important;
    border-radius: 14px !important;
}

@media (prefers-color-scheme: light) {
    html, body, .stApp {
        background: #f8fafc !important;
        color: #0f172a;
        color-scheme: light;
    }

    .live-stage-bg {
        background: radial-gradient(ellipse at 50% 0%, #e0e7ff 0%, #f8fafc 74%);
    }
    .live-grid {
        opacity: 0.38;
    }
    .plasma-orb {
        opacity: 0.28;
    }

    header[data-testid="stHeader"] {
        background: rgba(248, 250, 252, 0.82) !important;
        border-bottom-color: rgba(100, 116, 139, 0.18);
    }
    header[data-testid="stHeader"] * {
        color: #334155 !important;
    }

    .stApp p, .stApp li, .stApp label, .stApp span, .stApp h2, .stApp h3, .stApp h4 {
        color: #0f172a;
    }
    .stApp small, div[data-testid="stCaptionContainer"] p {
        color: #64748b !important;
    }
    .stApp h1 {
        background-image: linear-gradient(95deg, #1e1b4b 0%, #6d28d9 52%, #0369a1 100%);
    }

    section[data-testid="stSidebar"] {
        background: rgba(248, 250, 252, 0.94) !important;
        border-right-color: rgba(100, 116, 139, 0.20);
    }
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
    }

    div[data-testid="stTabs"] {
        background: rgba(255, 255, 255, 0.88) !important;
        border-color: rgba(100, 116, 139, 0.22) !important;
        box-shadow: 0 24px 64px rgba(15, 23, 42, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    }
    .auth-brand {
        background-image: linear-gradient(95deg, #1e1b4b 10%, #6d28d9 52%, #0369a1 100%);
    }
    .auth-tagline {
        color: #475569 !important;
    }
    .f-pill {
        background: #f1f5f9;
        border-color: #cbd5e1;
        color: #334155 !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > input,
    textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
    }
    input, textarea {
        color: #0f172a !important;
        caret-color: #7c3aed !important;
    }
    div[data-testid="stTabs"] input,
    div[data-testid="stTabs"] textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
    }
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
    }
    div[data-baseweb="popover"] * {
        color: #0f172a !important;
    }

    button[data-baseweb="tab"] {
        color: #475569 !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #312e81 !important;
        background: rgba(124, 58, 237, 0.08) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(124, 58, 237, 0.12) !important;
        color: #5b21b6 !important;
    }

    div[data-testid="stMetric"],
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.88) !important;
        border-color: rgba(100, 116, 139, 0.20) !important;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
    }
    div[data-testid="stMetricLabel"] p {
        color: #5b21b6 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
    }

    .room-chip {
        background: rgba(124, 58, 237, 0.10);
        border-color: rgba(124, 58, 237, 0.24);
        color: #312e81 !important;
    }
    section[data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.82) !important;
        border-color: rgba(124, 58, 237, 0.34) !important;
    }
}

:root {
    color-scheme: dark;
    --app-bg: #0b1120;
    --surface: rgba(17, 24, 39, 0.90);
    --surface-raised: rgba(24, 34, 53, 0.88);
    --text-primary: #e5e7eb;
    --text-muted: #94a3b8;
    --border: #293548;
    --control-bg: #182235;
    --control-text: #e5e7eb;
    --accent: #4f46e5;
    --accent-hover: #4338ca;
    --accent-soft: rgba(99, 102, 241, 0.14);
    --sidebar-bg: rgba(11, 17, 32, 0.94);
    --header-bg: rgba(11, 17, 32, 0.94);
    --card-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
    --danger: #fca5a5;
    --stage-glow: #172238;
    --cursor-glow: rgba(99, 102, 241, 0.13);
    --orb-indigo: rgba(79, 70, 229, 0.16);
    --orb-cyan: rgba(14, 165, 233, 0.10);
    --grid-line: rgba(148, 163, 184, 0.035);
    --ripple-border: rgba(165, 180, 252, 0.24);
}

@media (prefers-color-scheme: light) {
    :root {
        color-scheme: light;
        --app-bg: #f4f6fa;
        --surface: rgba(255, 255, 255, 0.92);
        --surface-raised: rgba(248, 250, 252, 0.92);
        --text-primary: #172033;
        --text-muted: #64748b;
        --border: #dbe2ea;
        --control-bg: #ffffff;
        --control-text: #172033;
        --accent: #4f46e5;
        --accent-hover: #4338ca;
        --accent-soft: rgba(79, 70, 229, 0.09);
        --sidebar-bg: rgba(255, 255, 255, 0.94);
        --header-bg: rgba(255, 255, 255, 0.94);
        --card-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
        --danger: #b91c1c;
        --stage-glow: #e9edff;
        --cursor-glow: rgba(79, 70, 229, 0.08);
        --orb-indigo: rgba(79, 70, 229, 0.09);
        --orb-cyan: rgba(14, 165, 233, 0.06);
        --grid-line: rgba(100, 116, 139, 0.035);
        --ripple-border: rgba(79, 70, 229, 0.18);
    }
}

html, body, .stApp {
    background: var(--app-bg) !important;
    color: var(--text-primary) !important;
    color-scheme: inherit;
}

.live-stage-bg {
    --pointer-x: 50%;
    --pointer-y: 50%;
    position: fixed !important;
    inset: 0;
    z-index: 0;
    display: block !important;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    pointer-events: none;
    background: radial-gradient(ellipse at 50% 0%, var(--stage-glow) 0%, var(--app-bg) 72%);
}
.live-stage-bg::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: radial-gradient(
        circle 360px at var(--pointer-x) var(--pointer-y),
        var(--cursor-glow),
        transparent 72%
    );
}
.live-grid {
    z-index: 0;
    background-image:
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 72px 72px;
    animation: gridPan 72s linear infinite;
}
.plasma-orb {
    opacity: 0.8;
    filter: blur(88px);
}
.orb-1 {
    background: radial-gradient(circle, var(--orb-indigo) 0%, transparent 72%);
    animation: orbFloatOne 48s ease-in-out infinite;
}
.orb-2 {
    background: radial-gradient(circle, var(--orb-cyan) 0%, transparent 72%);
    animation: orbFloatTwo 56s ease-in-out infinite;
}
.orb-3 {
    background: radial-gradient(circle, var(--orb-indigo) 0%, transparent 72%);
    animation: orbFloatThree 44s ease-in-out infinite;
}
@keyframes backgroundRipple {
    0% {
        opacity: 0.42;
        transform: translate(-50%, -50%) scale(0.08);
    }
    100% {
        opacity: 0;
        transform: translate(-50%, -50%) scale(1);
    }
}
.background-ripple {
    position: absolute;
    width: clamp(220px, 26vw, 380px);
    aspect-ratio: 1;
    border: 1px solid var(--ripple-border);
    border-radius: 50%;
    pointer-events: none;
    animation: backgroundRipple 950ms ease-out forwards;
}

@media (prefers-reduced-motion: reduce) {
    .live-grid, .plasma-orb, .background-ripple {
        animation: none !important;
    }
    .background-ripple {
        display: none;
    }
}

.block-container {
    max-width: 1320px;
    padding-top: 2rem;
    animation: none;
}

header[data-testid="stHeader"] {
    background: var(--header-bg) !important;
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(12px);
}
header[data-testid="stHeader"] * {
    color: var(--text-muted) !important;
}

.stApp p, .stApp li, .stApp label, .stApp span, .stApp h2, .stApp h3, .stApp h4 {
    color: var(--text-primary);
}
.stApp small, div[data-testid="stCaptionContainer"] p {
    color: var(--text-muted) !important;
}
.stApp h1 {
    background: none !important;
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    animation: none;
}

section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border);
    backdrop-filter: none;
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

div[data-testid="stTabs"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    box-shadow: var(--card-shadow) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
}
.auth-brand {
    background: none !important;
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    font-size: clamp(1.3rem, 2.2vw, 1.75rem);
    font-weight: 700;
    white-space: nowrap;
}
.auth-tagline {
    color: var(--text-muted) !important;
}
.f-pill {
    background: var(--surface-raised);
    border-color: var(--border);
    color: var(--text-muted) !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"] > input,
input,
textarea {
    background-color: var(--control-bg) !important;
    color: var(--control-text) !important;
    border-color: var(--border) !important;
    -webkit-text-fill-color: var(--control-text) !important;
    box-shadow: none;
}
div[data-testid="stTextInputRootElement"] {
    background-color: var(--control-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
input, textarea {
    caret-color: var(--accent) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
div[data-testid="stTextInputRootElement"] input {
    background: transparent !important;
    border: 0 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
input:focus, textarea:focus {
    outline: none !important;
    border-color: var(--accent) !important;
}
textarea:focus {
    box-shadow: 0 0 0 2px var(--accent-soft) !important;
}
div[data-baseweb="input"] button {
    background-color: var(--control-bg) !important;
    color: var(--text-muted) !important;
    border-left: 1px solid var(--border) !important;
    box-shadow: none !important;
}
div[data-baseweb="input"] button svg {
    color: var(--text-muted) !important;
    fill: currentColor;
}
div[data-testid="stTextInputRootElement"] button {
    background: var(--control-bg) !important;
    color: var(--text-muted) !important;
    border: 0 !important;
    border-left: 1px solid var(--border) !important;
    border-radius: 0 7px 7px 0 !important;
    box-shadow: none !important;
}
div[data-testid="stTextInputRootElement"] button svg {
    color: var(--text-muted) !important;
    fill: currentColor;
}
div[data-testid="stTextInputRootElement"]:focus-within,
div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-soft) !important;
}

div[data-testid="stTabs"] div[data-baseweb="input"] > div,
div[data-testid="stTabs"] input,
div[data-testid="stTabs"] textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
}
div[data-testid="stTabs"] div[data-testid="stTextInputRootElement"] {
    background: #ffffff !important;
    border-color: #dbe2ea !important;
}
div[data-testid="stTabs"] div[data-testid="stTextInputRootElement"] input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 0 !important;
}
div[data-testid="stTabs"] div[data-testid="stTextInputRootElement"] button {
    background: #ffffff !important;
    color: #64748b !important;
    border-left-color: #dbe2ea !important;
}
div[data-testid="stTabs"] div[data-baseweb="input"] button {
    background-color: #ffffff !important;
    color: #64748b !important;
    border-left-color: #dbe2ea !important;
}
div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-soft) !important;
}
div[data-baseweb="popover"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
}
div[data-baseweb="popover"] * {
    color: var(--text-primary) !important;
}

div.stButton > button {
    background: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 9px !important;
    box-shadow: none !important;
    transition: background-color 0.15s ease, border-color 0.15s ease !important;
}
div.stButton > button p {
    color: #ffffff !important;
    font-weight: 600 !important;
    letter-spacing: 0;
}
div.stButton > button:hover {
    background: var(--accent-hover) !important;
    border-color: var(--accent-hover) !important;
    box-shadow: none !important;
    transform: none;
}
div.stButton > button:active {
    transform: none;
}
section[data-testid="stSidebar"] div.stButton > button {
    background: transparent !important;
    border-color: var(--border) !important;
}
section[data-testid="stSidebar"] div.stButton > button p {
    color: var(--danger) !important;
}

button[data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    transition: color 0.15s ease, background-color 0.15s ease !important;
}
button[data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: var(--accent-soft) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: var(--accent-soft) !important;
    color: var(--accent) !important;
}

div[data-testid="stMetric"],
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: var(--card-shadow) !important;
    backdrop-filter: none;
}
div[data-testid="stMetric"] {
    border-top: 1px solid var(--border) !important;
    padding: 12px !important;
    transition: border-color 0.15s ease !important;
}
div[data-testid="stMetric"]:hover {
    transform: none;
    border-color: var(--accent) !important;
}
div[data-testid="stMetricLabel"] p {
    color: var(--text-muted) !important;
    font-size: 0.62rem !important;
    line-height: 1.25 !important;
    white-space: normal !important;
}
div[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: clamp(0.75rem, 1vw, 1rem) !important;
    line-height: 1.2 !important;
    white-space: normal !important;
    overflow-wrap: anywhere;
}

.sec-badge {
    background: rgba(16, 185, 129, 0.10);
    border-color: rgba(16, 185, 129, 0.25);
    color: #34d399 !important;
}
.live-dot {
    animation: none;
}
.room-chip {
    background: var(--accent-soft);
    border-color: var(--border);
    color: var(--text-primary) !important;
}
section[data-testid="stFileUploaderDropzone"] {
    background: var(--surface-raised) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
}
a {
    color: var(--accent);
}

@media (prefers-color-scheme: light) {
    .stApp h1, .auth-brand {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
    }
    section[data-testid="stSidebar"] div.stButton > button p {
        color: var(--danger) !important;
    }
}

@media (max-width: 640px) {
    .auth-brand {
        white-space: normal;
        font-size: 1.4rem;
    }
}
</style>

<div class="live-stage-bg">
    <div class="live-grid"></div>
    <div class="plasma-orb orb-1"></div>
    <div class="plasma-orb orb-2"></div>
    <div class="plasma-orb orb-3"></div>
</div>
""", unsafe_allow_html=True)

st.html(
    """
    <script>
    (() => {
        const controllerKey = "__smartExpenseBackgroundController";

        if (!window[controllerKey]) {
            let framePending = false;
            let pointerX = 50;
            let pointerY = 50;

            const updatePointer = (event) => {
                if (event.pointerType === "touch") return;

                pointerX = (event.clientX / window.innerWidth) * 100;
                pointerY = (event.clientY / window.innerHeight) * 100;
                if (framePending) return;

                framePending = true;
                window.requestAnimationFrame(() => {
                    framePending = false;
                    const stage = document.querySelector(".live-stage-bg");
                    if (!stage) return;
                    stage.style.setProperty("--pointer-x", `${pointerX}%`);
                    stage.style.setProperty("--pointer-y", `${pointerY}%`);
                });
            };

            const rippleOnClick = (event) => {
                if (event.button !== 0) return;
                const stage = document.querySelector(".live-stage-bg");
                if (!stage) return;

                const previousRipples = stage.querySelectorAll(".background-ripple");
                if (previousRipples.length >= 3) previousRipples[0].remove();

                const ripple = document.createElement("span");
                ripple.className = "background-ripple";
                ripple.style.left = `${event.clientX}px`;
                ripple.style.top = `${event.clientY}px`;
                stage.appendChild(ripple);
                window.setTimeout(() => ripple.remove(), 1000);
            };

            document.addEventListener("pointermove", updatePointer, {passive: true});
            document.addEventListener("pointerdown", rippleOnClick, {passive: true});
            window[controllerKey] = true;
        }
    })();
    </script>
    <script>
    (() => {
        const controllerKey = "__smartExpenseLoginRepelController";
        const baselineByButton = new WeakMap();
        const validationTimers = new WeakMap();
        let lastPointerX = window.innerWidth / 2;
        let lastPointerY = window.innerHeight / 2;
        let lastEscapeX = 0;
        let lastEscapeY = 1;
        let animationFrameId = null;
        let animationButton = null;
        const stateMarker = () => document.getElementById("login-repel-state");
        const repelIsActive = () => stateMarker()?.dataset.active === "true";
        const getLoginButton = () => Array.from(document.querySelectorAll("button")).find(
            (button) => button.textContent.replace(/\\s+/g, " ").trim().startsWith("Sign In to Workspace")
        );

        if (window[controllerKey]) return;

        const restoreButton = () => {
            const button = getLoginButton();
            if (animationFrameId !== null) {
                window.cancelAnimationFrame(animationFrameId);
                animationFrameId = null;
            }
            if (button) {
                button.style.transform = "";
                button.style.willChange = "";
                baselineByButton.delete(button);
            }
            if (animationButton && animationButton !== button) {
                animationButton.style.transform = "";
                animationButton.style.willChange = "";
                baselineByButton.delete(animationButton);
            }
            animationButton = null;
        };

        const animateButton = () => {
            animationFrameId = null;
            const button = animationButton;
            if (!button || !button.isConnected) {
                animationButton = null;
                return;
            }

            const motion = baselineByButton.get(button);
            if (!motion) {
                animationButton = null;
                return;
            }

            motion.x += (motion.targetX - motion.x) * 0.2;
            motion.y += (motion.targetY - motion.y) * 0.2;
            button.style.willChange = "transform";

            if (Math.abs(motion.targetX - motion.x) < 0.15
                && Math.abs(motion.targetY - motion.y) < 0.15) {
                motion.x = motion.targetX;
                motion.y = motion.targetY;
                button.style.transform = motion.x === 0 && motion.y === 0
                    ? ""
                    : `translate3d(${motion.x}px, ${motion.y}px, 0)`;
                if (motion.x === 0 && motion.y === 0) button.style.willChange = "";
                return;
            }

            button.style.transform = `translate3d(${motion.x}px, ${motion.y}px, 0)`;
            animationFrameId = window.requestAnimationFrame(animateButton);
        };

        const moveButtonTo = (button, motion, x, y) => {
            motion.targetX = x;
            motion.targetY = y;
            animationButton = button;
            if (animationFrameId === null) {
                animationFrameId = window.requestAnimationFrame(animateButton);
            }
        };

        const moveAwayFromPointer = (event) => {
            if (event.pointerType === "touch") return;
            const pointerDeltaX = event.clientX - lastPointerX;
            const pointerDeltaY = event.clientY - lastPointerY;
            lastPointerX = event.clientX;
            lastPointerY = event.clientY;

            if (!repelIsActive()) {
                restoreButton();
                return;
            }

            const button = getLoginButton();
            if (!button) return;

            let baseline = baselineByButton.get(button);
            if (!baseline) {
                const rect = button.getBoundingClientRect();
                const card = button.closest('[data-testid="stTabs"]');
                const bounds = card ? card.getBoundingClientRect() : {
                    left: 0,
                    top: 0,
                    right: window.innerWidth,
                    bottom: window.innerHeight,
                    width: window.innerWidth,
                    height: window.innerHeight,
                };
                baseline = {left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom,
                    width: rect.width, height: rect.height, bounds, x: 0, y: 0, targetX: 0, targetY: 0};
                baselineByButton.set(button, baseline);
            }

            const centerX = baseline.left + baseline.x + baseline.width / 2;
            const centerY = baseline.top + baseline.y + baseline.height / 2;
            const awayX = centerX - event.clientX;
            const awayY = centerY - event.clientY;
            const distance = Math.hypot(awayX, awayY);
            const radius = 250;

            if (distance > 1) {
                lastEscapeX = awayX / distance;
                lastEscapeY = awayY / distance;
            } else {
                const pointerSpeed = Math.hypot(pointerDeltaX, pointerDeltaY);
                if (pointerSpeed > 1) {
                    lastEscapeX = pointerDeltaX / pointerSpeed;
                    lastEscapeY = pointerDeltaY / pointerSpeed;
                }
            }

            if (distance >= radius) {
                moveButtonTo(button, baseline, 0, 0);
                return;
            }

            const strength = (radius - distance) / radius;
            const maxX = baseline.bounds.width * 0.1;
            const maxY = baseline.bounds.height * 0.1;
            const safeRadius = Math.hypot(baseline.width / 2, baseline.height / 2) + 12;
            const bubbleStrength = Math.max(0, Math.min(1, (radius - distance) / (radius - safeRadius)));
            const minLeft = Math.max(0, baseline.bounds.left) + 6;
            const maxRight = Math.min(window.innerWidth, baseline.bounds.right) - 6;
            const minTop = Math.max(0, baseline.bounds.top) + 6;
            const maxBottom = Math.min(window.innerHeight, baseline.bounds.bottom) - 6;
            const minX = Math.max(-maxX, minLeft - baseline.left);
            const maxAllowedX = Math.min(maxX, maxRight - baseline.right);
            const minY = Math.max(-maxY, minTop - baseline.top);
            const maxAllowedY = Math.min(maxY, maxBottom - baseline.bottom);
            const desiredX = lastEscapeX * maxX * bubbleStrength * strength;
            const desiredY = lastEscapeY * maxY * bubbleStrength * strength;
            let offsetX = Math.min(maxAllowedX, Math.max(minX, desiredX));
            let offsetY = Math.min(maxAllowedY, Math.max(minY, desiredY));

            const edgeGap = 14;
            const left = baseline.left + offsetX;
            const top = baseline.top + offsetY;
            const cursorCovered = event.clientX >= left - edgeGap
                && event.clientX <= left + baseline.width + edgeGap
                && event.clientY >= top - edgeGap
                && event.clientY <= top + baseline.height + edgeGap;

            if (cursorCovered) {
                const candidates = [
                    {x: offsetX, y: event.clientY - edgeGap - 1 - baseline.top - baseline.height},
                    {x: offsetX, y: event.clientY + edgeGap + 1 - baseline.top},
                    {x: event.clientX - edgeGap - 1 - baseline.left - baseline.width, y: offsetY},
                    {x: event.clientX + edgeGap + 1 - baseline.left, y: offsetY},
                ].filter((candidate) =>
                    candidate.x >= minX && candidate.x <= maxAllowedX
                    && candidate.y >= minY && candidate.y <= maxAllowedY
                );

                if (candidates.length) {
                    candidates.sort((a, b) =>
                        Math.hypot(a.x - offsetX, a.y - offsetY)
                        - Math.hypot(b.x - offsetX, b.y - offsetY)
                    );
                    offsetX = candidates[0].x;
                    offsetY = candidates[0].y;
                }
            }

            moveButtonTo(button, baseline, offsetX, offsetY);
        };

        document.addEventListener("pointermove", moveAwayFromPointer, {passive: true});
        document.addEventListener("input", (event) => {
            const input = event.target;
            if (!(input instanceof HTMLInputElement)) return;

            const panel = input.closest('[data-testid="stTabPanel"]');
            const marker = panel?.querySelector("#login-repel-state");
            const label = input.getAttribute("aria-label");
            if (!marker || (label !== "Username" && label !== "Password")) return;

            marker.dataset.active = "false";
            restoreButton();

            const previousTimer = validationTimers.get(input);
            if (previousTimer) window.clearTimeout(previousTimer);
            validationTimers.set(input, window.setTimeout(() => {
                if (!input.isConnected) return;
                input.dispatchEvent(new KeyboardEvent("keydown", {
                    key: "Enter",
                    code: "Enter",
                    bubbles: true,
                }));
            }, 600));
        });
        document.addEventListener("click", (event) => {
            if (!repelIsActive()) return;
            const button = getLoginButton();
            if (button && (event.target === button || button.contains(event.target))) {
                event.preventDefault();
                event.stopImmediatePropagation();
            }
        }, true);

        const observer = new MutationObserver(() => {
            if (!repelIsActive()) {
                restoreButton();
            } else {
                moveAwayFromPointer({
                    pointerType: "mouse",
                    clientX: lastPointerX,
                    clientY: lastPointerY,
                });
            }
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ["data-active"],
        });
        window.addEventListener("resize", restoreButton);
        window[controllerKey] = true;
    })();
    </script>
    """,
    unsafe_allow_javascript=True,
)

# ------------------------------------------------------------
# BUILT-IN AUTHENTICATED ENCRYPTION (SHA-256 CTR + HMAC-SHA256)
# ------------------------------------------------------------
KEY_FILE = ".splitter_key"
TEXT_PREFIX = "enc2::"
BLOB_PREFIX = b"ENC2::"


@st.cache_resource
def _get_master_key() -> bytes:
    secret = ""
    try:
        secret = str(st.secrets.get("SPLITTER_MASTER_KEY", "")).strip()
    except Exception:
        secret = ""
    if not secret:
        secret = os.environ.get("SPLITTER_MASTER_KEY", "").strip()
    if secret:
        return hashlib.sha256(secret.encode("utf-8")).digest()

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            raw = f.read().strip()
            if len(raw) >= 32:
                return hashlib.sha256(raw).digest()
    raw = os.urandom(32).hex().encode("utf-8")
    with open(KEY_FILE, "wb") as f:
        f.write(raw)
    return hashlib.sha256(raw).digest()


def _derive_keys(master: bytes) -> tuple[bytes, bytes]:
    enc_key = hashlib.sha256(master + b"::enc").digest()
    mac_key = hashlib.sha256(master + b"::mac").digest()
    return enc_key, mac_key


def _keystream(enc_key: bytes, nonce: bytes, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hashlib.sha256(enc_key + nonce + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:length])


def _encrypt_bytes(raw: bytes) -> bytes:
    enc_key, mac_key = _derive_keys(_get_master_key())
    nonce = os.urandom(16)
    ks = _keystream(enc_key, nonce, len(raw))
    ct = bytes(a ^ b for a, b in zip(raw, ks))
    tag = hmac.new(mac_key, nonce + ct, hashlib.sha256).digest()
    return nonce + tag + ct


def _decrypt_bytes(payload: bytes) -> bytes | None:
    if len(payload) < 48:
        return None
    enc_key, mac_key = _derive_keys(_get_master_key())
    nonce, tag, ct = payload[:16], payload[16:48], payload[48:]
    expected = hmac.new(mac_key, nonce + ct, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        return None
    ks = _keystream(enc_key, nonce, len(ct))
    return bytes(a ^ b for a, b in zip(ct, ks))


def encrypt_upi(plain: str) -> str:
    plain = (plain or "").strip()
    if not plain:
        return ""
    token = base64.urlsafe_b64encode(_encrypt_bytes(plain.encode("utf-8"))).decode("ascii")
    return TEXT_PREFIX + token


def decrypt_upi(stored: str) -> tuple[str, bool, bool]:
    if not stored:
        return "", False, True
    if not stored.startswith(TEXT_PREFIX):
        return stored, False, True
    try:
        raw = base64.urlsafe_b64decode(stored[len(TEXT_PREFIX):].encode("ascii"))
        dec = _decrypt_bytes(raw)
        if dec is None:
            return "", True, False
        return dec.decode("utf-8"), True, True
    except Exception:
        return "", True, False


def encrypt_qr(raw: bytes | None) -> bytes | None:
    if not raw:
        return None
    return BLOB_PREFIX + _encrypt_bytes(bytes(raw))


def decrypt_qr(stored: bytes | None) -> tuple[bytes | None, bool, bool]:
    if not stored:
        return None, False, True
    raw = bytes(stored)
    if not raw.startswith(BLOB_PREFIX):
        return raw, False, True
    dec = _decrypt_bytes(raw[len(BLOB_PREFIX):])
    if dec is None:
        return None, True, False
    return dec, True, True


def mask_upi(upi_id: str) -> str:
    if not upi_id or "@" not in upi_id:
        return upi_id
    handle, bank = upi_id.split("@", 1)
    vis = handle[:2] if len(handle) > 2 else handle[:1]
    return f"{vis}{'*' * max(3, len(handle) - len(vis))}@{bank}"


# ------------------------------------------------------------
# DB CONNECTION & NOTIFICATIONS
# ------------------------------------------------------------
@st.cache_resource
def get_conn():
    return lg.connect()


conn = get_conn()
# Streamlit may reuse this connection after the database schema has changed.
user_columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)")}
if "avatar_image" not in user_columns:
    conn.execute("ALTER TABLE users ADD COLUMN avatar_image BLOB")
    conn.commit()


def persist_avatar(uid, avatar_image):
    if hasattr(lg, "set_avatar"):
        lg.set_avatar(conn, uid, avatar_image)
    else:
        # A live rerun may still hold an older, already-imported logic module.
        conn.execute("UPDATE users SET avatar_image=? WHERE id=?", (avatar_image, uid))
        conn.commit()

if "toast" in st.session_state:
    st.toast(st.session_state.pop("toast"))
if st.session_state.pop("balloons", False):
    st.balloons()


def notify(msg, balloons=False):
    st.session_state["toast"] = msg
    if balloons:
        st.session_state["balloons"] = True
    st.rerun()


# ------------------------------------------------------------
# HELPERS: UPI QR + BILL SCAN (OPTIONAL OCR)
# ------------------------------------------------------------
def make_upi_qr(upi_id, name, amount):
    try:
        import qrcode
        link = f"upi://pay?pa={upi_id}&pn={quote(name)}&am={amount:.2f}&cu=INR"
        img = qrcode.make(link)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return None


def shrink_image(file_bytes, max_side=500):
    from PIL import Image, ImageOps, UnidentifiedImageError

    try:
        with Image.open(io.BytesIO(file_bytes)) as source:
            source.load()
            img = ImageOps.exif_transpose(source).convert("RGB")
        img.thumbnail((max_side, max_side))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        raise ValueError(
            "The QR image could not be read. Re-save it as a valid PNG or JPG and upload it again."
        ) from exc


def prepare_avatar(file_bytes):
    from PIL import Image, ImageOps, UnidentifiedImageError

    try:
        with Image.open(io.BytesIO(file_bytes)) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        raise ValueError("Upload a valid PNG or JPG image.") from exc

    width, height = image.size
    side = min(width, height)
    if side == 0:
        raise ValueError("The uploaded image has no usable dimensions.")

    left = (width - side) // 2
    top = (height - side) // 2
    image = image.crop((left, top, left + side, top + side))
    image.thumbnail((256, 256))
    buf = io.BytesIO()
    image.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


@st.cache_resource
def get_ocr_engine():
    from rapidocr_onnxruntime import RapidOCR
    return RapidOCR()


def scan_bill(file_bytes):
    try:
        import numpy as np
        from PIL import Image
        engine = get_ocr_engine()
    except Exception:
        return None, "OCR engine is optional on this host. Type the amount manually."
    try:
        img = np.array(Image.open(io.BytesIO(file_bytes)).convert("RGB"))
        result, _ = engine(img)
        lines = [r[1] for r in (result or [])]
        total = lg.parse_total(lines)
        if total is None:
            return None, "Could not detect a clear total on this receipt. Enter the amount manually."
        return total, f"Detected total ₹{total:,.2f}. Check before saving."
    except Exception as e:
        return None, f"Scan failed ({e}). Enter the amount manually."


# ------------------------------------------------------------
# LOGIN / REGISTER SCREEN (Centered Floating Obsidian Glass Card)
# ------------------------------------------------------------
def _validate_login_repel():
    username = st.session_state.get("login_user", "")
    password = st.session_state.get("login_pw", "")
    if not username.strip() or not password:
        st.session_state["login_repel_active"] = False
        return

    st.session_state["login_repel_active"] = lg.check_login(conn, username, password) is None


def auth_screen():
    st.session_state.setdefault("login_repel_active", False)
    _, center, _ = st.columns([1, 1.35, 1])
    with center:
        st.markdown("""
        <div class="auth-header-box">
            <div class="sec-badge"><span class="live-dot"></span> Encrypted FinTech Ledger</div>
            <div class="auth-brand">💸 Smart Expense Splitter</div>
            <p class="auth-tagline">
                Split group trips &amp; hostel bills fairly · Minimum-transfer UPI settlements
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["🔑 Sign In", "📝 Create Account"])
        with tab_login:
            u = st.text_input("Username", placeholder="e.g. sayan", key="login_user",
                              on_change=_validate_login_repel)
            p = st.text_input("Password", type="password", placeholder="••••••••", key="login_pw",
                              on_change=_validate_login_repel)
            active = st.session_state["login_repel_active"]
            st.markdown(
                f'<span id="login-repel-state" data-active="{str(active).lower()}" '
                'style="display:none"></span>',
                unsafe_allow_html=True,
            )
            if active:
                st.caption("Those credentials didn't match. Update either field to try again.")
            _, login_button, _ = st.columns([1, 4, 1])
            with login_button:
                submitted = st.button("Sign In to Workspace →", use_container_width=True)
            if submitted:
                user = lg.check_login(conn, u, p)
                if user:
                    st.session_state["login_repel_active"] = False
                    st.session_state["uid"] = user["id"]
                    notify(f"Welcome back, {user['display_name']}! 👋")
                else:
                    st.session_state["login_repel_active"] = True

        with tab_reg:
            ru = st.text_input("Username", placeholder="min 3 characters", key="reg_user")
            rn = st.text_input("Display Name", placeholder="shown to room members", key="reg_name")
            rp = st.text_input("Password", type="password", placeholder="min 4 characters", key="reg_pw")
            rp2 = st.text_input("Confirm Password", type="password", placeholder="re-enter password", key="reg_pw2")
            if st.button("Create Secure Account →", use_container_width=True):
                if rp != rp2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = lg.create_user(conn, ru, rn, rp)
                    (st.success if ok else st.error)(msg)

        st.markdown("""
        <div class="auth-footer-pills">
            <span class="f-pill">🔐 PBKDF2-SHA256 Auth</span>
            <span class="f-pill">🛡️ Encrypted UPI Vault</span>
            <span class="f-pill">📸 Receipt OCR</span>
            <span class="f-pill">⚡ Min-Transfer Solver</span>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------
# PAGE: PROFILE & ENCRYPTED UPI VAULT
# ------------------------------------------------------------
def page_profile(user):
    st.subheader("🔐 Profile & Encrypted UPI Vault")
    st.markdown(
        '<div class="sec-badge"><span class="live-dot"></span> SHA-256 CTR + HMAC-SHA256 Encrypted Storage Active</div>',
        unsafe_allow_html=True,
    )

    saved_avatar = user.get("avatar_image")
    raw_upi = user["upi_id"] or ""
    upi_plain, upi_was_enc, upi_ok = decrypt_upi(raw_upi)
    qr_plain, qr_was_enc, qr_ok = decrypt_qr(user["qr_image"])

    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        st.markdown("#### Profile Picture")
        if saved_avatar:
            st.image(saved_avatar, width=96, caption="Current profile picture")
        else:
            st.caption("No profile picture saved. Your initials will appear in room member lists.")
        st.caption("Visible to other members of rooms you're in.")
        avatar_upload = st.file_uploader(
            "Upload a profile picture",
            type=["png", "jpg", "jpeg"],
            key=f"avatar_upload_{user['id']}",
            help="PNG or JPG, up to 5 MB. Other members in your rooms can see it.",
        )
        if avatar_upload is not None:
            avatar_bytes = avatar_upload.getvalue()
            if len(avatar_bytes) > 5 * 1024 * 1024:
                st.error("Profile pictures must be 5 MB or smaller.")
            else:
                try:
                    avatar_preview = prepare_avatar(avatar_bytes)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.image(avatar_preview, width=96, caption="Preview")
                    if st.button("Save Profile Picture", key=f"save_avatar_{user['id']}"):
                        persist_avatar(user["id"], avatar_preview)
                        notify("Profile picture saved.")
        if saved_avatar and st.button("Remove Profile Picture", key=f"remove_avatar_{user['id']}"):
            persist_avatar(user["id"], None)
            notify("Profile picture removed.")

        name = st.text_input("Display Name", value=user["display_name"], key="prof_name")
        if upi_was_enc and not upi_ok:
            st.warning("Existing encrypted UPI could not be unlocked with the current master key. Re-enter to re-encrypt.")
        upi_input = st.text_input(
            "Your UPI ID (e.g. sayan@okicici)",
            value=upi_plain,
            key="prof_upi",
            type="password",
            help="Encrypted before writing to SQLite; masked in UI.",
        )
        if upi_plain:
            st.caption(
                f"Saved UPI (masked): `{mask_upi(upi_plain)}`  ·  Encrypted in DB: "
                f"**{'Yes' if upi_was_enc else 'Legacy (save to encrypt)'}**"
            )
            if upi_was_enc:
                with st.expander("🔍 Inspect Encrypted Database Ciphertext"):
                    st.code(raw_upi[:84] + "...", language="text")

        if st.button("Encrypt & Save Profile"):
            if name.strip():
                lg.update_profile(conn, user["id"], name, encrypt_upi(upi_input))
                notify("Profile & UPI encrypted and saved ✅")
            else:
                st.error("Name cannot be empty.")

    with c2:
        st.write("**Encrypted Payment QR** (decrypted only for room settlements)")
        if qr_was_enc and not qr_ok:
            st.warning("Saved QR could not be decrypted with the current master key. Re-upload below.")
        elif qr_plain:
            st.image(
                qr_plain,
                width=210,
                caption=f"Decrypted preview ({'Encrypted BLOB' if qr_was_enc else 'Legacy BLOB — re-upload to encrypt'})",
            )
            if st.button("Remove Saved QR"):
                lg.set_qr(conn, user["id"], None)
                notify("QR removed from vault.")
        else:
            st.caption("No custom QR uploaded. A dynamic UPI QR is generated automatically from your encrypted UPI ID.")

        up = st.file_uploader("Upload your UPI QR screenshot", type=["png", "jpg", "jpeg"], key="qr_upload")
        if up is not None and st.button("Encrypt & Save QR"):
            try:
                qr_image = shrink_image(up.getvalue())
            except ValueError as exc:
                st.error(str(exc))
            else:
                lg.set_qr(conn, user["id"], encrypt_qr(qr_image))
                notify("QR image encrypted and saved ✅")


# ------------------------------------------------------------
# PAGE: MY HISTORY
# ------------------------------------------------------------
def page_history(user):
    st.subheader("📜 My Closed Rooms History")
    st.caption("When a host closes a settled room, your summary stays here while detailed room bills are wiped.")
    rows = lg.history_for_user(conn, user["id"])
    if not rows:
        st.info("No finished rooms yet.")
        return
    c1, c2, c3 = st.columns(3)
    c1.metric("Rooms Finished", len(rows))
    c2.metric("Total You Paid", f"₹{sum(r['my_paid'] for r in rows):,.2f}")
    c3.metric("Your Net Shares", f"₹{sum(r['my_share'] for r in rows):,.2f}")
    df = pd.DataFrame(rows).rename(columns={
        "closed_on": "Closed On", "room_name": "Room", "host_name": "Host", "members_text": "Members",
        "total_spent": "Room Total (₹)", "my_paid": "You Paid (₹)", "my_share": "Your Share (₹)",
        "expense_count": "Bills"})
    st.dataframe(df, hide_index=True, use_container_width=True)


# ------------------------------------------------------------
# PAGE: MY ROOMS
# ------------------------------------------------------------
def page_rooms(user):
    uid = user["id"]

    col_a, col_b = st.columns(2)
    with col_a:
        with st.expander("➕ Create a Room (You become Host)"):
            rname = st.text_input("Room name (e.g. Goa Trip)", key="new_room_name")
            if st.button("Create Room"):
                if rname.strip():
                    lg.create_room(conn, rname, uid)
                    notify("Room created! Share its code with your group. 🎉", balloons=True)
                else:
                    st.error("Enter a room name.")
    with col_b:
        with st.expander("🔑 Join a Room via Code"):
            jcode = st.text_input("6-character code from host", key="join_code")
            if st.button("Join Room"):
                ok, msg, _ = lg.join_room(conn, jcode, uid)
                if ok:
                    notify(msg)
                else:
                    st.error(msg)

    rooms = lg.rooms_for_user(conn, uid)
    if not rooms:
        st.info("You are not in any room yet. Create one above or join using a friend's code.")
        return

    labels = {}
    for r in rooms:
        label = r["name"] if r["name"] not in labels else f"{r['name']} #{r['id']}"
        labels[label] = r
    pick = st.selectbox("🎯 Select Active Room", list(labels.keys()), key="room_pick")
    room = labels[pick]
    rid = room["id"]
    is_host = room["host_user_id"] == uid

    members = lg.room_members(conn, rid)
    if members and "avatar_image" not in members[0]:
        avatar_rows = conn.execute(
            "SELECT m.id, u.avatar_image FROM members m "
            "LEFT JOIN users u ON m.user_id=u.id WHERE m.room_id=?",
            (rid,),
        )
        avatars_by_member = {row["id"]: row["avatar_image"] for row in avatar_rows}
        for member in members:
            member["avatar_image"] = avatars_by_member.get(member["id"])
    mid_by_name = {m["name"]: m["id"] for m in members}
    my_mid = next((m["id"] for m in members if m["user_id"] == uid), members[0]["id"])
    bal = lg.compute_balances(conn, rid)
    total_spend = sum(b["paid"] for b in bal.values())
    my_net = bal[my_mid]["net"]

    left_col, right_col = st.columns([1, 1.45], gap="large")

    with right_col:
        with st.container(border=True):
            st.markdown("#### Room Overview")
            k1, k2 = st.columns(2)
            k1.metric("Room Code", room["code"] if is_host else "JOINED")
            k2.metric("Members", len(members))
            k3, k4 = st.columns(2)
            k3.metric("Total Spend", f"₹{total_spend:,.2f}")
            k4.metric("Balance", f"₹{my_net:+,.2f}",
                      delta="In" if my_net > 0 else ("Owe" if my_net < 0 else "Even"))

    # ---------------- Members ----------------
    with left_col:
        st.subheader("Members")
        chips_html = ""
        for m in members:
            tags = []
            if m["id"] == my_mid:
                tags.append("You")
            if m["user_id"] == room["host_user_id"]:
                tags.append("Host")
            if m["user_id"] is None:
                tags.append("Guest")
            role = f" · {' / '.join(tags)}" if tags else ""
            safe_name = html.escape(m["name"])
            if m["avatar_image"]:
                avatar = base64.b64encode(m["avatar_image"]).decode("ascii")
                avatar_html = (
                    f'<img class="room-avatar" src="data:image/png;base64,{avatar}" '
                    f'alt="Profile picture of {safe_name}">'
                )
            else:
                initials = "".join(part[0] for part in m["name"].split()[:2]).upper() or "?"
                avatar_html = (
                    f'<span class="room-avatar room-avatar-fallback" aria-hidden="true">'
                    f'{html.escape(initials)}</span>'
                )
            chips_html += (
                f'<span class="room-chip">{avatar_html}'
                f'<span>{safe_name}{html.escape(role)}</span></span> '
            )
        st.markdown(chips_html, unsafe_allow_html=True)

        if is_host:
            st.divider()
            g = st.text_input("Add a friend without an account (Guest)", key=f"guest_{rid}")
            if st.button("Add Guest"):
                if lg.add_guest(conn, rid, g):
                    notify(f"{g.strip()} added.")
                else:
                    st.error("Enter a new, unique name.")
            removable = [m["name"] for m in members if m["user_id"] != room["host_user_id"]]
            if removable:
                who = st.selectbox("Remove a member", removable, key=f"rm_{rid}")
                if st.button("Remove Member"):
                    if lg.remove_member_if_unused(conn, rid, mid_by_name[who]):
                        notify(f"{who} removed.")
                    else:
                        st.error(f"{who} is part of existing bills. Delete those expenses first.")

    # ---------------- Add Expense ----------------
    with left_col:
        st.divider()
        st.subheader("Add Expense")
        if len(members) < 2:
            st.warning("Add or wait for at least 2 members first.")
        else:
            names = [m["name"] for m in members]
            amt_key, desc_key = f"amt_{rid}", f"desc_{rid}"

            with st.expander("📸 Scan a Bill Photo (OCR Auto-Fill)"):
                img = st.file_uploader("Upload bill image", type=["png", "jpg", "jpeg"], key=f"bill_{rid}")
                if img is not None and st.button("Read Amount from Bill"):
                    value, msg = scan_bill(img.getvalue())
                    if value:
                        st.session_state[amt_key] = float(value)
                        st.success(msg)
                    else:
                        st.warning(msg)

            desc = st.text_input("Description (e.g. Dinner, Cab)", key=desc_key)
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, key=amt_key)
            category = st.selectbox("Category", ["Food", "Travel", "Rent", "Groceries", "Shopping", "Other"],
                                    key=f"cat_{rid}")
            exp_date = st.date_input("Date", value=date.today(), key=f"date_{rid}")
            payer = st.selectbox("Who paid?", names, index=names.index(next(
                m["name"] for m in members if m["id"] == my_mid)), key=f"payer_{rid}")
            split_type = st.radio("Split Mode", ["Equal", "Custom"], horizontal=True, key=f"st_{rid}")

            shares = {}
            if split_type == "Equal":
                people = st.multiselect("Split between", names, default=names, key=f"ppl_{rid}")
                if people and amount > 0:
                    shares = lg.split_equal(amount, [mid_by_name[p] for p in people])
                    st.info(f"Live Split Preview: **{len(people)} members** × **₹{amount / len(people):,.2f}** each")
            else:
                st.write("Enter each member's custom share:")
                cols = st.columns(min(2, len(names)))
                for idx, n in enumerate(names):
                    with cols[idx % len(cols)]:
                        v = st.number_input(n, min_value=0.0, step=10.0, key=f"custom_{rid}_{mid_by_name[n]}")
                        if v > 0:
                            shares[mid_by_name[n]] = v
                entered = sum(shares.values())
                remaining = round(amount - entered, 2)
                st.caption(f"Entered: ₹{entered:,.2f} / Bill: ₹{amount:,.2f}  |  Remaining: ₹{remaining:,.2f}")

            if st.button("Save Expense"):
                if amount <= 0 or not shares:
                    st.error("Enter an amount and who shares it.")
                elif abs(sum(shares.values()) - amount) > 0.01:
                    st.error("Shares must add up to the total amount!")
                else:
                    lg.add_expense(conn, rid, mid_by_name[payer], amount, desc, category,
                                   str(exp_date), shares)
                    for k in [amt_key, desc_key] + [f"custom_{rid}_{m['id']}" for m in members]:
                        st.session_state.pop(k, None)
                    notify("Expense saved! 🎈", balloons=True)

    # ---------------- Balances & Encrypted UPI Pay ----------------
    with right_col:
        st.divider()
        st.subheader("Settlements")
        st.caption("Minimum-transfer payment plan")
        plan = lg.settle_plan({m: b["net"] for m, b in bal.items()})
        if not plan:
            st.success("All settled! Nobody owes anything. 🎉")
        for f, t, amt in plan:
            fn, tn = bal[f]["name"], bal[t]["name"]
            with st.expander(f"👉 {fn} pays {tn} ₹{amt:,.2f}", expanded=False):
                rec = lg.user_of_member(conn, t)
                rec_upi, upi_enc, upi_ok = decrypt_upi(rec["upi_id"] or "") if rec else ("", False, True)
                rec_qr, qr_enc, qr_ok = decrypt_qr(rec["qr_image"]) if rec else (None, False, True)

                if rec and (rec_qr or rec_upi):
                    if upi_enc or qr_enc:
                        st.markdown(
                            '<div class="sec-badge"><span class="live-dot"></span> Decrypted for Active Room Settlement</div>',
                            unsafe_allow_html=True,
                        )
                    qcol, icol = st.container(), st.container()
                    with qcol:
                        if rec_qr:
                            st.image(rec_qr, width=210, caption=f"{tn}'s Verified UPI QR — pay ₹{amt:,.2f}")
                        elif rec_upi:
                            qr = make_upi_qr(rec_upi, rec["display_name"], amt)
                            if qr:
                                st.image(qr, width=210, caption=f"Dynamic QR · ₹{amt:,.2f} pre-filled")
                    with icol:
                        if rec_upi:
                            st.write(f"**Payee:** {tn}")
                            st.write(f"**Masked UPI:** `{mask_upi(rec_upi)}`")
                            with st.expander("Reveal Full UPI ID to Copy"):
                                st.code(rec_upi)
                            upi_uri = f"upi://pay?pa={rec_upi}&pn={quote(rec['display_name'])}&am={amt:.2f}&cu=INR"
                            st.markdown(f"[📲 Open in UPI App (₹{amt:,.2f})]({upi_uri})")
                elif rec and ((upi_enc and not upi_ok) or (qr_enc and not qr_ok)):
                    st.warning(f"{tn}'s encrypted UPI/QR could not be decrypted with the current key.")
                else:
                    st.info(f"{tn} has not added UPI details yet (Profile & UPI Vault page).")

                if st.button("✓ Mark as Paid", key=f"paid_{rid}_{f}_{t}"):
                    lg.record_payment(conn, rid, f, t, amt)
                    notify(f"{fn} → {tn} ₹{amt:,.2f} recorded ✅")

        st.divider()
        st.subheader("Net Balances")
        st.caption("Positive amounts are owed to members; negative amounts are owed by members.")
        bal = lg.compute_balances(conn, rid)
        st.dataframe(pd.DataFrame([{"Member": b["name"], "Paid (₹)": b["paid"], "Share (₹)": b["share"],
                                    "Net Balance (₹)": b["net"]} for b in bal.values()]),
                     hide_index=True, use_container_width=True)

    # ---------------- Category Breakdown ----------------
    with right_col.expander("📊 Category Breakdown", expanded=False):
        cats = lg.category_totals(conn, rid)
        if not cats:
            st.info("Add expenses to unlock interactive analytics.")
        else:
            try:
                import altair as alt

                dark_axis = dict(
                    labelColor="#cbd5e1",
                    titleColor="#f8fafc",
                    gridColor="rgba(168,85,247,0.16)",
                    domainColor="rgba(168,85,247,0.32)",
                )
                dark_legend = dict(labelColor="#e2e8f0", titleColor="#f8fafc")

                ch1, ch2 = st.container(), st.container()
                with ch1:
                    st.write("**Spending by Category (Hover to inspect)**")
                    cat_df = pd.DataFrame(cats)
                    donut = (
                        alt.Chart(cat_df)
                        .mark_arc(innerRadius=58, outerRadius=115, cornerRadius=8, stroke="#050311", strokeWidth=2)
                        .encode(
                            theta=alt.Theta("total:Q", title="Total (₹)"),
                            color=alt.Color(
                                "category:N",
                                scale=alt.Scale(range=["#8b5cf6", "#38bdf8", "#ec4899", "#10b981", "#f59e0b", "#6366f1"]),
                                title="Category",
                            ),
                            tooltip=["category:N", alt.Tooltip("total:Q", format=",.2f", title="Amount (₹)")],
                        )
                        .properties(height=300)
                        .configure_view(strokeWidth=0)
                        .configure_legend(**dark_legend)
                        .configure(background="transparent")
                    )
                    st.altair_chart(donut, use_container_width=True)

                with ch2:
                    st.write("**Paid vs. Actual Share per Member**")
                    mem_rows = []
                    for b in bal.values():
                        mem_rows.append({"Member": b["name"], "Type": "Paid", "Amount": b["paid"]})
                        mem_rows.append({"Member": b["name"], "Type": "Share", "Amount": b["share"]})
                    bar = (
                        alt.Chart(pd.DataFrame(mem_rows))
                        .mark_bar(cornerRadiusTopLeft=7, cornerRadiusTopRight=7)
                        .encode(
                            x=alt.X("Member:N", title=""),
                            xOffset="Type:N",
                            y=alt.Y("Amount:Q", title="Amount (₹)"),
                            color=alt.Color("Type:N", scale=alt.Scale(range=["#38bdf8", "#8b5cf6"])),
                            tooltip=["Member:N", "Type:N", alt.Tooltip("Amount:Q", format=",.2f", title="₹")],
                        )
                        .properties(height=300)
                        .configure_view(strokeWidth=0)
                        .configure_axis(**dark_axis)
                        .configure_legend(**dark_legend)
                        .configure(background="transparent")
                    )
                    st.altair_chart(bar, use_container_width=True)

                months = lg.month_totals(conn, rid)
                if months:
                    st.write("**Monthly Spend Report**")
                    mchart = (
                        alt.Chart(pd.DataFrame(months))
                        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color="#ec4899")
                        .encode(
                            x=alt.X("month:N", title="Month"),
                            y=alt.Y("total:Q", title="Total (₹)"),
                            tooltip=["month:N", alt.Tooltip("total:Q", format=",.2f", title="Total (₹)")],
                        )
                        .properties(height=240)
                        .configure_view(strokeWidth=0)
                        .configure_axis(**dark_axis)
                        .configure(background="transparent")
                    )
                    st.altair_chart(mchart, use_container_width=True)
            except Exception:
                st.write("**Spending by category**")
                st.bar_chart(pd.DataFrame(cats).set_index("category"))
                st.write("**Monthly report**")
                st.bar_chart(pd.DataFrame(lg.month_totals(conn, rid)).set_index("month"))

    # ---------------- History ----------------
    with right_col.expander("📜 History", expanded=False):
        rows = lg.list_expenses(conn, rid)
        if not rows:
            st.info("No expenses yet.")
        else:
            st.dataframe(pd.DataFrame(rows).rename(columns={
                "id": "ID", "date": "Date", "description": "Description", "category": "Category",
                "payer": "Paid By", "amount": "Amount (₹)"}), hide_index=True, use_container_width=True)
            labels2 = {f"#{r['id']} | {r['date']} | {r['description']} | ₹{r['amount']} ({r['payer']})": r["id"]
                       for r in rows}
            pick2 = st.selectbox("Select an expense to delete", list(labels2.keys()), key=f"del_{rid}")
            if st.button("🗑️ Delete Expense"):
                lg.delete_expense(conn, rid, labels2[pick2])
                notify("Expense deleted.")
        pays = lg.list_payments(conn, rid)
        if pays:
            st.write("**Recorded Settlements**")
            st.dataframe(pd.DataFrame(pays).rename(columns={
                "date": "Date", "payer": "From", "receiver": "To", "amount": "Amount (₹)"}),
                hide_index=True, use_container_width=True)

    # ---------------- Close Room (Host Only) ----------------
    if is_host:
        with right_col.expander("⚙️ Room Administration", expanded=False):
            st.write("Close this room once every balance is settled.")
            st.caption("Everyone keeps a short summary in My History. Detailed room bills are wiped.")
            bal = lg.compute_balances(conn, rid)
            if lg.settle_plan({m: b["net"] for m, b in bal.items()}):
                st.warning("Some payments are still pending. Settle everything first in Settlements.")
            else:
                ok = st.checkbox("Yes, close this room and delete its data", key=f"close_ok_{rid}")
                if st.button("Close Room & Save History"):
                    if ok:
                        done, msg = lg.close_room(conn, rid, uid)
                        if done:
                            notify(msg, balloons=True)
                        else:
                            st.error(msg)
                    else:
                        st.error("Tick the box first to confirm.")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
uid = st.session_state.get("uid")
user = lg.get_user(conn, uid) if uid else None

if not user:
    auth_screen()
else:
    st.title("Smart Expense Splitter")
    st.sidebar.markdown(f"### 👋 Hi, {user['display_name']}")
    st.sidebar.markdown(
        '<div class="sec-badge" style="margin-top:4px;"><span class="live-dot"></span> Vault Encrypted</div>',
        unsafe_allow_html=True,
    )
    page = st.sidebar.radio("Navigation", ["🏠 My Rooms", "🔐 Profile & UPI Vault", "📜 My History"])
    if st.sidebar.button("Logout"):
        st.session_state.pop("uid", None)
        st.rerun()

    if page.startswith("🏠"):
        page_rooms(user)
    elif page.startswith("🔐"):
        page_profile(user)
    else:
        page_history(user)