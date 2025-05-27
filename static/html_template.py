def html_template(title, message, status):
    color = {
        "success": "#10B981",  # verde Tailwind
        "error": "#EF4444",    # vermelho Tailwind
        "warning": "#F59E0B"   # amarelo Tailwind
    }.get(status, "#3B82F6")   # azul padrão (fallback)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                background-color: #111;
                color: #e5e7eb;
                font-family: 'Inter', sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }}
            .container {{
                background-color: #1f2937;
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                text-align: center;
                width: 100%;
                max-width: 480px;
            }}
            h1 {{
                color: {color};
                font-size: 1.875rem;
                margin-bottom: 16px;
                font-weight: 600;
            }}
            p {{
                font-size: 1rem;
                line-height: 1.6;
                color: #d1d5db;
            }}
            .button {{
                display: inline-block;
                margin-top: 24px;
                padding: 10px 20px;
                background-color: {color};
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 500;
                transition: background-color 0.3s ease, color 0.3s ease;
            }}
            .button:hover {{
                background-color: white;
                color: {color};
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <p>{message}</p>
            <a class="button" href="http://localhost:3000/">Back to Home</a>
        </div>
    </body>
    </html>
    """
