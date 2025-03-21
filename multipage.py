import requests
import random
import time

# Google Form URL
form_url = "https://docs.google.com/forms/d/e/(id)/formResponse"

# Define the entries and their possible values
form_data_options = {
    "entry.1859276911": ["Under 18", "18 to 30", "31 to 50", "50+"],
    "entry.2081693768": ["Primary", "Secondary", "Tertiary (Pre-U, Diploma & Degree)", "Postgraduate"],
    "entry.310971995": ["Yes", "No"],
    "entry.2102277841": ["Television / Radio", "Internet (e.g. YouTube, articles)", 
                         "Education (e.g.,School / University)", "Word of mouth (Friends / Family)", 
                         "Never heard of geothermal emergy before"],
    "entry.1083296061": ["I have never heard of it before.", "I have heard of it but do not know how it works.", 
                         "I have a basic understanding of it.", "I have a good understanding of how it works.", 
                         "I am very knowledgeable about geothermal energy."],
    "entry.95430949": ["Generating Electricity", "Heating and cooling purposes", 
                       "Recreational uses (hot springs, natural saunas)", "I am not sure"],
    "entry.485322760": ["Yes"],
    "entry.1772408195": ["Hot springs", "Wind", "Sun", "Coal"],
    "entry.2030700350": ["Yes"],
    "entry.1482778588": ["Yes"],
    "entry.877807573": ["Environmental impact (e.g., impact on rural landscapes or natural reserves)", 
                        "Safety risks (e.g., accidents)", "Increased energy costs or infrastructure expenses", 
                        "Potential changes in land use (e.g., new power lines or substations being built around.)", 
                        "Reliability and accessibility of energy supply", 
                        "Where I'm staying may not have access to geothermal resources.", 
                        "I do not see any concerns with this."],
    "entry.1775937798": [str(i) for i in range(1, 6)],  # 1 to 5
    "entry.590269175": ["Coal", "Natural gas", "Hydropower", "Solar Energy", "Geothermal Energy", "Not sure"],
    "entry.2080102884": ["Yes"],
    "entry.1068638830": ["Yes"],
    "entry.1452812921": ["Lower energy costs", "Environmental benefits", "Government incentives", 
                         "Community initiatives", "Energy independence and security (reducing reliance on non-renewables)", 
                         "Technological innovation and modernisation", "Job creation and local economic growth", 
                         "Long-term cost savings", "Health and air quality improvement from reduced pollution"],
    "entry.332418379": ["Yes", "No", "Don't know"],
    "entry.725233898": ["Yes", "No"]
}

# Entries that allow multiple selections
multiple_choice_entries = ["entry.2102277841", "entry.1772408195", "entry.877807573", "entry.1452812921"]

# Function to generate random form data
def generate_random_form_data():
    form_data = {}
    for entry, options in form_data_options.items():
        if entry in multiple_choice_entries:
            num_choices = random.randint(1, len(options))
            form_data[entry] = random.sample(options, num_choices)
        else:
            form_data[entry] = random.choice(options)
    # Add pageHistory for 7 pages
    form_data["pageHistory"] = "0,1,2,3,4,5,6"
    return form_data

# Function to submit the form
def submit_form(form_data):
    payload = {}
    # Handle single-choice entries
    for key, value in form_data.items():
        if key not in multiple_choice_entries:
            payload[key] = value
        else:
            # Handle multiple-choice entries by adding each value as a separate key
            for val in value:
                if key in payload:
                    payload[key].append(val)  # Append to existing list if key exists
                else:
                    payload[key] = [val]  # Create new list if key doesn't exist

    # Display the values being sent
    print("\nValues being sent:")
    for key, value in form_data.items():
        if isinstance(value, list):
            print(f"{key}: {', '.join(value)}")
        else:
            print(f"{key}: {value}")
    
    # Send the form data
    response = requests.post(form_url, data=payload)
    if response.status_code == 200:
        print("\nForm submitted successfully!")
    else:
        print(f"\nFailed to submit form. Status code: {response.status_code}")

# Main loop to submit multiple random responses
def main():
    num_submissions = 150  # Number of random submissions (you can change this)
    for i in range(num_submissions):
        print(f"\nSubmitting form {i+1}/{num_submissions}...")
        form_data = generate_random_form_data()
        submit_form(form_data)
        time.sleep(1)  # Add delay to avoid overwhelming the server

if __name__ == "__main__":
    main()
