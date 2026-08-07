import re

files_to_fix = ['privacy.html', 'terms.html', 'security.html']

for filename in files_to_fix:
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # 1. Remove the rogue </script> tag before Smooth scroll for anchor links
        bad_script_block = """    </script>

        // Smooth scroll for anchor links"""
        good_script_block = """        // Smooth scroll for anchor links"""
        
        content = content.replace(bad_script_block, good_script_block)
        
        # 2. Fix the court location in terms.html
        if filename == 'terms.html':
            content = content.replace(
                "laws of the State of Delaware, without regard to its conflict of law provisions. Any legal action or proceeding arising under these Terms will be brought exclusively in the federal or state courts located in Delaware.",
                "laws of India, without regard to its conflict of law provisions. Any legal action or proceeding arising under these Terms will be brought exclusively in the courts located in Bangalore, India."
            )
            
        with open(filename, 'w') as f:
            f.write(content)
            
        print(f"Fixed {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

