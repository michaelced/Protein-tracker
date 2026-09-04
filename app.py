import streamlit as st

# Configure the page with Dark Mode iOS aesthetic
st.set_page_config(
    page_title="Protein Tracker", 
    page_icon="⚡",
    layout="centered"
)

# Custom CSS for Dark iOS Theme (OLED Black background with dark gray cards and high contrast text)
st.markdown("""
<style>
    /* Global app background */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Hide default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* iOS Dark Mode grouped cards style */
    .ios-card {
        background-color: #1c1c1e;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        margin-bottom: 16px;
        color: #ffffff;
    }
    
    /* Ensure all card text, headers, and markdown are bright white and legible */
    .ios-card h3, .ios-card h4, .ios-card p, .ios-card span, .ios-card div {
        color: #ffffff !important;
    }
    
    .stMarkdown p, .stMarkdown span, label {
        color: #ffffff !important;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff !important;
    }
    .metric-label {
        font-size: 13px;
        color: #8e8e93 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("### Protein Tracker")
st.markdown("<p style='color: #8e8e93; margin-top: -15px;'>Log meals freely and monitor your daily goal</p>", unsafe_allow_html=True)

# Set targets based on your 67kg (148lbs) weight
MIN_TARGET = 107
MAX_TARGET = 147

# Initialize session state for unlimited entries
if "entries" not in st.session_state:
    st.session_state.entries = [
        {"food": "Rice with chicken", "protein": 25},
        {"food": "2 eggs", "protein": 12},
        {"food": "Rice with pork", "protein": 25},
        {"food": "Whey protein shake", "protein": 25}
    ]

# Helper function to estimate protein based on food text description
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

# --- SECTION 1: TODAY'S OVERVIEW ---
total_protein = sum(item["protein"] for item in st.session_state.entries)
progress_ratio = min(total_protein / MAX_TARGET, 1.0)

st.markdown('<div class="ios-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-label">Total Protein</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{total_protein}g</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-label">Target Range</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{MIN_TARGET}-{MAX_TARGET}g</div>', unsafe_allow_html=True)

st.write("")
st.progress(progress_ratio)

# Dynamic Feedback Message
if total_protein < MIN_TARGET:
    shortfall = MIN_TARGET - total_protein
    st.warning(f"You are roughly {shortfall}g short of your minimum muscle-building target.")
elif MIN_TARGET <= total_protein <= MAX_TARGET:
    st.success("You are right inside your optimal muscle growth window!")
else:
    st.info("You have exceeded your max target. Well fueled!")
st.markdown('</div>', unsafe_allow_html=True)


# --- SECTION 2: ADD NEW FOOD ENTRY ---
st.markdown('<div class="ios-card">', unsafe_allow_html=True)
st.markdown("#### Add Food Entry")

with st.form("add_form", clear_on_submit=True):
    new_food = st.text_input("What did you eat?", placeholder="e.g., Greek yogurt, Steak, Shake...")
    submitted = st.form_submit_button("Add to Log", use_container_width=True)
    
    if submitted and new_food:
        calculated_protein = estimate_protein(new_food)
        st.session_state.entries.append({"food": new_food, "protein": calculated_protein})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# --- SECTION 3: LOGGED ITEMS (UNLIMITED LIST WITH DELETE) ---
st.markdown('<div class="ios-card">', unsafe_allow_html=True)
st.markdown("#### Today's Log")

if not st.session_state.entries:
    st.write("No food logged yet today.")
else:
    for i, entry in enumerate(st.session_state.entries):
        cols = st.columns([4, 1, 1])
        with cols[0]:
            st.markdown(f"**{entry['food']}**")
        with cols[1]:
            st.markdown(f"~{entry['protein']}g")
        with cols[2]:
            if st.button("✕", key=f"del_{i}"):
                st.session_state.entries.pop(i)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
