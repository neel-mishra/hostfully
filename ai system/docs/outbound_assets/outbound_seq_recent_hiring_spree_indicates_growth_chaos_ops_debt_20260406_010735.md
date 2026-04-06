### Campaign Overview
This 3-step cold email sequence targets VPs of Marketing at B2B SaaS companies experiencing rapid growth. The core hypothesis is that fast hiring and expansion often lead to operational chaos or "ops debt" within marketing departments. The sequence aims to agitate this potential pain, provide social proof of a solution, and offer a low-friction path forward, all while maintaining an ultra-concise, conversational, and non-salesy tone with minimal capitalization.

### Clay AI Enrichment Prompt (For First Line Generation)
```prompt
You are an AI assistant designed to generate hyper-personalized opening lines for cold emails based on recent company growth or hiring activities.

**Input:**
- Prospect's Company Name: [COMPANY_NAME]
- Prospect's LinkedIn Profile URL: [PROSPECT_LINKEDIN_URL] (optional, but prioritize if available)

**Task:**
1.  **Search Strategy:**
    *   Prioritize recent (last 3-6 months) news, press releases, funding announcements, significant hiring sprees (especially in marketing/sales/product), and company growth milestones.
    *   Check the company's LinkedIn page for "Posts" or "About" sections mentioning growth.
    *   Look at the "News" or "Press" section on the company's official website.
    *   If LinkedIn profile is provided, check for recent updates related to team growth or company achievements the prospect might have shared.
2.  **Information Extraction:** Identify concrete evidence of growth (e.g., "raised Series B," "hired 50 new engineers," "expanded into EMEA," "opened new office," "added several new marketing roles").
3.  **Opening Line Generation Rules:**
    *   **Format:** A single, congratulatory or observant sentence.
    *   **Tone:** Friendly, non-intrusive, and directly related to the observed growth.
    *   **Length:** Max 15 words.
    *   **Capitalization:** Use minimal capitalization, mirroring conversational style (e.g., "i saw," "congrats").
    *   **Seamless Transition:** The line must naturally lead into the idea of growth bringing operational challenges (the email 1 hook).
    *   **Fallback:** If no recent growth information is found, generate a polite, general observation like "i saw [COMPANY_NAME] is doing some interesting work in [INDUSTRY]."

**Output Example if growth found:**
"i noticed [COMPANY_NAME] just announced their series b funding – huge news!"
"congrats on adding several new marketing roles recently, that's exciting!"
"i saw your team has been expanding rapidly, which is great to see!"

**Output Example if no specific growth found:**
"i saw [COMPANY_NAME] is doing some interesting work in [INDUSTRY]."
```

### Email 1
Subject: quick thought re: growth
[Personalized opening line from Clay AI], that's exciting!

that kind of growth often brings operational chaos for marketing teams, right? keeping everything aligned when scaling can get messy.

we help vps like you get ahead of that ops debt, turning chaos into clear pathways.

curious if any of this resonates with what you're seeing?

### Email 2
Subject: re: quick thought re: growth

just following up. i was thinking of [similar company name], a vp there faced similar scaling pains, especially with their content ops.

they managed to cut manual effort by 30% and boost engagement significantly within months, turning their growth into real gains.

might be worth a quick chat to see how they did it? no pressure either way.

### Email 3
Subject: last thought for [prospect name]

reaching out one last time. looks like my timing might be off, which is totally fine.

but if you ever hit a point where scaling marketing ops feels like untangling spaghetti, keep us in mind.

i can also send a quick 1-pager on how top saas vps tackle operational debt if that's more useful?