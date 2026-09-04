import streamlit as st

# Configure the page
st.set_page_config(page_title="Night Shift Protein Tracker", page_icon="💪")
st.title("Night Shift Protein & Recovery Tracker")

# Set targets based on your 67kg (148lbs) weight
MIN_TARGET = 107
MAX_TARGET = 147

st.write(f"**Your Daily Target:** {MIN_TARGET}g to {MAX_TARGET}g of protein")

# Helper function to estimate protein based on food descriptions
def estimate_protein(food_text):
    text = food_text.lower()
    
    # Simple keyword-based estimation logic for common night shift meals
    if not text:
        return 0
    elif "whey" in text or "protein powder" in text or "shake" in text:
        return 25
    elif "egg" in text:
        # Count numbers if mentioned, otherwise assume 2 eggs
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
        # Default baseline if text is entered but doesn't match specific high-protein keywords
        return 15

# Create text input fields for your specific schedule
st.subheader("Log What You're Eating")
dinner_desc = st.text_input("6:00 PM Dinner (e.g., Rice with chicken)", value="Rice with chicken")
snack_desc = st.text_input("10:00 PM Snack (e.g., 2 eggs)", value="2 eggs")
pre_workout_desc = st.text_input("4:00 AM Pre-workout (e.g., Rice with pork)", value="Rice with pork")
post_workout_desc = st.text_input("Post-workout Supplement (e.g., Whey protein shake)", value="Whey protein shake")

# Automatically calculate protein based on descriptions
dinner = estimate_protein(dinner_desc)
snack = estimate_protein(snack_desc)
pre_workout = estimate_protein(pre_workout_desc)
post_workout = estimate_protein(post_workout_desc)

# Show the estimated breakdown to the user
st.subheader("Estimated Protein Breakdown")
st.write(f"- **6:00 PM Dinner:** ~{dinner}g protein")
st.write(f"- **10:00 PM Snack:** ~{snack}g protein")
st.write(f"- **4:00 AM Pre-workout:** ~{pre_workout}g protein")
st.write(f"- **Post-workout:** ~{post_workout}g protein")

# Calculate the total
total_protein = dinner + snack + pre_workout + post_workout

# Display the progress bar
st.subheader("Daily Progress")
progress_ratio = min(total_protein / MAX_TARGET, 1.0)
st.progress(progress_ratio)

st.write(f"**Current Total:** ~{total_protein}g")

# Dynamic Assistant Feedback
st.subheader("💡 Assistant Feedback")

if total_protein < MIN_TARGET:
    shortfall = MIN_TARGET - total_protein
    st.warning(f"You are roughly {shortfall}g short of your minimum muscle-building target. Try typing a larger meat portion or adding another egg.")
elif MIN_TARGET <= total_protein <= MAX_TARGET:
    st.success("Perfect! Your estimated intake hits your optimal protein window for muscle growth and recovery. Keep it up!")
else:
    st.info("You are above your maximum optimal target. You are very well-fueled for recovery!")

