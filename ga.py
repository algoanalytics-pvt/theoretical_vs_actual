import os
import streamlit as st
import streamlit.components.v1 as components

GA_ID = "G-8DM8073S27"

# ── People to exclude (add IPs of developers/testers) ──
EXCLUDED_IPS  = ["103.148.120.152"]


def _get_ip() -> str:
    try:
        headers = st.context.headers
        return (
            headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or headers.get("X-Real-Ip", "")
            or "unknown"
        )
    except:
        return "unknown"


def _is_excluded() -> bool:
    ip = _get_ip()
    return ip in EXCLUDED_IPS


def load_ga(app_name: str) -> None:
    """Call once at top of every app."""
    if _is_excluded():
        return  # developer/tester — skip entirely

    components.html(
        f"""
        <script>
        const host = window.parent.location.hostname;
        const isLocal =
            host === "localhost" ||
            host === "127.0.0.1" ||
            host === "0.0.0.0";

        if (!isLocal) {{
            const existing = window.parent.document.querySelector(
                'script[src*="googletagmanager.com/gtag/js?id={GA_ID}"]'
            );
            if (!existing) {{
                const s = window.parent.document.createElement("script");
                s.async = true;
                s.src = "https://www.googletagmanager.com/gtag/js?id={GA_ID}";
                window.parent.document.head.appendChild(s);
            }}

            window.parent.dataLayer = window.parent.dataLayer || [];
            function gtag() {{ window.parent.dataLayer.push(arguments); }}
            window.parent.gtag = window.parent.gtag || gtag;

            setTimeout(() => {{
                window.parent.gtag('js', new Date());
                window.parent.gtag('config', '{GA_ID}', {{
                    app_name:   '{app_name}',
                    page_title: '{app_name}',
                }});
                window.parent.gtag('event', 'app_opened', {{
                    app_name: '{app_name}',
                }});
            }}, 1000);
        }}
        </script>
        """,
        height=0,
    )


def track_event(event_name: str, app_name: str, feature: str = "") -> None:
    """Call on every button/feature you want to track."""
    if _is_excluded():
        return  # developer/tester — skip entirely

    components.html(
        f"""
        <script>
        const host = window.parent.location.hostname;
        const isLocal =
            host === "localhost" ||
            host === "127.0.0.1" ||
            host === "0.0.0.0";

        if (!isLocal && window.parent.gtag) {{
            window.parent.gtag('event', '{event_name}', {{
                app_name: '{app_name}',
                feature:  '{feature}',
            }});
        }}
        </script>
        """,
        height=0,
    )