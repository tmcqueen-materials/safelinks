# Safelinks
Microsoft safelinks purport to make email safer by replacing links to ones that redirect via microsoft cloud services to stop access if the location is identified as malicious. While there is some success, the link obfuscation comes at two measurable costs: (1) that it engenders more blind trust in links, which results in riskier behavior outside the closed email ecosystem; and (2) it hides key actionable information from informed users. Further, safelinks are often unknown to third parties and results in great confusion for those individuals not using Microsoft tools, in addition to the obvious privacy risks associated with a single point (Microsoft) knowing all links accessed by an individual.

This respository provides a python tool that strips the safelink wrapping and restores the original link. It is primarily designed to run automatically as part of a filter chain in getmail. It can be used in a stand-alone fashion to remove safelinks from messages.

Compared to existing tools I'm aware of [1,2], this version does not require any modules beyond those part of the python3 core, and correctly handles various encodings and multipart messages. It is also more privacy-preserving than web-based alternatives [3]. It is roughly equivalent to the Outlook extension [outlook_unsafelink](https://github.com/Dunky13/outlook_unsafelink) and the Thunderbird equivalents [4,5].

# Usage
## Getmail
1. Download [strip_safelinks.py](https://github.com/tmcqueen-materials/safelinks/blob/main/strip_safelinks.py) to your home directory
2. Add a filter to your `.getmailrc` file:
```
[filter-1]
type = Filter_external
path = ~/strip_safelinks.py
ignore_stderr = true
```

# Related Resources
1. https://github.com/coingraham/safelinks_stripper
1. https://github.com/j3rd2020/urlstripscan
1. http://www.o365atp.com/
1. https://addons.thunderbird.net/en-US/thunderbird/addon/safelink-removal
1. https://addons.thunderbird.net/en-US/thunderbird/addon/unmangle-outlook-safelinks
