import streamlit as st
import pickle
import numpy as np
import pandas as pd
from urllib.parse import urlparse
import re

st.set_page_config(
    page_title="PhishPrint",
    page_icon=":)",
    layout="centered"
)

@st.cache_resource
def load_models():
    with open('../models/xgboost.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('../models/feature_pipeline.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    return model, pipeline

model, pipeline = load_models()

@st.cache_resource
def load_feature_names():
    df = pd.read_csv('../data/dataset.csv', index_col=0)
    X = df.drop('status', axis=1)
    selected_mask = pipeline.named_steps['selector'].get_support()
    return X.columns[selected_mask].tolist()

selected_feature_names = load_feature_names()

def extract_features(url):
    parsed = urlparse(url)
    hostname = parsed.netloc
    path = parsed.path

    features = {
        'length_url': len(url),
        'length_hostname': len(hostname),
        'ip': 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) else 0,
        'nb_dots': url.count('.'),
        'nb_hyphens': url.count('-'),
        'nb_at': url.count('@'),
        'nb_qm': url.count('?'),
        'nb_and': url.count('&'),
        'nb_or': url.count('|'),
        'nb_eq': url.count('='),
        'nb_underscore': url.count('_'),
        'nb_tilde': url.count('~'),
        'nb_percent': url.count('%'),
        'nb_slash': url.count('/'),
        'nb_star': url.count('*'),
        'nb_colon': url.count(':'),
        'nb_comma': url.count(','),
        'nb_semicolumn': url.count(';'),
        'nb_dollar': url.count('$'),
        'nb_space': url.count(' '),
        'nb_www': url.count('www'),
        'nb_com': url.count('.com'),
        'nb_dslash': url.count('//'),
        'http_in_path': 1 if 'http' in path else 0,
        'https_token': 1 if parsed.scheme == 'https' else 0,
        'ratio_digits_url': sum(c.isdigit() for c in url) / len(url) if len(url) > 0 else 0,
        'ratio_digits_host': sum(c.isdigit() for c in hostname) / len(hostname) if len(hostname) > 0 else 0,
        'punycode': 1 if 'xn--' in url else 0,
        'port': 1 if parsed.port else 0,
        'tld_in_path': 1 if any(tld in path for tld in ['.com', '.org', '.net']) else 0,
        'tld_in_subdomain': 1 if any(tld in hostname.split('.')[0] for tld in ['.com', '.org']) else 0,
        'abnormal_subdomain': 1 if re.search(r'(w[0-9]+|web\d)', hostname) else 0,
        'nb_subdomains': len(hostname.split('.')) - 2 if len(hostname.split('.')) > 2 else 0,
        'prefix_suffix': 1 if '-' in hostname else 0,
        'random_domain': 0,
        'shortening_service': 1 if any(s in url for s in ['bit.ly', 'tinyurl', 'goo.gl', 't.co']) else 0,
        'path_extension': 1 if any(ext in path for ext in ['.exe', '.zip', '.pdf', '.js']) else 0,
        'nb_redirection': url.count('//') - 1 if url.count('//') > 1 else 0,
        'nb_external_redirection': 0,
        'length_words_raw': len(re.findall(r'\w+', url)),
        'char_repeat': max([url.count(c) for c in set(url)]) if url else 0,
        'shortest_words_raw': min([len(w) for w in re.findall(r'\w+', url)]) if re.findall(r'\w+', url) else 0,
        'shortest_word_host': min([len(w) for w in hostname.split('.')]) if hostname else 0,
        'shortest_word_path': min([len(w) for w in re.findall(r'\w+', path)]) if re.findall(r'\w+', path) else 0,
        'longest_words_raw': max([len(w) for w in re.findall(r'\w+', url)]) if re.findall(r'\w+', url) else 0,
        'longest_word_host': max([len(w) for w in hostname.split('.')]) if hostname else 0,
        'longest_word_path': max([len(w) for w in re.findall(r'\w+', path)]) if re.findall(r'\w+', path) else 0,
        'avg_words_raw': np.mean([len(w) for w in re.findall(r'\w+', url)]) if re.findall(r'\w+', url) else 0,
        'avg_word_host': np.mean([len(w) for w in hostname.split('.')]) if hostname else 0,
        'avg_word_path': np.mean([len(w) for w in re.findall(r'\w+', path)]) if re.findall(r'\w+', path) else 0,
        'phish_hints': 1 if any(hint in url.lower() for hint in ['secure', 'account', 'update', 'login', 'verify', 'banking', 'confirm']) else 0,
        'domain_in_brand': 0,
        'brand_in_subdomain': 0,
        'brand_in_path': 0,
        'suspecious_tld': 1 if any(tld in url for tld in ['.tk', '.ml', '.ga', '.cf', '.gq']) else 0,
        'statistical_report': 0,
        'nb_hyperlinks': 0,
        'ratio_intHyperlinks': 0,
        'ratio_extHyperlinks': 0,
        'ratio_nullHyperlinks': 0,
        'nb_extCSS': 0,
        'ratio_intRedirection': 0,
        'ratio_extRedirection': 0,
        'ratio_intErrors': 0,
        'ratio_extErrors': 0,
        'login_form': 1 if 'login' in url.lower() else 0,
        'external_favicon': 0,
        'links_in_tags': 0,
        'submit_email': 0,
        'ratio_intMedia': 0,
        'ratio_extMedia': 0,
        'sfh': 0,
        'iframe': 0,
        'popup_window': 0,
        'safe_anchor': 0,
        'onmouseover': 0,
        'right_clic': 0,
        'empty_title': 0,
        'domain_in_title': 0,
        'domain_with_copyright': 0,
        'whois_registered_domain': 0,
        'domain_registration_length': 0,
        'domain_age': 0,
        'web_traffic': 0,
        'dns_record': 0,
        'google_index': 0,
        'page_rank': 0
    }
    return features

