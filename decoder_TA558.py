import re
import base64

# Load the file
with open("image.jpg", "rb") as f: #change "image.jpg" with your image name or path
    data = f.read().decode(errors="ignore")  # Decode

# Extract the malware in base64 using RegEx
match = re.search(r"<<BASE64_START>>(.*?)<<BASE64_END>>", data, re.DOTALL)
if match:
    base64_string = match.group(1).strip()
    decoded_data = base64.b64decode(base64_string)
    
    # Save the raw output. You should see the magic number "MZ" with HxD
    with open("output.bin", "wb") as out:
        out.write(decoded_data)
    
    print("malware decoded! Saved in output.bin")
else:
    print("No payload found :(")
