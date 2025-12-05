# llm_log_filter.awk
# Print only lines that look like JSON with possible prompt-injection label
/index.*possible_prompt_injection/ {
    print "[SUSPICIOUS] " $0
}

/LAB-REDTEAM-TEST/ {
    print "[LAB-REDTEAM] " $0
}