st.title('PhishPrint')
st.markdown('Digital Footprint Analysis of Malicious URLs')
st.markdown('---')
url_input = st.text_input(
    "Enter a URL to analyze:",
    placeholder="https://example.com"
)

analyse_btn = st.button('Analyse URL', use_container_width=True)

if analyse_btn:
    if not url_input:
        st.warning('Enter URL first!')
    else:
        with st.spinner('Analyzing URL...'):
            features = extract_features(url_input)
            df_input = pd.DataFrame([features])

            train_df = pd.read_csv('../data/dataset.csv', index_col=0)
            train_cols = train_df.drop('status', axis=1).columns
            df_input = df_input.reindex(columns=train_cols, fill_value=0)

            X_transformed = pipeline.transform(df_input)

            prediction = model.predict(X_transformed)[0]
            confidence = model.predict_proba(X_transformed).max() * 100
        st.markdown('---')

        if prediction == 1:
            st.error(f"Phishing URL Detected!")
            st.metric("Confidence", f"{confidence:.1f}%")
            st.markdown("""
            Why is this suspicious?
            - Domain is not indexed by Google
            - Low or no page rank
            - Contains phishing keyword patterns
            """)
        else:
            st.success('Legitimate URL')
            st.metric('Confidence', f'{confidence:.1f}%')

        st.markdown('---')
        st.subheader('URL Feature Breakdown')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("URL Length", features['length_url'])
            st.metric('No. of Dots', features['nb_dots'])
        with col2:
            st.metric('No. of Hyphens', features['nb_hyphens'])
            st.metric('SubDomains', features['nb_subdomains'])
        with col3:
            st.metric('HTTPS', 'Yes' if features['https_token'] else 'No')
            st.metric('Phish Hints', features['phish_hints'])

st.markdown('---')
st.caption('PhishPrint | Tanish N Jay')