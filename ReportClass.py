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
            color: #FFFFFF;
            padding: 10px 20px;
            text-align: center;
            border-radius: 5px;
        }
        .week-summary {
            color: #030303;
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
            background-color: #FFFFFF;
        }
        .kid {
            background-color: #F9F9F9;
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
        .blue-box {
            background-color: #E0F7FA;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #B2EBF2;
            display: inline-block;
        }
        .red-box {
            background-color: #FCE4EC;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #F8BBD0;
            display: inline-block;
        }
        .yellow-box {
            background-color: #FFF9C4;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #FFF59D;
            display: inline-block;
        }
        .green-box {
            background-color: #E8F5E9;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #C8E6C9;
            display: inline-block;
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
    def generate_week_summary(normal_items_total,
                              dsv_items_total,
                              orders_total,
                              ldm_total,
                              dsv_ldm_total,
                              kids_total,
                              hay_direct_kids_total,
                              potentially_delayed_orders_total):
        return (f"""
        <div class="week-summary">
            <h3>Varer i alt: {normal_items_total + dsv_items_total} stk (almindelige ordrer: {normal_items_total} stk, DSV ordrer: {dsv_items_total} stk).</h3>
            <h3>Ca. lademeter i alt: {ldm_total + dsv_ldm_total} ldm (almindelige ordrer: {ldm_total} ldm, DSV ordrer: {dsv_ldm_total} ldm).</h3>
            <h3>Almindelige ordrer i alt: {orders_total}.</h3>
            <h3>Konsoliderede ordregrupper i alt (almindelige ordrer): {kids_total}.</h3>
            <h3>Hay-Direct ordrer: {hay_direct_kids_total}.</h3>
            <h3>Ordrer med forsinkelsesrisiko: {potentially_delayed_orders_total}.</h3>
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
            <p>Ca. ldm i alt: {round(ldm_total, 2)} ldm.</p>
            <p>Ordrer i alt: {orders_total}.</p>
            <p>Konsoliderede ordregrupper i alt: {kids_total}.</p>
            <p>Varer per KID i gennemsnit: {round(items_total / kids_total, 1)}.</p>
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
                     order_numbers,
                     is_moved_back,
                     is_delayed,
                     is_hay_direct,
                     is_big):
        ordre_dato_msg, ordre_msg = ("Ordren", "ordre") if orders_total == 1 else ("Ordrerne", "ordrer")
        vare_msg = "vare" if items_total == 1 else "varer"

        tags = []
        if is_delayed:
            tags.append('<p class="red-box">Forsinkelsesrisiko: ordren skal rykkes frem til ugen før.</p>')
        if is_hay_direct:
            tags.append('<p class="yellow-box">Hay-Direct ordre.</p>')
        if is_moved_back and not is_delayed:
            tags.append('<p class="green-box">Rykket frem for at matche leveringsdatoen for dette land.</p>')
        if is_big:
            tags.append('<p class="blue-box">Stor ordre.</p>')

        all_tags = "\n".join(tags)
        return (f"""
            <div class="kid">
                <h3>Konsolideret ordregruppe nr. {kid_number}:</h3>
                {all_tags}
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
