{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import requests\
import re\
\
import streamlit as st
SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]
\
\
def serpapi_search(query):\
    params = \{\
        "engine": "google",\
        "q": query,\
        "api_key": SERPAPI_API_KEY,\
        "num": 5\
    \}\
    response = requests.get("https://serpapi.com/search", params=params)\
    response.raise_for_status()\
    data = response.json()\
    results = []\
    for result in data.get("organic_results", []):\
        results.append(\{"title": result.get("title"), "link": result.get("link"), "snippet": result.get("snippet")\})\
    return results\
\
def extract_emails(text):\
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+", text)\
\
def extract_phones(text):\
    # Simple phone regex (improve as needed)\
    phone_pattern = r"(\\+44\\s?7\\d\{3\}|\\(?07\\d\{3\}\\)?)\\s?\\d\{3\}\\s?\\d\{3\}"\
    return re.findall(phone_pattern, text)\
\
def get_page_text(url):\
    try:\
        resp = requests.get(url, timeout=5)\
        if resp.status_code == 200:\
            return resp.text\
    except:\
        return ""\
    return ""\
\
def main():\
    st.title("Contact Finder Prototype with SerpAPI")\
    name = st.text_input("Full Name", "")\
    company = st.text_input("Company (optional)", "")\
    \
    if st.button("Search"):\
        if not name:\
            st.warning("Please enter a name.")\
            return\
        \
        query = f'"\{name\}"'\
        if company:\
            query += f' "\{company\}"'\
        query += " contact OR email OR phone"\
\
        st.info("Searching Google via SerpAPI...")\
        results = serpapi_search(query)\
        \
        if not results:\
            st.write("No search results found.")\
            return\
        \
        contacts_found = []\
        for res in results:\
            page_text = get_page_text(res["link"])\
            emails = extract_emails(page_text)\
            phones = extract_phones(page_text)\
            if emails or phones:\
                contacts_found.append(\{"url": res["link"], "emails": emails, "phones": phones\})\
\
        if not contacts_found:\
            st.write("No contacts found in the search results.")\
        else:\
            for contact in contacts_found:\
                st.markdown(f"### URL: [\{contact['url']\}](\{contact['url']\})")\
                if contact['emails']:\
                    st.write("Emails:", ", ".join(contact['emails']))\
                if contact['phones']:\
                    st.write("Phones:", ", ".join(contact['phones']))\
\
if __name__ == "__main__":\
    main()\
}
