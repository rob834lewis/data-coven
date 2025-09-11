
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 07SEP2025

    Purpose         : Store all main imports in one place

    Dependencies    :

    Program name    : ecb_daily_rates

    Modifications
    -------------
    07SEP2025   RLEWIS  Initial Version
    11SEP2025   RLEWIS  Updated with common imports
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from globals          import *
from common.functions import upload_to_gcs, wdays, get_logger

# ---------------
# --- Logging ---
# ---------------

logger = get_logger("ecb_daily_rates")

# ----------------------
# --- Date Variables ---
# ----------------------

today = wdays().get("today")

# -----------------------
# --- Other Variables ---
# -----------------------

# bucket locations
raw_prefix     = "raw/exchange_rates/"     # Folder (prefix) in bucket for raw files
staging_prefix = "staging/exchange_rates/" # Folder for cleaned, intermediate CSV
output_prefix  = "output/exchange_rates/"  # Folder for final curated dataset
archive_prefix = "archive/exchange_rates/" # Folder for long-term storage of raw files

# ECB daily exchange rates XML feed
ecb_xml_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
ecb_xml_ns  = {'': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}  # XML namespace (ECB-specific)

# ------------
# --- Main ---
# ------------

logger.info("Starting ECB daily rates pipeline")

# ---
# Step 1: Fetch raw XML and store in raw/
# ---

resp = requests.get(ecb_xml_url)             # Call the ECB API to get the XML file
resp.raise_for_status()                      # Throw error if request failed (HTTP != 200)
raw_filename = f"ecb_rates_{today}.xml"      # Name of raw file

# Upload raw XML text directly into raw/ folder
upload_to_gcs(gcp_bucket, raw_prefix, raw_filename, resp.text)
logger.info(f"Raw stored: {raw_prefix}{raw_filename}")

# ---
# Step 2: Transform to staging CSV
# ---

root = ET.fromstring(resp.content)   # Parse the XML content

# Find the Cube node containing rates
cube = root.find('.//Cube/Cube', ecb_xml_ns)  
date = cube.get('time')  # Get the date attribute from the XML (e.g., '2025-09-05')

# Extract rates into dictionary: {"USD": 1.08, "GBP": 0.85, ...}
rates = {c.get('currency'): float(c.get('rate')) for c in cube.findall('Cube', ecb_xml_ns)}
rates['EUR'] = 1.0  # Add EUR as baseline = 1.0

# Build a DataFrame with one row containing all rates
df = pd.DataFrame([rates])
df.insert(0, 'date', date)  # Insert 'date' column at position 0

# Save cleaned CSV into staging/
staging_filename = f"ecb_rates_clean_{today}.csv"
upload_to_gcs(gcp_bucket, staging_prefix, staging_filename, df.to_csv(index=False))
logger.info(f"Staging stored: {staging_prefix}{staging_filename}")

# ---
# Step 3: Curate for output (select only EUR, GBP, USD)
# ---

final_df = df[['date', 'EUR', 'USD', 'GBP']]   # Keep only useful columns
final_filename = f"ecb_rates_final_{today}.csv"  # Output filename

# Save curated file into output/
upload_to_gcs(gcp_bucket, output_prefix, final_filename, final_df.to_csv(index=False))
logger.info(f"Output stored: {output_prefix}{final_filename}")

# ---
# Step 4: Archive raw file
# ---

# Re-upload the original raw XML into archive/ (for historical traceability)
upload_to_gcs(gcp_bucket, archive_prefix, raw_filename, resp.text)
logger.info(f"Archived: {archive_prefix}{raw_filename}")


"""
# Derive GBP & USD as base currencies
df['GBP_base_USD'] = df['USD'] / df['GBP']
df['USD_base_GBP'] = df['GBP'] / df['USD']

"""