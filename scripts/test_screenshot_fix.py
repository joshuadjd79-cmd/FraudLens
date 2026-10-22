import os, re
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "assets")

def test_render():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 1100)
    ax.set_ylim(0, 620)
    ax.axis('off')

    char_w = 8.60215
    sql_text = """SELECT customer_id,
       UPPER(first_name || ' ' || last_name) AS full_name_uppercase,
       LOWER(email) AS standardized_email,
       LENGTH(phone) AS phone_len,
       SUBSTR(phone, 1, 3) AS country_code
FROM CUSTOMER
WHERE customer_id IN (1001, 1002, 1005);"""

    sql_lines = sql_text.strip().split('\n')
    curr_line_y = 492
    KEYWORDS = {'SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'GROUP', 'BY', 'HAVING', 'ORDER', 'IN', 'BETWEEN', 'AND', 'AS', 'COUNT', 'SUM', 'AVG', 'ROUND', 'UPPER', 'LOWER', 'SUBSTR', 'LENGTH', 'DESC', 'ASC', 'UPDATE', 'SET', 'DELETE', 'INSERT', 'INTO', 'VALUES'}

    for l_idx, line in enumerate(sql_lines):
        ax.text(38, curr_line_y, str(l_idx + 1), color='#94A3B8', fontsize=7.5, ha='right', va='center', family='monospace')
        if line.strip().startswith('--'):
            ax.text(52, curr_line_y, line, color='#16A34A', fontsize=8, va='center', family='monospace', fontstyle='italic')
        else:
            tokens = list(re.finditer(r"(--[^\n]*|'[^']*'|\b[A-Za-z_][A-Za-z0-9_]*\b|\S)", line))
            for m in tokens:
                token_str = m.group(0)
                pos_x = 52 + m.start() * char_w
                up_t = token_str.upper().rstrip(';,()')
                if token_str.startswith('--'):
                    c = '#16A34A'
                elif token_str.startswith("'"):
                    c = '#B91C1C'
                elif up_t in KEYWORDS:
                    c = '#004085'
                else:
                    c = '#1F2937'
                ax.text(pos_x, curr_line_y, token_str, color=c, fontsize=8, va='center', family='monospace')
        curr_line_y -= 14

    out_file = os.path.join(ASSETS_DIR, "test_render.png")
    fig.savefig(out_file, dpi=300)
    plt.close(fig)
    print("Test render successful:", out_file)

if __name__ == "__main__":
    test_render()
