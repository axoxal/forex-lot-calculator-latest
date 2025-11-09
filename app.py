import streamlit as st

st.set_page_config(page_title="Forex & Gold Lot Size Calculator", layout="centered")

st.title("📊 Forex & Gold Lot Size Calculator")

# -----------------------
# Input Section
# -----------------------
col1, col2 = st.columns(2)

with col1:
    account_currency = st.selectbox("Account Currency", ["USD", "INR"])
    pair = st.selectbox("Trading Pair", ["XAUUSD (Gold)", "EURUSD", "GBPUSD", "USDJPY", "US30", "Custom"])

with col2:
    account_size = st.number_input("Account Size", min_value=1.0, format="%.2f")
    risk_percent = st.number_input("Risk per Trade ( % )", min_value=0.1, max_value=100.0, value=1.0)

st.subheader("📍 Trade Setup")

entry_price = st.number_input("Entry Price", format="%.5f")
sl_price = st.number_input("Stop Loss Price", format="%.5f")

# -----------------------
# Multiple Accounts
# -----------------------
st.subheader("💰 Multiple Accounts (Optional)")
col3, col4 = st.columns(2)

with col3:
    account1_risk = st.number_input("Risk Amount Account 1 (USD/INR)", min_value=0.0, value=0.0, format="%.2f")

with col4:
    account2_risk = st.number_input("Risk Amount Account 2 (USD/INR)", min_value=0.0, value=0.0, format="%.2f")


# -----------------------
# Calculation Function
# -----------------------
def calculate_lot_size(entry, sl, risk_amount, pair):
    sl_distance = abs(entry - sl)

    if sl_distance == 0:
        return None, None, None

    if pair == "XAUUSD (Gold)":
        pip_value_per_lot = 1             # $1 per 0.01 move
        pip_distance = sl_distance / 0.10 # $1 = 0.10 distance
    else:
        pip_value_per_lot = 10            # $10 per pip (standard pairs)
        pip_distance = sl_distance / 0.0001

    lot_size = risk_amount / (pip_distance * pip_value_per_lot)

    return lot_size, pip_distance, pip_value_per_lot


# -----------------------
# Results Section
# -----------------------
if st.button("✅ Calculate Lot Size"):

    calculated_risk = (risk_percent / 100) * account_size

    lot_size_1, pips_1, val1 = calculate_lot_size(
        entry_price, sl_price,
        account1_risk if account1_risk > 0 else calculated_risk,
        pair
    )

    lot_size_2, pips_2, val2 = calculate_lot_size(entry_price, sl_price, account2_risk, pair)

    st.subheader("📈 Results")

    # --- Account 1 ---
    if lot_size_1:
        st.success(
            f"**Account 1 Lot Size:** `{lot_size_1:.2f}` lots\n"
            f"SL Distance: `{pips_1:.1f}` pips\n"
            f"Risk Amount Used: `{account1_risk if account1_risk > 0 else calculated_risk:.2f} {account_currency}`"
        )

    # --- Account 2 ---
    if lot_size_2 and account2_risk > 0:
        st.info(
            f"**Account 2 Lot Size:** `{lot_size_2:.2f}` lots\n"
            f"SL Distance: `{pips_2:.1f}` pips\n"
            f"Risk Amount Used: `{account2_risk:.2f} {account_currency}`"
        )

    if not lot_size_1 and not lot_size_2:
        st.error("❌ Invalid Entry or Stop Loss. Check your inputs.")


# -----------------------
# Footer / Branding
# -----------------------
st.write("---")
st.markdown(
    """
    <div style="text-align:center; font-size:14px;">
        🚀 <b>Developed by Aromal</b> — Smart Risk Management Tool for Prop Trading <br>
        Built using <b>Streamlit + Python</b>
    </div>
    """,
    unsafe_allow_html=True
)

