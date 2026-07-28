#!/usr/bin/env python
"""Edit toobey-network index.html - add mobile hamburger menu."""

import re

path = r'D:\Hermes生成\文化\tn_tmp\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the mobile .nav-links{display:none} and add hamburger + dropdown styles
# Find @media(max-width:768px){ ... }
media_pattern = r'(@media\s*\(max-width:\s*768px\)\s*\{)(.*?)(\})'
media_match = re.search(media_pattern, content, re.DOTALL)

if not media_match:
    print("ERROR: Could not find @media block")
    exit(1)

old_block = media_match.group(2)
print(f"Found @media block, {len(old_block)} chars")

# Replace .nav-links{display:none} and related styles inside the media block
new_mobile_styles = '''
.hamburger{display:flex}
.nav-links{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(15,23,42,.97);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);flex-direction:column;align-items:center;justify-content:center;gap:24px;z-index:1000}
.nav-links.mobile-open{display:flex}
.nav-links a{font-size:16px!important;color:rgba(255,255,255,.85)!important}
.nav-links a.nav-btn-new{padding:10px 40px!important;border-color:rgba(255,255,255,.3)!important}
.btn-primary{display:none!important}
'''

# Replace the old block content
# But keep the .nav-links{display:none} only once (not duplicated)
old_lines = old_block.split('\n')
new_lines = []
seen_nav_hide = False
for line in old_lines:
    stripped = line.strip()
    if '.nav-links{display:none}' in stripped and not seen_nav_hide:
        # Replace with new styles
        new_lines.append('')
        for ns in new_mobile_styles.split('\n'):
            ns = ns.strip()
            if ns:
                new_lines.append(ns)
        seen_nav_hide = True
    elif '.nav-links{display:none}' in stripped and seen_nav_hide:
        # Skip duplicate
        pass
    else:
        new_lines.append(line)

new_block = '\n'.join(new_lines)
new_content = content.replace(old_block, new_block)

# 2. Add JavaScript toggle function before the closing </script>
# Find the last </script> tag
js_toggle = '''

// Mobile hamburger menu toggle
(function(){
  var hamburger = document.getElementById('hamburger');
  var navLinks = document.querySelector('.nav-links');
  if(!hamburger || !navLinks) return;
  hamburger.addEventListener('click', function(){
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('mobile-open');
  });
  // Close menu when clicking a link
  navLinks.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){
      hamburger.classList.remove('active');
      navLinks.classList.remove('mobile-open');
    });
  });
})();

'''

# Find the last </script> tag
last_script_close = content.rfind('</script>')
if last_script_close > 0:
    # Insert before it
    insert_pos = content.rfind('\n', 0, last_script_close) + 1
    new_content = new_content[:insert_pos] + js_toggle + new_content[insert_pos:]
    print("JS toggle function added ✓")
else:
    print("ERROR: Could not find </script>")

# Also need to remove the .btn-primary{display:none!important} from the old .nav-links{display:none} line
# since we already replaced it above in the first occurrence

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"File written ({len(new_content)} bytes)")
print("Done!")
