import streamlit as st
import phonenumbers
from phonenumbers import carrier, geocoder, timezone, PhoneNumberType
import json
import re
import random

# Initialize session state
if 'phone_data' not in st.session_state:
    st.session_state.phone_data = [
        {"phoneNumber": "+1234567890", "name": "John Doe", "carrier": "Verizon", "city": "New York", "country": "United States", "spamScore": 0.2},
        {"phoneNumber": "+919876543210", "name": "Priya Sharma", "carrier": "Airtel", "city": "Delhi", "country": "India", "spamScore": 0.5}
    ]
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Parse phone number with advanced features
def parse_phone_number(phone_number):
    try:
        parsed = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed):
            reasons = []
            if not phonenumbers.is_possible_number(parsed):
                reasons.append("Number is not possible (e.g., wrong length).")
            if not phonenumbers.is_valid_number_for_region(parsed, parsed.country_code):
                reasons.append("Number is invalid for the detected region.")
            return None, f"Invalid phone number: {', '.join(reasons)}"
        
        country = geocoder.description_for_number(parsed, "en") or "Unknown"
        # Attempt to get city, avoiding country duplication
        city = geocoder.description_for_number(parsed, "en", region="city") or "Unknown"
        if city == country:
            city = "Unknown"
        carrier_name = carrier.name_for_number(parsed, "en") or "Unknown"
        tz = timezone.time_zones_for_number(parsed)[0] if timezone.time_zones_for_number(parsed) else "Unknown"
        
        # Number type
        number_type = phonenumbers.number_type(parsed)
        type_map = {
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE: "Fixed Line",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
            PhoneNumberType.TOLL_FREE: "Toll-Free",
            PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            PhoneNumberType.SHARED_COST: "Shared Cost",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            PhoneNumberType.PAGER: "Pager",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.VOICEMAIL: "Voicemail",
            PhoneNumberType.UNKNOWN: "Unknown"
        }
        number_type_str = type_map.get(number_type, "Unknown")
        
        # Format numbers
        national_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        international_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        
        # Enhanced spam score calculation
        raw_number = str(parsed.national_number)
        spam_score = 0.0
        # Repetitive digits (e.g., 1111)
        if re.search(r"(\d)\1{3,}", raw_number):
            spam_score += 0.3
        # Sequential digits (e.g., 1234 or 4321)
        if re.search(r"1234|4321|0123|9876|6789", raw_number):
            spam_score += 0.2
        # Short number
        if len(raw_number) < 7:
            spam_score += 0.2
        # Suspicious number types
        if number_type in [PhoneNumberType.PREMIUM_RATE, PhoneNumberType.TOLL_FREE, PhoneNumberType.SHARED_COST]:
            spam_score += 0.3
        # Add slight random variation to simulate external data
        spam_score += random.uniform(0.0, 0.1)
        spam_score = min(round(spam_score, 2), 1.0)
        
        return parsed, {
            "country": country,
            "city": city,
            "carrier": carrier_name,
            "timezone": tz,
            "number_type": number_type_str,
            "national_format": national_format,
            "international_format": international_format,
            "spam_score": spam_score
        }
    except phonenumbers.NumberParseException:
        return None, "Error parsing phone number. Ensure correct format (e.g., +1234567890)."

# Streamlit app
st.title("PhoneFinder - Advanced Phone Number Lookup")
st.markdown("Search for detailed phone number information or contribute to our database. All data is stored in-memory for privacy.")

# Phone Number Lookup Section
st.header("Search Phone Number")
phone_number = st.text_input("Enter phone number (e.g., +1234567890)", key="phone_input")

