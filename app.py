import streamlit as st

# Configure the page with Dark Mode iOS aesthetic matching the design
st.set_page_config(
    page_title="Kalo Protein Tracker", 
    page_icon="⚡",
    layout="centered"
)

# Custom CSS for high-end iOS dark fitness app aesthetic (OLED Black, Lime Accents, Rounded Cards)
st.markdown("""
<style>
    /* Global app background - Pure OLED Black */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Hide default streamlit header/footer branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* iOS Dark Mode grouped cards style */
    .kalo-card {
        background-color: #161618;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #26262a;
        margin-bottom: 16px;
        color: #ffffff;
    }
    
    /* Typography */
    .app-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0px;
    }
    .app-subtitle {
        font-size: 14px;
        color: #8e8e93;
        margin-top: 4px;
        margin-bottom: 20px;
    }
    
    /* Pill button style */
    .pill-active {
        background-color: #bcf833;
        color: #000000;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
        text-align: center;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff !important;
    }
    .metric-label {
        font-size: 12px;
        color: #8e8e93 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Ensure all markdown/text elements inside containers match */
    .stMarkdown p, .stMarkdown span, label {
        color: #ffffff !important;
    }
    
    /* Streamlit progress bar override for lime green fill */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #bcf833;
    }
</style>
""", unsafe_allow_html=True)

# App Header (Kalo-inspired top bar)
col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
with col_h1:
    st.markdown('<div class="app-title">⚡ Kalo</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown('<div style="text-align: right; color: #bcf833; font-weight: 600; padding-top: 6px;">🔥 7</div>', unsafe_allow_html=True)
with col_h3:
    st.markdown('<div style="text-align: right; color: #8e8e93; font-weight: 600; padding-top: 6px;">👤</div>', unsafe_allow_html=True)

st.markdown('<div class="app-subtitle">Small steps, big changes.</div>', unsafe_allow_html=True)

# Timeframe Selector Pills
cols_pill = st.columns(4)
with cols_pill[0]:
    st.markdown('<div class="pill-active">Week</div>', unsafe_allow_html=True)
with cols_pill[1]:
    st.markdown('<div style="text-align: center; color: #8e8e93; padding-top: 6px; font-size: 13px;">Month</div>', unsafe_allow_html=True)
with cols_pill[2]:
    st.markdown('<div style="text-align: center; color: #8e8e93; padding-top: 6px; font-size: 13px;">3 Months</div>', unsafe_allow_html=True)
with cols_pill[3]:
    st.markdown('<div style="text-align: center; color: #8e8e93; padding-top: 6px; font-size: 13px;">Year</div>', unsafe_allow_html=True)

st.write("")

# Set targets based on your 67kg (148lbs) weight
MIN_TARGET = 107
MAX_TARGET = 147

# Initialize session state for unlimited food entries
if "entries" not in st.session_state:
    st.session_state.entries = [
        {"food": "Rice with chicken", "protein": 25},
        {"food": "2 eggs", "protein": 12},
        {"food": "Rice with pork", "protein": 25},
        {"food": "Whey protein shake", "protein": 25}
    ]

# Helper function to estimate protein based on food description text
def estimate_protein(food_text):
    text = food_text.lower()
    if not text:
        return 0
    elif "whey" in text or "protein powder" in text or "shake" in text:
        return 25
    elif "egg" in text:
        if "4" in text: return 24
        if "3" in text: return 18
        if "1" in text: return 6
        return 12  # Default to 2 eggs
    elif "chicken" in text or "beef" in text or "pork" in text or "meat" in text:
        if "double" in text or "large" in text or "heavy" in text:
            return 40
        return 25  # Standard single serving portion
    elif "fish" in text or "tuna" in text:
        return 22
    else:
        return 15  # Baseline estimate for general items

# --- CARD 1: PROTEIN OVERVIEW ---
total_protein = sum(item["protein"] for item in st.session_state.entries)
progress_ratio = min(total_protein / MAX_TARGET, 1.0)
percentage = int((total_protein / MIN_TARGET) * 100)

st.markdown('<div class="kalo-card">', unsafe_allow_html=True)
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.markdown('<div class="metric-label">Protein Intake</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{total_protein} <span style="font-size: 14px; color: #8e8e93;">g avg</span></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div style="text-align: right; color: #bcf833; font-weight: 600; font-size: 14px; padding-top: 4px;">{percentage}% of target</div>', unsafe_allow_html=True)

st.write("")
st.progress(progress_ratio)

# Status message matching the card style
if total_protein < MIN_TARGET:
    shortfall = MIN_TARGET - total_protein
    st.markdown(f'<p style="color: #ff9f0a; font-size: 13px; margin-top: 8px;">⚠️ {shortfall}g short of minimum target ({MIN_TARGET}g)</p>', unsafe_allow_html=True)
elif MIN_TARGET <= total_protein <= MAX_TARGET:
    st.markdown('<p style="color: #bcf833; font-size: 13px; margin-top: 8px;">✨ Optimal muscle-building zone achieved!</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="color: #30d158; font-size: 13px; margin-top: 8px;">🚀 Supercharged protein intake today!</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# --- CARD 2: ADD FOOD ENTRY ---
st.markdown('<div class="kalo-card">', unsafe_allow_html=True)
st.markdown('<div style="font-weight: 600; margin-bottom: 10px; font-size: 15px;">Log Meal or Supplement</div>', unsafe_allow_html=True)

with st.form("add_form", clear_on_submit=True):
    new_food = st.text_input("What did you eat?", placeholder="e.g., Chicken breast, 3 eggs, Whey shake...")
    submitted = st.form_submit_button("Add Entry", use_container_width=True)
    
    if submitted and new_food:
        calculated_protein = estimate_protein(new_food)
        st.session_state.entries.append({"food": new_food, "protein": calculated_protein})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# --- CARD 3: TODAY'S LOGGED ITEMS ---
st.markdown('<div class="kalo-card">', unsafe_allow_html=True)
st.markdown('<div style="font-weight: 600; margin-bottom: 14px; font-size: 15px;">Today’s Log</div>', unsafe_allow_html=True)

if not st.session_state.entries:
    st.markdown('<p style="color: #8e8e93; font-size: 13px;">No food logged yet today.</p>', unsafe_allow_html=True)
else:
    for i, entry in enumerate(st.session_state.entries):
        cols = st.columns([5, 2, 1])
        with cols[0]:
            st.markdown(f'<span style="font-size: 14px;">{entry["food"]}</span>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f'<span style="color: #bcf833; font-weight: 600; font-size: 14px;">~{entry["protein"]}g</span>', unsafe_allow_html=True)
        with cols[2]:
            if st.button("✕", key=f"del_{i}"):
                st.session_state.entries.pop(i)
                st.rerun()
        if i < len(st.session_state.entries) - 1:
            st.markdown('<hr style="border: none; border-top: 1px solid #26262a; margin: 8px 0;">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
