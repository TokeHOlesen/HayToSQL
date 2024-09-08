class Report:
    @staticmethod
    def generate_html_head():
        return ("""
<!DOCTYPE html>
<html lang="dk">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;500;700&display=swap" rel="stylesheet">
    <title>Palissade ugerapport</title>
    <style>
        body {
            font-family: 'Fira Sans', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #EAEAEA;
            color: #030303;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 20px;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
        }
        .header {
            background-color: #007BFF;
            color: #ffffff;
            padding: 10px 20px;
            text-align: center;
            border-radius: 5px;
        }
        .week-summary {
            color: #333;
            padding: 2px 20px;
            margin: 10px auto;
            border: 2px solid lightblue;
            border-radius: 5px;
            line-height: 0.8;
        }
        .day {
            margin-top: 20px;
            border: 2px solid lightblue;
            border-radius: 5px;
            padding: 0px 20px;
            padding-bottom: 20px;
            text-align: left;
            line-height: 0.9;
            margin-bottom: 20px;
            background-color: #fff;
        }
        .kid {
            background-color: #f9f9f9;
            padding: 5px 10px;
            margin-top: 10px;
            padding-left: 40px;
            line-height: 0.8;
            border-left: 3px solid lightblue;
            position: relative;
        }

        .kid:first-child {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="container">
""")

    @staticmethod
    def generate_header(start_date, end_date):
        return (f"""
        <div class="header">
            <h1>Ugerapport for perioden {start_date} - {end_date}</h1>
        </div>
        """)

    @staticmethod
    def generate_week_summary(orders_total, ldm_total):
        return (f"""
        <div class="week-summary">
            <h3>Ordrer i alt: {orders_total}.</h3>
            <h3>Lademeter i alt: {ldm_total} ldm.</h3>
        </div>
        """)

    @staticmethod
    def generate_day_head(weekday,
                          date,
                          items_total,
                          ldm_total,
                          orders_total,
                          kids_total,
                          dates,
                          destinations,
                          order_list):
        return (f"""
        <div class="day">
            <h2>{weekday} d. {date}</h2>
            <p>Varer i alt: {items_total}.</p>
            <p>Ca. ldm i alt: {round(ldm_total, 2)}.</p>
            <p>Ordrer i alt: {orders_total}.</p>
            <p>KID'er i alt: {kids_total}.</p>
            <p>Ordrene har følgende bekræftelsesdatoer: {', '.join(dates)}.</p>
            <p>Destinationer: {', '.join(destinations)}.</p>
            <p style="line-height: 1.2">{'|&#8203;'.join(order_list)}</p>
        """)

    @staticmethod
    def generate_day_tail():
        return ("""
        </div>
        """)

    @staticmethod
    def generate_kid(kid_number,
                     custname,
                     city,
                     country,
                     confirmed_dates,
                     orders_total,
                     items_total,
                     ldm_total,
                     order_numbers):
        ordre_dato_msg, ordre_msg = ("Ordren", "ordre") if orders_total == 1 else ("Ordrerne", "ordrer")
        vare_msg = "vare" if items_total == 1 else "varer"
        return (f"""
            <div class="kid">
                <h3>KID nr. {kid_number}:</h3>
                <p>{custname}, {city}, {country}.</p>
                <p>{orders_total} {ordre_msg}, {items_total} {vare_msg}, ca. {round(ldm_total, 2)} ldm.</p>
                <p>{ordre_dato_msg} er bekræftet til d.: {', '.join(confirmed_dates)}.</p>
                <p>{'|'.join(order_numbers)}</p>
            </div>
        """)

    @staticmethod
    def generate_html_tail():
        return ("""
    </div>
</body>
</html>
        """)
