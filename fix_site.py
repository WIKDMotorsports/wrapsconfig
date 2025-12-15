
import os

html_path = 'index.html'

with open(html_path, 'r') as f:
    content = f.read()

# 1. Replace all FFB700 with FF3B30
content = content.replace('#FFB700', '#FF3B30')

# 2. Update Preloader Logic
old_logic = """
                // Safety timeout: 5 seconds
                const timeoutPromise = new Promise(resolve => setTimeout(resolve, 5000));

                // Wait for all videos or timeout
                Promise.race([
                    Promise.all(uniqueUrls.map(loadVideo)),
                    timeoutPromise
                ]).then(() => {"""

new_logic = """
                // Safety timeout: 5 seconds
                const timeoutPromise = new Promise(resolve => setTimeout(resolve, 5000));

                // Minimum display time: 2.5 seconds (prevents flashing)
                const minTimePromise = new Promise(resolve => setTimeout(resolve, 2500));

                // Wait for (Videos loaded OR Timeout) AND Minimum Time
                Promise.all([
                    Promise.race([Promise.all(uniqueUrls.map(loadVideo)), timeoutPromise]),
                    minTimePromise
                ]).then(() => {"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
else:
    print("Warning: Could not find old preloader logic to replace.")
    # Fallback to finding the specific Promise.race block if formatting changed slightly
    # But since I just wrote it, it should match.
    pass

with open(html_path, 'w') as f:
    f.write(content)