if st.button("Search"):
    if phone_number:
        parsed, result = parse_phone_number(phone_number)
        if not parsed:
            st.error(result)
        else:
            phone_data = st.session_state.phone_data
            found = next((entry for entry in phone_data if entry["phoneNumber"] == phone_number), None)
            parsed_result = parse_phone_number(phone_number)[1]  # Recalculate for fresh spam score
            if found:
                # Update existing entry with fresh data
                result = found
                result.update({
                    "carrier": parsed_result["carrier"],
                    "city": parsed_result["city"],
                    "country": parsed_result["country"],
                    "timezone": parsed_result["timezone"],
                    "number_type": parsed_result["number_type"],
                    "national_format": parsed_result["national_format"],
                    "international_format": parsed_result["international_format"],
                    "spam_score": parsed_result["spam_score"]
                })
            else:
                result = {
                    "phoneNumber": phone_number,
                    "name": "Unknown (Contribute to add name)",
                    "carrier": parsed_result["carrier"],
                    "city": parsed_result["city"],
                    "country": parsed_result["country"],
                    "timezone": parsed_result["timezone"],
                    "number_type": parsed_result["number_type"],
                    "national_format": parsed_result["national_format"],
                    "international_format": parsed_result["international_format"],
                    "spam_score": parsed_result["spam_score"]
                }
                st.session_state.phone_data.append(result)
            
            # Add to search history
            st.session_state.search_history.append(result)
            
            st.subheader("Search Results")
            st.write(f"**Phone Number:** {result['phoneNumber']}")
            st.write(f"**International Format:** {result['international_format']}")
            st.write(f"**National Format:** {result['national_format']}")
            st.write(f"**Name:** {result['name']}")
            st.write(f"**Carrier:** {result['carrier']}")
            st.write(f"**City:** {result['city']}")
            st.write(f"**Country:** {result['country']}")
            st.write(f"**Timezone:** {result['timezone']}")
            st.write(f"**Number Type:** {result['number_type']}")
            st.write(f"**Spam Score:** {result['spam_score']} (0 = low, 1 = high)")
            if result['spam_score'] >= 0.7:
                st.warning("High spam score detected! This number may be associated with spam or scam activities.")
            
            # Download results as JSON
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="Download Results as JSON",
                data=json_str,
                file_name=f"phone_lookup_{phone_number}.json",
                mime="application/json"
            )
    else:
        st.error("Please enter a phone number.")

# Contribute Data Section
st.header("Contribute Phone Number Data")
with st.form(key="contribute_form"):
    contribute_phone = st.text_input("Phone number (e.g., +1234567890)", key="contribute_phone")
    name = st.text_input("Name (optional)", key="contribute_name")
    city = st.text_input("City (optional)", key="contribute_city")
    carrier_input = st.text_input("Carrier (e.g., Airtel)", key="contribute_carrier")
    submit_button = st.form_submit_button("Submit Data")

    if submit_button:
        if contribute_phone and carrier_input:
            parsed, result = parse_phone_number(contribute_phone)
            if not parsed:
                st.error(result)
            else:
                phone_data = st.session_state.phone_data
                new_entry = {
                    "phoneNumber": contribute_phone,
                    "name": name if name else "Unknown",
                    "carrier": carrier_input,
                    "city": city if city else result["city"],
                    "country": result["country"],
                    "timezone": result["timezone"],
                    "number_type": result["number_type"],
                    "national_format": result["national_format"],
                    "international_format": result["international_format"],
                    "spam_score": result["spam_score"]
                }
                # Update existing entry or append new one
                existing_index = next((i for i, entry in enumerate(phone_data) if entry["phoneNumber"] == contribute_phone), -1)
                if existing_index >= 0:
                    phone_data[existing_index] = new_entry
                else:
                    phone_data.append(new_entry)
                st.session_state.phone_data = phone_data
                st.success("Data submitted successfully!")
        else:
            st.error("Phone number and carrier are required fields.")

# Search History Section
st.header("Your Search History")
if st.session_state.search_history:
    for i, entry in enumerate(reversed(st.session_state.search_history)):
        with st.expander(f"Search {len(st.session_state.search_history) - i}: {entry['phoneNumber']}"):
            st.write(f"**International Format:** {entry['international_format']}")
            st.write(f"**National Format:** {entry['national_format']}")
            st.write(f"**Name:** {entry['name']}")
            st.write(f"**Carrier:** {entry['carrier']}")
            st.write(f"**City:** {entry['city']}")
            st.write(f"**Country:** {entry['country']}")
            st.write(f"**Timezone:** {entry['timezone']}")
            st.write(f"**Number Type:** {entry['number_type']}")
            st.write(f"**Spam Score:** {entry['spam_score']}")
            if entry['spam_score'] >= 0.7:
                st.warning("High spam score detected!")
else:
    st.write("No search history yet.")

# Footer
st.markdown("---")
st.markdown(
    "Developed by Lav Kush | "
    "[Portfolio](https://lav-developer.netlify.app)",
    unsafe_allow_html=True
)