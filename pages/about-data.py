import streamlit as st
from pages.sidebar import load_sidebar  # Import the sidebar function
load_sidebar()
## Show in webpage
st.header("About Data")

st.markdown("""
            
Last Update of the Dataset: 24 February 2025 <br>
Data Source: X Community Notes, 2021-2025, available to public at: https://x.com/i/communitynotes/download-data <br>

 ### Introduction
Community Notes, formerly known as Birdwatch since the program’s inception on 1/28/21, is a crowd-sourced content moderation feature on X (formerly Twitter) that allows users to add context and fact-checks to potentially misleading posts [1]. Launched in 2021, this system employs a unique bridging-based algorithm that prioritizes agreement between contributors with diverse perspectives, rather than relying on majority rule [2]. By May 2024, the program had more than 500 thousand contributors, with notes being viewed billions of times [3]. The feature has been applied to a wide range of content, including posts by government accounts, politicians, and even X's owner, Elon Musk [4]. 

While Community Notes has shown promise in combating misinformation, with a study finding COVID-19 vaccine notes to be accurate 96% of the time [5], it has also faced criticism for potential vulnerabilities to manipulation and inconsistent application. Despite these challenges, the open-source nature of the algorithm and the transparency of the data have made Community Notes an intriguing subject for researchers studying bias, misinformation diffusion, and the effectiveness of collaborative fact-checking systems [6,7,8].
Understanding the main themes and narratives within large-scale textual data is crucial for gaining insights into public discourse and dynamics. 

            
### Preprocessing for the German data:
The data has been preprocessed to ensure consistency and facilitate analysis. <br>
The following steps were applied to the ‘summary’ column from downloaded X data (downloaded February 26, 2025) and saved in a ‘cleaned_summary’ column:<br>

1. Convert to lowercase <br>
2. Standardize accent characters (ä → ae, ö → oe, ü → ue, ß → ss) <br>
3. Remove URLs <br>
4. Expand contractions (e.g., "am" → "an dem", "ins" → "in das") <br>
5. Remove mentions (@) and hashtags (#) <br>
6. Keep only alphabetic characters (optionally preserve hyphens in compound words) <br>
7. Remove stopwords and very short words (2 letters and less) <br>
8. Lemmatization using a German-specific lemmatizer <br>
        
### Preprocessing for the English data: 

1. Convert to lowercase <br>
2. Decode HTML <br>
3. Standardize accent characters (résumé → resume, jalapeño → jalapeno) <br>
4. Remove URLs <br>
5. Expand Contractions (can’t → cannot, I’m → I am ) <br>
6. Remove mentions (@) and hashtags (#) <br>
7. Keep only alphabetic characters <br>
8. Remove stopwords and very short words (2 letters and less) <br>
9. Lemmatization using a English-specific lemmatizer <br>
       

### Citations:
[1] X: Introduction to Community Notes, x.com. Available at: https://communitynotes.x.com/guide/en/about/introduction (Accessed: 07 February 2025).  <br>
[2] Buterin, V. (2023) What do I think about community notes?, Vitalik Buterin’s website. Available at: https://vitalik.eth.limo/general/2023/08/16/communitynotes.html (Accessed: 07 February 2025). <br>
[3] X (2024) Powered by the People. Available at: https://x.com/CommunityNotes/status/1788617818784792880 (Accessed: 07 February 2025). <br>
[4] Musk, E. (2024) X.com, X (formerly Twitter). Available at: https://x.com/elonmusk/status/1859695994688110819 (Accessed: 07 February 2025). <br>
[5] Allen, M. R., Desai, N., Namazi, A., Leas, E., Dredze, M., Smith, D. M., & Ayers, J. W. (2024). Characteristics of X (Formerly Twitter) Community Notes Addressing COVID-19 Vaccine Misinformation. JAMA. <br>
[6] Wang, C., & Lucas, P. (2024). Efficiency of Community-Based Content Moderation Mechanisms: A Discussion Focused on Birdwatch. Group Decision and Negotiation, 33(3), 673-709. <br>
[7] Allen, J., Martel, C., & Rand, D. G. (2022, April). Birds of a feather don’t fact-check each other: Partisanship and the evaluation of news in Twitter’s Birdwatch crowdsourced fact-checking program. In Proceedings of the 2022 CHI conference on human factors in computing systems (pp. 1-19). <br>
[8] Chuai, Y., Tian, H., Pröllochs, N., & Lenzini, G. (2023). The roll-out of community notes did not reduce engagement with misinformation on Twitter. arXiv preprint arXiv:2307.07960. <br>
""", unsafe_allow_html=True)
