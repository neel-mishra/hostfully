### Campaign Overview
This 3-step cold email sequence targets VPs of Marketing at B2B SaaS companies. The core hypothesis is that recent growth (often indicated by a hiring spree) leads to challenges in efficiently scaling marketing channels and managing lead acquisition costs. The sequence aims to agitate this pain, introduce TLDR as a high-ROI solution for reaching technical audiences, and provide social proof, all while maintaining a concise, direct, and non-salesy tone.

### Clay AI Enrichment Prompt (For First Line Generation)
```prompt
Analyze the LinkedIn profile and recent news of [Prospect Company].
1.  **Objective:** Generate a highly personalized, concise opening sentence (under 15 words) for a cold email to the VP of Marketing.
2.  **Primary Research:** Look for indications of rapid company growth or significant expansion of the marketing/growth team within the last 6-12 months (e.g., 3+ new hires in demand gen, performance marketing, growth, or similar roles; recent large funding rounds; major product launches indicating scale).
3.  **Conditional Output:**
    *   **If rapid growth/hiring spree is evident:** Craft a sentence that congratulates them on this growth and subtly alludes to the challenge of scaling marketing efficiently or maintaining channel performance.
        *   Example output: "Great to see [Company Name]'s growth. Scaling marketing efficiently?"
        *   Example output: "Impressive marketing team expansion! Keeping lead costs low?"
    *   **If no clear rapid growth/hiring spree is evident:** Craft a sentence that addresses a common, high-level challenge for B2B SaaS VPs of Marketing focused on technical audiences regarding efficient customer acquisition channels.
        *   Example output: "Finding high-ROI channels for [Company Name] is tough, right?"
        *   Example output: "Optimizing tech audience acquisition a priority at [Company Name]?"
4.  **Format:** Output ONLY the generated sentence, with no additional commentary. Ensure it flows naturally into an email that discusses challenges with rising CPCs on platforms like LinkedIn.
```

### Email 1
Subject: scaling [company_name] marketing

[clay_generated_first_line]
(e.g., "great to see [company_name]'s growth. scaling marketing efficiently?")
many vps like you find it tough for technical audiences, especially with linkedin cpcs rising.
we help b2b saas companies get qualified tech leads at half the cost.
is optimizing acquisition on your radar?

### Email 2
Subject: re: scaling [company_name] marketing

following up on my note below.
delve drove $1m in attributed pipeline with tldr, at a 52x roi.
we reach 7m tech professionals where they pay attention, outperforming paid social for them.
worth a 5-minute look at our case studies?

### Email 3
Subject: closing the loop

no worries if this isn't a priority, but i wanted to try one last time.
our ads place your message natively in newsletters read by 7m tech pros, with a 48% open rate.
it's why companies like plaid saw $382k in pipeline.
if it makes sense, just reply 'learn more'. if not, no worries at all.